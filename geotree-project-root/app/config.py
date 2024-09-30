import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:admin@geotree/postgis")
    REDIS_URL = os.getenv("REDIS_URL", "redis://admin:admin@redis:6379/0")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
