from fastapi import FastAPI
app = FastAPI()
from routes.train import router as upload_router
from tasks import app as ceApp

@app.get("/task/{task_id}")
def get_task_status(task_id: str):
    result = ceApp.AsyncResult(task_id)
    if result.ready():
        return {"task_id": task_id, "status": result.status, "result": result.result}
    else:
        return {"task_id": task_id, "status": result.status, "result": "Task is still processing"}

app.include_router(upload_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
