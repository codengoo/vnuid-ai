from celery import Celery

app = Celery(
    "tasks",
    broker="amqp://user:password@localhost:5672//",
    backend="rpc://"
)

@app.task
def add_task(x, y):
    print(x,y)
    return x + y