import shutil

from fastapi import FastAPI
app = FastAPI()
from routes.train import router as upload_router


# @app.post("/add")
# def add_number(x: int, y: int):
#     task = ceApp.send_task("tasks.add_task", args=[x, y])
#     return {"task_id": task.id, "status": "Processing"}
#
#
# @app.get("/task/{task_id}")
# def get_task_status(task_id: str):
#     result = ceApp.AsyncResult(task_id)
#     return {"task_id": task_id, "status": result.status, "result": result.result}
#
#
# @app.post("/uploads")
# async def upload_image(files: list[UploadFile] = File(...)):

app.include_router(upload_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
