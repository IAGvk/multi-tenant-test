from sqlalchemy.ext.declarative import as_declarative, declared_attr
import importlib

@as_declarative()
class Base:
    id: int
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Dynamically import all models to register them with Base
def import_models():
    importlib.import_module("app.models.user")  # Import the User model
    # Add other models here as needed

import_models()