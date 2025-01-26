.PHONY: install run test clean test-api run-and-test

# Python interpreter
PYTHON = python3
VENV = .venv
BIN = $(VENV)/bin

# Scripts directory
SCRIPTS_DIR = scripts

# Default target
all: install

# Create virtual environment and install dependencies
install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && pip install --upgrade pip
	. $(VENV)/bin/activate && pip install -r requirements.txt

# Run the application
run: install
	. $(VENV)/bin/activate && $(PYTHON) app.py

# Run all tests
test:
	. $(VENV)/bin/activate && pytest -v

# Run API tests
test-api:
	$(SCRIPTS_DIR)/test_api.sh

# Run application and API tests
run-and-test: run
	sleep 2
	$(SCRIPTS_DIR)/test_api.sh

# Clean up
clean:
	chmod +x $(SCRIPTS_DIR)/clean.sh && $(SCRIPTS_DIR)/clean.sh

# Docker targets (for local development without installing dependencies)
docker-build:
	docker build -t home-assignment-api .

docker-run: docker-clean docker-build
	docker run -p 8000:8000 -d --name home-assignment-api home-assignment-api

docker-test-api: docker-clean docker-run
	sleep 3 # Wait for server to start before running tests
	$(SCRIPTS_DIR)/test_api.sh

docker-clean:
	docker rm -f home-assignment-api