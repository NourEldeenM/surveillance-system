from database import engine, Base
from models.user import User  # Ensure you import all models
# Create tables in the database
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")