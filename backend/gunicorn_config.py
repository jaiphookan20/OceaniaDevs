import multiprocessing

bind = "127.0.0.1:4040"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "gthread"
timeout = 120
keepalive = 5