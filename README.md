# Wolt Backend Internship Assignment 2025

This project implements a delivery fee calculator API for Wolt's 2025 Engineering Internship.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- make (Unix utility for building and running projects)
- docker (Docker container engine) and running docker daemon
- curl (optional) - for testing API
- pytest (optional) - for running tests

# Without Docker

## Install the project

```bash
make install
```

## Run the application

Run the application and start server in the virtual environment.
```bash
make run
```

## Run all tests

```bash
make test
```

## Run specific tests

```bash
make test-delivery
make test-range
make test-venue
```

## Clean up

Clean up the virtual environment and remove all generated files.
```bash
make clean
```


# With Docker

```bash 
make docker-run # Run the application in docker container and start server.
make docker-test-api # Run application, then run the test script to test the API.
make docker-clean # Clean up docker container.
```

