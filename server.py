import uvicorn
from fastapi import FastAPI
from app.routes.todo import router as todo_router

app = FastAPI()
app.include_router(todo_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True)
