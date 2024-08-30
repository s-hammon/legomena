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
	@${PY} -m unittest discover -s .

run: $(VENV) 
	@. $(BIN)/activate
	@${PY} main.py

tidy: $(VENV)
	@pip list --format=freeze > requirements.txt

clean:
	@rm -rf $(VENV)
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete