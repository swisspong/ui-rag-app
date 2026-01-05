
start-dev-local:
	python ./init_db.py && PYTHONPATH=$(CURDIR) fastapi dev --port 8005 src/interfaces/http/server.py
start-prod-local:
	PYTHONPATH=$(CURDIR) fastapi run --workers 4 --port 8002 src/interfaces/http/server.py
start-worker:
	PYTHONPATH=$(CURDIR) celery -A src.contexts.rag.infrastructure.queues.celery_app worker --loglevel=info -E