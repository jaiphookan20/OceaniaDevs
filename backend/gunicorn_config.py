import multiprocessing

# bind = "0.0.0.0:4040"  # Bind the application to all network interfaces on port 4040
# workers = multiprocessing.cpu_count() * 2 + 1  # Number of worker processes, calculated based on the number of CPU cores
# threads = 2  # Number of threads per worker
# worker_class = "gthread"  # Use the gthread worker class for handling requests
# timeout = 120  # Timeout for requests in seconds
# keepalive = 5  # Keep-alive time in seconds for connections


# Gunicorn works by internally handing the calling of your flask code. 
# This is done by having workers ready to handle the requests instead of the sequential one-at-a-time model that the default flask server provides. 
# The end result is your app can handle more requests per second.

bind = "0.0.0.0:4040"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 4
worker_class = "gthread"
timeout = 300  # 5 minutes
keepalive = 5
worker_tmp_dir = "/dev/shm"
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 120