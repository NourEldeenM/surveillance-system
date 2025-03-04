from app.core.database import engine, Base
from app.models.user import User  # Ensure you import all models
from app.models.branch import Branch
from app.models.region import Region
from app.models.admin import Admin
from app.models.branch_admin import BranchAdmin
from app.models.staff import Staff

# Create tables in the database
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")