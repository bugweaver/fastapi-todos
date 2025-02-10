from sqlalchemy.exc import SQLAlchemyError

def handle_repository_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            print(f"Database Error in {func.__name__}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected Error in {func.__name__}: {e}")
            raise
    return wrapper