from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

print("Database and tables created successfully!")
