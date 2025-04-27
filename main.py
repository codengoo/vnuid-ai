from fastapi import FastAPI
app = FastAPI()
from routes.train import router as upload_router

app.include_router(upload_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
