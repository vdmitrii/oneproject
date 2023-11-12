run_experiment:
	poetry run git init
	poetry run dvc init -f
	poetry run dvc repro