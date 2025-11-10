# src/backend/routers/__init__.py
import importlib
import pkgutil
from pathlib import Path
from fastapi import FastAPI

def auto_discover_routers(app: FastAPI):
    """Auto-discover all routers in this package"""
    routers_dir = Path(__file__).parent
    
    for module_info in pkgutil.iter_modules([str(routers_dir)]):
        if not module_info.name.startswith("_") and module_info.name.endswith("routers"):
            try:
                module = importlib.import_module(f".{module_info.name}", __package__)
                if hasattr(module, "router"):
                    app.include_router(module.router)
                    print(f"✅ Registered router: {module_info.name}")
            except Exception as e:
                print(f"❌ Failed to register {module_info.name}: {e}")

# Manual export for explicit control
from .get_routers import router as get_router
from .post_routers import router as post_router
from .projects import router as projects_router
from .landowner import router as landowner_router
from .associate_business import router as associate_business_router

__all__ = [
    "get_router", 
    "post_router", 
    "projects_router", 
    "landowner_router", 
    "associate_business_router"
]