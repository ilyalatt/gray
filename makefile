.PHONY: restore run

restore:
	if [ ! -d ".venv" ]; then PIPENV_VENV_IN_PROJECT=true pipenv install --dev; fi

run: restore
	pipenv run python3 src/main.py
