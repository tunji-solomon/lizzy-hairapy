# tasks.py
from celery import Celery

# Connect to Redis (adjust if your container name is different)
app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')  # 👈 result backend

app.conf.update(
    result_expires=3600,  # results expire in 1 hour
)

@app.task
def add(x, y):
    return x + y
