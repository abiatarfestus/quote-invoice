help:
	make -h

venv: # Open the virtual environment shell
	pipenv shell

check: # Check for inconsistencies using Black Formatter
	black --check --diff quote_invoice

format: # Format code with Black and isort
	black quote_invoice
	isort --profile black quote_invoice

