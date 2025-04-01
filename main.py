from fastapi import FastAPI

from tasks import app as ceApp

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello man"}


@app.post("/add")
def add_number(x: int, y: int):
    task = ceApp.send_task("tasks.add_task", args=[x, y])
    return {"task_id": task.id, "status": "Processing"}

@app.get("/task/{task_id}")
def get_task_status(task_id: str):
    result = ceApp.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
