PY = python3
VENV = .venv
BIN=$(VENV)/bin

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif

$(VENV): requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt
	@touch $(VENV)

test: $(VENV)
	@. $(BIN)/activate
	@${PY} -m unittest discover -s tests

clean:
	@rm -rf $(VENV)
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

# make build
build:
	@pip install .

.PHONY: test clean build