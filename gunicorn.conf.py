# Config File
wsgi_app = 'wacsv:create_app()'

# Debugging
reload = True

# Server Socket
bind = "0.0.0.0:8001"

# Worker Processes
workers = 2
worker_class = 'sync'
timeout = 30
keepalive = 2
