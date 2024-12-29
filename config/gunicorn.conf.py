from config.settings import (GUNICORN_BACKLOG, GUNICORN_GRACEFUL_TIMEOUT,
                             GUNICORN_KEEPALIVE, GUNICORN_LOGLEVEL,
                             GUNICORN_MAX_REQUESTS,
                             GUNICORN_MAX_REQUESTS_JITTER, GUNICORN_THREADS,
                             GUNICORN_WORKER_CONNECTIONS, GUNICORN_WORKERS)

workers = GUNICORN_WORKERS
threads = GUNICORN_THREADS
loglevel = GUNICORN_LOGLEVEL
errorlog = '-'
accesslog = '-'

backlog = GUNICORN_BACKLOG
worker_connections = GUNICORN_WORKER_CONNECTIONS
max_requests = GUNICORN_MAX_REQUESTS
max_requests_jitter = GUNICORN_MAX_REQUESTS_JITTER
graceful_timeout = GUNICORN_GRACEFUL_TIMEOUT
keepalive = GUNICORN_KEEPALIVE
