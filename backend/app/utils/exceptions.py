class DuplicateEmailError(Exception):
    """Raised when a duplicate email is detected in the database."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email '{email}' already exists.")

class DatabaseError(Exception):
    """Raised when a generic database error occurs."""
    def __init__(self, detail: str = "A database error occurred."):
        self.detail = detail
        super().__init__(detail)

class NotFoundError(Exception):
    """Raised when a requested resource is not found."""
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with ID '{identifier}' not found.")

class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, detail: str = "Invalid input data."):
        self.detail = detail
        super().__init__(detail)
        
class UnauthorizedError(Exception):
    """Raised when unauthorized request is made."""
    def __init__(self, detail: str = "Unauthorized"):
        self.detail = detail
        super().__init__(detail)