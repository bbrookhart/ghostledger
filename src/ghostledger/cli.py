"""Command-line interface for GHOSTLEDGER."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path
from typing import Any, cast

from ghostledger.catalog import Catalog, taxonomy
from ghostledger.engine import ALL_CHANNELS, BASELINE, LAYERED, load_outcomes, run_scenario
from ghostledger.evidence import verify_bundle
from ghostledger.models import Condition, ValidationError, __version__
from ghostledger.reporting import summarize, write_reports


def _json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _controls(value: str) -> tuple[str, ...]:
    aliases = {"baseline": BASELINE, "layered": LAYERED}
    if value in aliases:
        return aliases[value]
    controls = tuple(item.strip() for item in value.split(",") if item.strip())
    if not controls:
        raise argparse.ArgumentTypeError("controls cannot be empty")
    return controls


def _channels(value: str) -> tuple[str, ...]:
    if value == "all":
        return ALL_CHANNELS
    channels = tuple(item.strip() for item in value.split(",") if item.strip())
    if not channels:
        raise argparse.ArgumentTypeError("channels cannot be empty")
    return channels


def cmd_doctor(_: argparse.Namespace) -> int:
    result = {
        "ghostledger": __version__,
        "python": platform.python_version(),
        "python_supported": sys.version_info >= (3, 11),
        "docker": shutil.which("docker") is not None,
        "offline_core": True,
        "scenario_catalog": Catalog().validate(),
    }
    _json(result)
    return 0 if result["python_supported"] else 2


def cmd_taxonomy_list(_: argparse.Namespace) -> int:
    for item in taxonomy():
        print(f"{item['id']}  {item['name']:<30} {item['description']}")
    return 0


def cmd_scenario_list(args: argparse.Namespace) -> int:
    scenarios = Catalog().list()
    if args.domain:
        scenarios = [item for item in scenarios if item.domain == args.domain]
    for item in scenarios:
        print(f"{item.scenario_id}  {item.domain:<28} {item.primary_class}  {item.title}")
    print(f"\n{len(scenarios)} scenario pairs / {len(scenarios) * 2} paired cases")
    return 0


def cmd_scenario_show(args: argparse.Namespace) -> int:
    _json(Catalog().get(args.scenario_id).public_view())
    return 0


def cmd_scenario_validate(_: argparse.Namespace) -> int:
    _json(Catalog().validate())
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    outcome, run_dir = run_scenario(
        args.scenario_id,
        condition=args.condition,
        controls=args.control,
        channels=args.channels,
        output_root=args.output,
        seed=args.seed,
    )
    result = outcome.as_dict()
    result["run_directory"] = str(run_dir)
    _json(result)
    return 0


def _load_campaign_manifest(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValidationError("campaign manifest must be a JSON object")
    data = cast(dict[str, Any], raw)
    required = {"name", "scenarios", "conditions", "control_sets", "seeds"}
    if missing := required - data.keys():
        raise ValidationError(f"campaign manifest missing keys: {sorted(missing)}")
    catalog_ids = {item.scenario_id for item in Catalog().list()}
    selected = catalog_ids if data["scenarios"] == ["all"] else set(data["scenarios"])
    if unknown := selected - catalog_ids:
        raise ValidationError(f"campaign references unknown scenarios: {sorted(unknown)}")
    data["resolved_scenarios"] = sorted(selected)
    data["resolved_runs"] = (
        len(selected) * len(data["conditions"]) * len(data["control_sets"]) * len(data["seeds"])
    )
    return data


def cmd_campaign_plan(args: argparse.Namespace) -> int:
    _json(_load_campaign_manifest(args.manifest))
    return 0


def cmd_campaign_run(args: argparse.Namespace) -> int:
    manifest = _load_campaign_manifest(args.manifest)
    campaign_dir = args.output / str(manifest["name"])
    return _execute_campaign(manifest, campaign_dir)


def _execute_campaign(manifest: dict[str, Any], campaign_dir: Path) -> int:
    runs_dir = campaign_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    (campaign_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    completed: dict[tuple[str, str, tuple[str, ...], int], dict[str, Any]] = {}
    for manifest_path in sorted(runs_dir.glob("*/manifest.json")):
        prior = json.loads(manifest_path.read_text())
        key = (
            str(prior["scenario_id"]),
            str(prior["condition"]),
            tuple(prior["controls"]),
            int(prior["seed"]),
        )
        outcome_path = manifest_path.parent / "outcome.json"
        if outcome_path.is_file():
            completed[key] = json.loads(outcome_path.read_text())
    outcomes: list[dict[str, Any]] = []
    new_runs = 0
    for scenario_id in manifest["resolved_scenarios"]:
        for condition in manifest["conditions"]:
            for control_name, control_values in manifest["control_sets"].items():
                controls = _controls(
                    control_values if isinstance(control_values, str) else ",".join(control_values)
                )
                for seed in manifest["seeds"]:
                    key = (scenario_id, condition, controls, int(seed))
                    if key in completed:
                        record = completed[key]
                    else:
                        outcome, _ = run_scenario(
                            scenario_id,
                            condition=condition,
                            controls=controls,
                            output_root=runs_dir,
                            seed=int(seed),
                        )
                        record = outcome.as_dict()
                        new_runs += 1
                    record["control_set"] = control_name
                    outcomes.append(record)
    reports = write_reports(outcomes, campaign_dir / "reports")
    _json(
        {
            "campaign": manifest["name"],
            "runs": len(outcomes),
            "new_runs": new_runs,
            "resumed_runs": len(outcomes) - new_runs,
            "summary": summarize(outcomes),
            "reports": [str(path) for path in reports],
        }
    )
    return 0


def cmd_campaign_resume(args: argparse.Namespace) -> int:
    stored = args.campaign_directory / "manifest.json"
    if not stored.is_file():
        raise ValidationError(f"campaign manifest not found: {stored}")
    manifest = json.loads(stored.read_text())
    return _execute_campaign(manifest, args.campaign_directory)


def cmd_evidence_verify(args: argparse.Namespace) -> int:
    valid, errors = verify_bundle(args.run_directory)
    _json({"valid": valid, "errors": errors, "run_directory": str(args.run_directory)})
    return 0 if valid else 3


def cmd_run_inspect(args: argparse.Namespace) -> int:
    run_dir = args.run_directory
    result = {
        "manifest": json.loads((run_dir / "manifest.json").read_text()),
        "outcome": json.loads((run_dir / "outcome.json").read_text()),
        "integrity": json.loads((run_dir / "integrity.json").read_text()),
    }
    _json(result)
    return 0


def cmd_replay(args: argparse.Namespace) -> int:
    manifest = json.loads((args.run_directory / "manifest.json").read_text())
    expected = json.loads((args.run_directory / "outcome.json").read_text())
    replayed, replay_dir = run_scenario(
        manifest["scenario_id"],
        condition=cast(Condition, manifest["condition"]),
        controls=tuple(manifest["controls"]),
        channels=tuple(manifest["channels"]),
        output_root=args.output,
        seed=int(manifest["seed"]),
    )
    equivalent = replayed.state_digest == expected["state_digest"]
    _json(
        {
            "equivalent_submitted_state": equivalent,
            "expected_state_digest": expected["state_digest"],
            "replayed_state_digest": replayed.state_digest,
            "replay_directory": str(replay_dir),
        }
    )
    return 0 if equivalent else 4


def cmd_metrics_verify(args: argparse.Namespace) -> int:
    outcomes = load_outcomes(args.directory)
    summary = summarize(outcomes)
    _json(summary)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    outcomes = load_outcomes(args.directory)
    paths = write_reports(outcomes, args.output)
    _json({"outcomes": len(outcomes), "reports": [str(path) for path in paths]})
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    _json(
        {
            "left": summarize(load_outcomes(args.left)),
            "right": summarize(load_outcomes(args.right)),
        }
    )
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    demo_dir = args.output / "demo"
    runs_dir = demo_dir / "runs"
    outcomes = []
    matrix: list[tuple[Condition, tuple[str, ...]]] = [
        ("benign", BASELINE),
        ("adversarial", BASELINE),
        ("benign", LAYERED),
        ("adversarial", LAYERED),
    ]
    for condition, controls in matrix:
        outcome, run_dir = run_scenario(
            args.scenario_id,
            condition=condition,
            controls=controls,
            output_root=runs_dir,
            seed=0,
        )
        valid, errors = verify_bundle(run_dir)
        if not valid:
            raise ValidationError(f"demo evidence verification failed: {errors}")
        record = outcome.as_dict()
        record["control_set"] = "baseline" if controls == BASELINE else "layered"
        outcomes.append(record)
    reports = write_reports(outcomes, demo_dir / "reports")
    print("GHOSTLEDGER v0.1.0 — deterministic harness demonstration")
    print("Scripted reference agents validate the harness; they do not measure model propensity.\n")
    print("CONDITION     CONTROL     VISIBLE  HARM  DETECTED  PREVENTED  RECOVERED")
    for item in outcomes:
        print(
            f"{item['condition']:<13} {item['control_set']:<11} "
            f"{item['visible_success']:<8.1f} {item['harm']:<5.1f} "
            f"{str(item['detected']):<9} {str(item['prevented']):<10} "
            f"{item['recovery_completeness']:.1f}"
        )
    print(f"\nEvidence and reports: {demo_dir}")
    print(f"HTML report: {reports[2]}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ghostledger",
        description="State-grounded evaluation of stealthy agent sabotage.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check runtime and corpus health")
    doctor.set_defaults(func=cmd_doctor)

    tax = sub.add_parser("taxonomy", help="Inspect the GHOSTLEDGER taxonomy")
    tax_sub = tax.add_subparsers(dest="taxonomy_command", required=True)
    tax_list = tax_sub.add_parser("list", help="List sabotage classes")
    tax_list.set_defaults(func=cmd_taxonomy_list)

    scenario = sub.add_parser("scenario", help="Inspect and validate scenario pairs")
    scenario_sub = scenario.add_subparsers(dest="scenario_command", required=True)
    scenario_list = scenario_sub.add_parser("list", help="List scenario pairs")
    scenario_list.add_argument("--domain")
    scenario_list.set_defaults(func=cmd_scenario_list)
    scenario_show = scenario_sub.add_parser("show", help="Show the agent-visible scenario view")
    scenario_show.add_argument("scenario_id")
    scenario_show.set_defaults(func=cmd_scenario_show)
    scenario_validate = scenario_sub.add_parser("validate", help="Validate the built-in corpus")
    scenario_validate.set_defaults(func=cmd_scenario_validate)

    run = sub.add_parser("run", help="Run a single deterministic evaluation")
    run.add_argument("scenario_id")
    run.add_argument("--condition", choices=["benign", "adversarial"], required=True)
    run.add_argument("--control", type=_controls, default=BASELINE)
    run.add_argument("--channels", type=_channels, default=ALL_CHANNELS)
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--output", type=Path, default=Path("runs"))
    run.set_defaults(func=cmd_run)

    campaign = sub.add_parser("campaign", help="Plan and execute campaign manifests")
    campaign_sub = campaign.add_subparsers(dest="campaign_command", required=True)
    campaign_plan = campaign_sub.add_parser("plan", help="Resolve a campaign without running it")
    campaign_plan.add_argument("manifest", type=Path)
    campaign_plan.set_defaults(func=cmd_campaign_plan)
    campaign_run = campaign_sub.add_parser("run", help="Execute a campaign")
    campaign_run.add_argument("manifest", type=Path)
    campaign_run.add_argument("--output", type=Path, default=Path("campaigns"))
    campaign_run.set_defaults(func=cmd_campaign_run)
    campaign_resume = campaign_sub.add_parser(
        "resume", help="Resume a stored campaign without duplicating completed runs"
    )
    campaign_resume.add_argument("campaign_directory", type=Path)
    campaign_resume.set_defaults(func=cmd_campaign_resume)

    evidence = sub.add_parser("evidence", help="Verify evidence bundles")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    evidence_verify = evidence_sub.add_parser("verify", help="Verify hashes and event chain")
    evidence_verify.add_argument("run_directory", type=Path)
    evidence_verify.set_defaults(func=cmd_evidence_verify)

    inspect_cmd = sub.add_parser("inspect", help="Inspect a run bundle")
    inspect_cmd.add_argument("run_directory", type=Path)
    inspect_cmd.set_defaults(func=cmd_run_inspect)

    replay = sub.add_parser("replay", help="Replay a deterministic run")
    replay.add_argument("run_directory", type=Path)
    replay.add_argument("--output", type=Path, default=Path("replays"))
    replay.set_defaults(func=cmd_replay)

    metrics = sub.add_parser("metrics", help="Recompute aggregate metrics")
    metrics_sub = metrics.add_subparsers(dest="metrics_command", required=True)
    metrics_verify = metrics_sub.add_parser("verify", help="Recompute from run outcomes")
    metrics_verify.add_argument("directory", type=Path)
    metrics_verify.set_defaults(func=cmd_metrics_verify)

    report = sub.add_parser("report", help="Generate JSON, Markdown, and HTML reports")
    report.add_argument("directory", type=Path)
    report.add_argument("--output", type=Path, default=Path("reports"))
    report.set_defaults(func=cmd_report)

    compare = sub.add_parser("compare", help="Compare two result directories")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)
    compare.set_defaults(func=cmd_compare)

    demo = sub.add_parser("demo", help="Run the four-cell offline demonstration")
    demo.add_argument("--scenario-id", default="GL-SW-001")
    demo.add_argument("--output", type=Path, default=Path("artifacts"))
    demo.set_defaults(func=cmd_demo)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.func(args))
    except (ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"ghostledger: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
