from core.database import engine, Base
from models.user import User  # Ensure you import all models
from models.branch import Branch
from models.region import Region
from models.admin import Admin
from models.branch_admin import BranchAdmin
from models.staff import Staff

# Create tables in the database
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")