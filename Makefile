.PHONY: install test check demo clean

install:
	python -m pip install -e .

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

check:
	PYTHONPATH=src python -m compileall -q src tests
	PYTHONPATH=src python -m ghostledger scenario validate
	PYTHONPATH=src python scripts/check_repository.py

demo:
	PYTHONPATH=src python -m ghostledger demo

clean:
	python scripts/clean_artifacts.py
