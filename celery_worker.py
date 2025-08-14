import platform
import os
from celery import Celery

# Force pool type if on Windows
pool_arg = []
if platform.system() == "Windows":
    pool_arg = ["--pool=solo"]

os.system(
    " ".join(["celery", "-A", "lizzy_hairapy", "worker", "-l", "info"] + pool_arg)
)
