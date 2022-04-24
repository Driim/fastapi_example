format:
	poetry run black src tests --safe

lint:
	poetry run flake8 src tests

tests:
	poetry run pytest

run-campaign:
	python -m uvicorn src.campaign.main:app --port 80

run-campaign-dev:
	@(export $(shell cat src/campaign/.env) && poetry run python -m uvicorn src.campaign.main:app --reload)

