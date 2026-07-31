from fastapi import status


# template response error
class AppException(Exception):
    """Base class buat semua custm error

    Args:
        message (str): pesan error
        status_code (int): status code error (400,401,404,500, etc, default 500)
        error_code (str): kode error custom (ex: "USER_NOT_FOUND", "INVALID_PASSWORD", etc)
        Atrributes:
            message (str): pesan error
            status_code (int): status code error
            error_code (str): kode error custom
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_SERVER_ERROR",
    ):
        self.message = message  # pesan error
        self.status_code = status_code  # status code
        self.error_code = error_code  # kode error
        super().__init__(message)


# 400 validation error
class validationExceptions(AppException):
    """ketika ada validasi yang kurang valid dari sisi client.

    contoh: dari body request gak ada field "name"

    Args:
        message (str): pesan error spesifik. Default "Input tidak valid"
    """

    def __init__(
        self,
        message: str = "Input tidak valid",
    ):
        super().__init__(
            message, status_code=status.HTTP_400_BAD_REQUEST, error_code="BAD_REQUEST"
        )


# 401 unauthorized error
class UnauthorizedException(AppException):
    """ketika user tidak terautentikasi
    Args:
        message (str): pesan error spesifik. Default "Unauthorized"
    """

    def __init__(
        self,
        message: str = "Unauthorized",
    ):
        super().__init__(
            message, status_code=status.HTTP_401_UNAUTHORIZED, error_code="UNAUTHORIZED"
        )


# 403 forbidden error
class ForbiddenException(AppException):
    """ketika user tidak memiliki akses
    Args:
        message (str): pesan error spesifik. Default "Tidak Memiliki Akses"
    """

    def __init__(
        self,
        message: str = "Tidak Memiliki Akses",
    ):
        super().__init__(
            message, status_code=status.HTTP_403_FORBIDDEN, error_code="FORBIDDEN"
        )


# 404 not found error
class NotFoundException(AppException):
    """ketika data atau id tidak ditemukan

    contoh: id user tidak ditemukan
    Args:
        message (str): Pesan error spesifik. Default "Data tidak ditemukan"
    """

    def __init__(
        self,
        message: str = "Data tidak ditemukan",
    ):
        super().__init__(
            message, status_code=status.HTTP_404_NOT_FOUND, error_code="NOT_FOUND"
        )


# 409 conflict error
class ConflictException(AppException):
    """ketika data sudah ada sebelumnya

    contoh: data user sudah ada
    Args:
        message (str): Pesan error spesifik. Default "Data sudah ada"
    """

    def __init__(
        self,
        message: str = "Data sudah ada",
    ):
        super().__init__(
            message, status_code=status.HTTP_409_CONFLICT, error_code="CONFLICT"
        )


# 422 Id reference tidak valid
class InvalidReferenceExceptions(AppException):
    """Dilempar kalau id reference tidak valid/tidak ada

    Args:
        message(str): pesan error spesifik. Default "Id reference tidak valid"
    """

    def __init__(
        self,
        message: str = "Id reference tidak valid",
    ):
        super().__init__(
            message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="UNPROCESSABLE_ENTITY",
        )


# 429 too many request - rate limit
class RateLimitException(AppException):
    """Dilempar kalau request melebihi limit dalam batas waktu tertentu

    Args:
        message(str): pesan error spesifik. Default "Terlalu banyak request, silahkan coba lagi nanti"
    """

    def __init__(
        self,
        message: str = "Terlalu banyak request, silahkan coba lagi nanti",
    ):
        super().__init__(
            message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="TOO_MANY_REQUESTS",
        )


# 500 internal server error
class InternalServerException(AppException):
    """ketika terjadi error server
    Args:
        message (str): pesan error spesifik. Default "Internal server error"
    """

    def __init__(
        self,
        message: str = "Internal server error",
    ):
        super().__init__(
            message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
        )


# 504 gateway timeout - API LLM
class GatewayTimeoutException(AppException):
    """Error ketika layanan pihak ketiga tidak merespon

    Args:
        message(str): pesan error spesifik. Default "Layanan pihak ketiga tidak merespon-API LLM Error"
    """

    def __init__(
        self,
        message: str = "Layanan pihak ketiga tidak merespon-API LLM Error",
    ):
        super().__init__(
            message,
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            error_code="GATEWAY_TIMEOUT",
        )
