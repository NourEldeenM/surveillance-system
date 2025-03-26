from fastapi import FastAPI
from .exception_handlers import (
    duplicate_email_exception_handler,
    database_error_exception_handler,
    not_found_exception_handler,
    validation_error_exception_handler,
)
from .exceptions import (
    DuplicateEmailError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DuplicateEmailError, duplicate_email_exception_handler)
    app.add_exception_handler(DatabaseError, database_error_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(ValidationError, validation_error_exception_handler)