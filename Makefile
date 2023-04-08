help:
	make -h

venv: # Open the virtual environment shell
	pipenv shell

check: # Check for inconsistencies using Black Formatter
	black --check --diff onestop

format: # Format code with Black and isort
	black onestop
	isort --profile black onestop

