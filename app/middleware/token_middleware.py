from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # List of paths that should be exempt from token checking
        exempt_paths = [
            "/docs", 
            "/openapi.json", 
            "/redoc"
        ]
        
        # Skip token check for exempt paths
        if request.url.path in exempt_paths:
            return await call_next(request)
        
        # Check for token in Authorization header
        auth_header = request.headers.get("ExampleHeader")
        
        if not auth_header:
            # Return a JSONResponse instead of raising HTTPException
            return JSONResponse(
                status_code=401, 
                content={
                    "status": "error",
                    "message": "Missing Authorization token"
                }
            )
        
        # Basic check - ensure the token is present and in correct format
        if not auth_header.startswith("Bearer "):
            # Return a JSONResponse for invalid token format
            return JSONResponse(
                status_code=401, 
                content={
                    "status": "error",
                    "message": "Invalid token format"
                }
            )
        
        # If we've made it this far, the token is present
        return await call_next(request)