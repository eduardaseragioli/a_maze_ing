PYTHON = python3
PIP = pip
REQS = requirements.txt
CONFIG = config.txt
MAIN = a_maze_ing.py

all: install

install:
	$(PIP) install -r $(REQS)

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 . --exclude=lib
	mypy . --warn-return-any --warn-unused-ignores \
	       --ignore-missing-imports --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	rm -rf __pycache__ .mypy_cache

.PHONY: all install run debug lint lint-strict clean