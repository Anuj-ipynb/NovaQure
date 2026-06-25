from typing import Any

from fastapi.responses import JSONResponse


def success_response(
    data: Any,
    status_code: int = 200,
):
    """
    Standard success response.

    Example:

    {
        "success": true,
        "data": {...}
    }
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data,
        },
    )


def error_response(
    code: str,
    message: str,
    status_code: int,
):
    """
    Standard error response.

    Example:

    {
        "success": false,
        "error": {
            "code": "...",
            "message": "..."
        }
    }
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
        },
    )
