from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoSchema, TodoAddSchema, TodoUpdateSchema

router = APIRouter(prefix="/api/todos", tags=["Todo"])


@router.get("/")
async def get_todos() -> list[TodoSchema]:
    try:
        todos = await TodoRepository.find_all()
        return todos
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve todos")


@router.post("/")
async def post_todo(todo: Annotated[TodoAddSchema, Depends()]) -> TodoSchema:
    try:
        todo = await TodoRepository.add_one(todo)
        return todo
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create todo")


@router.patch("/{todo_id}")
async def patch_todo(
    todo_id: int, todo: Annotated[TodoUpdateSchema, Depends()]
) -> TodoSchema:
    try:
        todo = await TodoRepository.update_one(todo_id, todo)
        return todo
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update todo")


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int) -> TodoSchema:
    try:
        deleted = await TodoRepository.delete_one(todo_id)
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete todo")
