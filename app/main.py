# app/main.py
from fastapi import FastAPI
from app.api import vault_routes, booking_routes, storage_routes
from app.database import engine
from app.models import vault_model, storage_model, booking_model
from app.middleware.token_middleware import TokenMiddleware


# Create database tables
vault_model.Base.metadata.create_all(bind=engine)
storage_model.Base.metadata.create_all(bind=engine)
booking_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Storage API", description="API for Storage Vault Bookings")

# Add middleware
app.add_middleware(TokenMiddleware)


# Include routers
app.include_router(vault_routes.router, prefix="/vaults", tags=["vaults"])
app.include_router(booking_routes.router, prefix="/bookings", tags=["bookings"])
app.include_router(storage_routes.router, prefix="/storages", tags=["storages"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Storage API"}