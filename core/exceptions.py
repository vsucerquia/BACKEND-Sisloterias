
class AppException(Exception):
    """Excepción base de la aplicación."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Recurso no encontrado."""

    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, 404)


class ConflictException(AppException):
    """Conflicto de datos."""

    def __init__(self, message: str = "Conflicto en los datos"):
        super().__init__(message, 409)


class BadRequestException(AppException):
    """Solicitud inválida."""

    def __init__(self, message: str = "Solicitud incorrecta"):
        super().__init__(message, 400)


class UnauthorizedException(AppException):
    """No autenticado o credenciales inválidas."""

    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, 401)
