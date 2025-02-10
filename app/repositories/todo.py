from app.utils.decorators import handle_repository_exceptions
from database import new_session
from app.schemas.todo import TodoAddSchema, TodoSchema, TodoUpdateSchema
from app.models.todo import TodosTable
from sqlalchemy import select


class TodoRepository:

    @classmethod
    async def _get_todo_by_id(cls, session, todo_id: int) -> TodoSchema:
        """Get todo by ID or None, if not found."""
        query = select(TodosTable).where(TodosTable.id == todo_id)
        result = await session.execute(query)
        todo = result.scalar_one_or_none()
        if todo is None:
            raise ValueError(f"Todo with id {todo_id} does not exist.")
        return todo

    @classmethod
    @handle_repository_exceptions
    async def add_one(cls, data: TodoAddSchema) -> TodoSchema:
        async with new_session() as session:
            todo_dict = data.model_dump()
            todo = TodosTable(**todo_dict)
            session.add(todo)
            await session.flush()
            await session.commit()
            return TodoSchema.model_validate(todo)

    @classmethod
    @handle_repository_exceptions
    async def update_one(
        cls, todo_id: int, update_data: TodoUpdateSchema
    ) -> TodoSchema:
        async with new_session() as session:
            todo = await cls._get_todo_by_id(session, todo_id)

            update_values = update_data.model_dump(exclude_unset=True)
            for key, value in update_values.items():
                if value is not None:
                    setattr(todo, key, value)

            await session.flush()
            await session.commit()
            return TodoSchema.model_validate(todo)

    @classmethod
    @handle_repository_exceptions
    async def delete_one(cls, todo_id: int) -> TodoSchema:
        async with new_session() as session:
            todo = await cls._get_todo_by_id(session, todo_id)

            await session.delete(todo)
            await session.commit()
            return todo

    @classmethod
    @handle_repository_exceptions
    async def find_all(cls) -> list[TodoSchema]:
        async with new_session() as session:
            query = select(TodosTable)
            result = await session.execute(query)
            todos_models = result.scalars().all()
            todos_schemas = [
                TodoSchema.model_validate(todo_model) for todo_model in todos_models
            ]
            return todos_schemas
