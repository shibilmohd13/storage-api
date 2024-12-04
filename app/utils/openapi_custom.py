from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    """
    Customize the OpenAPI schema to include ExampleHeader.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "ExampleHeaderAuth": {
            "type": "apiKey",
            "name": "ExampleHeader",
            "in": "header",
        }
    }
    openapi_schema["security"] = [{"ExampleHeaderAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
