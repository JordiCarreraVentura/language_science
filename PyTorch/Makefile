VENV_DIR := ../environments/pytorch
PYTHON := $(shell which python3)
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := . $(VENV_DIR)/bin/activate

.PHONY: all
all: venv

.PHONY: venv
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment at $(VENV_DIR)"; \
		$(PYTHON) -m venv $(VENV_DIR); \
	else \
		echo "Virtual environment already exists at '$(VENV_DIR)'"; \
	fi

.PHONY: install
install: venv
	@echo "Installing dependencies into '$(VENV_DIR)'"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

.PHONY: jupyter
jupyter: venv
	@jupyter notebook

.PHONY: clean
clean:
	@echo "Deleting virtual environment at '$(VENV_DIR)'"
	rm -rf $(VENV_DIR)
