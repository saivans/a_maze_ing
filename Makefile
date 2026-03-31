# Makefile for A-Maze-ing project

# Variables
PYTHON = python3
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt
SRC_DIR = src

# Default target
all: run

# Install dependencies
install:
	pip install flake8 mypy
	# Add any other dependencies your project needs
	# pip install -r requirements.txt

# Run the main program
run:
	PYTHONPATH=$(SRC_DIR) $(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

# Run with debugger
debug:
	PYTHONPATH=$(SRC_DIR) $(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf $(SRC_DIR)/__pycache__ 2>/dev/null || true
	rm -rf tests/__pycache__ 2>/dev/null || true

# Run linter and type checker
lint:
	flake8 $(SRC_DIR) $(MAIN_SCRIPT)
	mypy $(SRC_DIR) $(MAIN_SCRIPT) --warn-return-any --warn-unused-ignores 
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Run strict linting (optional)
lint-strict:
	flake8 $(SRC_DIR) $(MAIN_SCRIPT)
	mypy $(SRC_DIR) $(MAIN_SCRIPT) --strict

# Run tests (if you add tests later)
test:
	PYTHONPATH=$(SRC_DIR) python -m pytest tests/ -v

# Help target
help:
	@echo "Available targets:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Execute the main program"
	@echo "  make debug       - Run with Python debugger"
	@echo "  make clean       - Remove temporary files"
	@echo "  make lint        - Run flake8 and mypy checks"
	@echo "  make lint-strict - Run strict mypy checks"
	@echo "  make test        - Run pytest tests"
	@echo "  make help        - Show this help message"

.PHONY: all install run debug clean lint lint-strict test help