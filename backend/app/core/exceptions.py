from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detalle: str = "Recurso no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detalle)


class ForbiddenError(HTTPException):
    def __init__(self, detalle: str = "No autorizado"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detalle)


class ConflictError(HTTPException):
    def __init__(self, detalle: str = "Conflicto"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detalle)


class BadRequestError(HTTPException):
    def __init__(self, detalle: str = "Solicitud inválida"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detalle)


class UnauthorizedError(HTTPException):
    def __init__(self, detalle: str = "No autenticado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detalle,
            headers={"WWW-Authenticate": "Bearer"},
        )
