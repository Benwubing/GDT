VENV_DIR = env
REQUIREMENTS_FILE = gdt/requirements.txt
MANAGE_PY = gdt/manage.py

# Targets
.PHONY: all setup run

all: setup run

setup:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "Activating virtual environment and installing requirements..."
	@source $(VENV_DIR)/bin/activate && pip install -r $(REQUIREMENTS_FILE)
	@echo "Creating admin user..."
	@source $(VENV_DIR)/bin/activate && python $(MANAGE_PY) create_admin_user

run:
	@echo "Starting the server..."
	@source $(VENV_DIR)/bin/activate && python $(MANAGE_PY) runserver