import multiprocessing

bind = "0.0.0.0:4040"  # Change this line to bind to all interfaces
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "gthread"
timeout = 120
keepalive = 5
