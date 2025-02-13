from app.utils.decorators import handle_repository_exceptions
from app.schemas.todo import TodoAddSchema, TodoSchema, TodoUpdateSchema
from app.models.todo import TodosTable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_db
from database import new_session


class TodoRepository:

    @classmethod
    async def _get_todo_by_id(cls, db, todo_id: int) -> TodoSchema:
        """Get todo by ID or None, if not found."""
        query = select(TodosTable).where(TodosTable.id == todo_id)
        result = await db.execute(query)
        todo = result.scalar_one_or_none()
        if todo is None:
            raise ValueError(f"Todo with id {todo_id} does not exist.")
        return todo

    @classmethod
    @handle_repository_exceptions
    async def add_one(cls, data: TodoAddSchema, db: AsyncSession) -> TodoSchema:
        todo_dict = data.model_dump()
        todo = TodosTable(**todo_dict)
        db.add(todo)
        await db.flush()
        await db.commit()
        return TodoSchema.model_validate(todo)

    @classmethod
    @handle_repository_exceptions
    async def update_one(
        cls,
        todo_id: int,
        update_data: TodoUpdateSchema,
        db: AsyncSession,
    ) -> TodoSchema:
        async with new_session() as session:
            todo = await cls._get_todo_by_id(db, todo_id)

            update_values = update_data.model_dump(exclude_unset=True)
            for key, value in update_values.items():
                if value is not None:
                    setattr(todo, key, value)

            await session.flush()
            await session.commit()
            return TodoSchema.model_validate(todo)

    @classmethod
    @handle_repository_exceptions
    async def delete_one(cls, todo_id: int, db: AsyncSession) -> TodoSchema:
        todo = await cls._get_todo_by_id(db, todo_id)

        await db.delete(todo)
        await db.commit()
        return todo

    @classmethod
    @handle_repository_exceptions
    async def find_all(cls, db: AsyncSession) -> list[TodoSchema]:
        query = select(TodosTable)
        result = await db.execute(query)
        todos_models = result.scalars().all()
        todos_schemas = [
            TodoSchema.model_validate(todo_model) for todo_model in todos_models
        ]
        return todos_schemas
