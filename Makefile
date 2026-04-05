PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug clean lint

all: run

install:
	pip install flake8 mypy build

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache build dist *.egg-info mazegen/__pycache__ maze.txt

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .