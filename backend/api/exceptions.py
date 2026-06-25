from fastapi import HTTPException


class NovaQureException(HTTPException):
    """
    Base application exception.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ):

        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "error": {
                    "code": code,
                    "message": message,
                },
            },
        )


class NotFoundException(
    NovaQureException,
):
    def __init__(
        self,
        resource: str,
    ):

        super().__init__(
            404,
            "NOT_FOUND",
            f"{resource} not found.",
        )


class DuplicateException(
    NovaQureException,
):
    def __init__(
        self,
        resource: str,
    ):

        super().__init__(
            400,
            "DUPLICATE_RESOURCE",
            f"{resource} already exists.",
        )


class ValidationException(
    NovaQureException,
):
    def __init__(
        self,
        message: str,
    ):

        super().__init__(
            400,
            "VALIDATION_ERROR",
            message,
        )
