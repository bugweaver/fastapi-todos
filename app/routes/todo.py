from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoSchema, TodoAddSchema, TodoUpdateSchema

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter(prefix="/todos", tags=["Todo"])


@router.get("/", response_model=List[TodoSchema])
async def get_todos(db: AsyncSession = Depends(get_db)) -> list[TodoSchema]:
    try:
        todos = await TodoRepository.find_all(db)
        return todos
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve todos")


@router.post("/", response_model=TodoSchema, status_code=201)
async def post_todo(
    todo: TodoAddSchema, db: AsyncSession = Depends(get_db)
) -> TodoSchema:
    try:
        todo = await TodoRepository.add_one(todo, db)
        return todo
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create todo")


@router.patch("/{todo_id}", response_model=TodoSchema)
async def patch_todo(
    todo_id: int, todo: TodoUpdateSchema, db: AsyncSession = Depends(get_db)
) -> TodoSchema:
    try:
        todo = await TodoRepository.update_one(todo_id, todo, db)
        return todo
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update todo")


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)) -> None:
    try:
        deleted = await TodoRepository.delete_one(todo_id, db)
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete todo")
