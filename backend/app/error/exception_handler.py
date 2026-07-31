from datetime import datetime, timezone

from error.exceptions import AppException
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.setting import settings


def _build_exceptions_response(
    status_code: int, error_code: str, message: str, detail: str | None = None
) -> JSONResponse:
    """Membuat response error sesuai format errornya

    Format hasilnya: { status, response_code, public_id, error_code, message, timestamp, data }

        detail cuma dimasukin kalau DEBUG=True (mode development).
        Di production, detail teknis (misal traceback/error asli) DISEMBUNYIKAN biar gak bocorin
        informasi sensitif ke client.

        Args:
            message (str): pesan error
            status_code (int): status code error (400,401,404,500, etc, default 500)
            error_code (str): kode error custom (ex: "USER_NOT_FOUND", "INVALID_PASSWORD", etc)
            detail (str | None): Detail teknis tambahan (traceback, raw error).
            Cuma ditampilkan kalau DEBUG=True. Default None.

        Returns:
            JSONResponse: Response FastAPI siap dikirm ke client
    """
    body = {
        "status": "error",
        "response_code": status_code,
        "public_id": None,
        "error_code": error_code,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": None,
    }

    # detail teknis cuma muncul di mode development, biar gampang di debug

    if settings.DEBUG:
        body["detail"] = detail

    return JSONResponse(status_code=status_code, content=body)


def register_exception_handler(app: FastAPI) -> None:
    """Register exception handler ke instance FastAPI

    dipanggil sekali aja di main.py (entry point aplikasi/server)
    Args:
        app (FastAPI): instance FastAPI yg akan di register exception handler
    """

    # --- 1. Handler buat semua exceptions (AppException & turunnya)
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Tangkap semua custom exceptionya

        Args:
            request (Request): request yang lagi diproses saat terjadi exception
            exc (AppException): instance exception yang terjadi atau di raise dari handler lain

        Returns:
            JSONResponse: response error sesuai format errornya
        """
        return _build_exceptions_response(
            status_code=exc.status_code,
            error_code=exc.error_code,
            message=exc.message,
            detail=exc.detail,
        )

    # --- 2. Handler buat error validasi otomatis dari Pydantic/FastAPI
    # ini kejadian misal: field wajib gak diisi, tipe data salah (kirim string padahal harus int)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Tangkap error validasi otomatis dari Pydantic (field kosong, tipe salah, dst).

        Args:
            request (Request): request yang lagi diproses saat terjadi exception
            exc (RequestValidationError): Error validasi otomatis dari Pydantic/FastAPI

        Returns:
            JSONResponse: response error sesuai format errornya 400(Bad Request)
        """
        errors = exc.errors()
        first_error = errors[0] if errors else {}
        field = ".".join(
            str(loc) for loc in first_error.get("loc", []) if loc != "body"
        )
        reason = first_error.get("msg", "Input tidak valid")

        message = f"field: {field} " if field else reason

        return _build_exceptions_response(
            status_code=exc.HTTP_400_BAD_REQUEST,
            error_code="HTTP_EXCEPTION",
            message=message,
            detail=str(
                exc
            ),  # detail lengkap semua field yang error, cuma muncul di DEBUG
        )

    # --- 3. Handler buat HTTPException bawaan Starlette/FastAPI ---
    # ini kejadian kalau ada yang manggil raise HTTPException(status_code=..., detail=...) langsung
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Tangkap HTTPException bawaan FastAPI/Starlette (bukan custom exception kita).

        Args:
            request (Request): Request yang lagi diproses saat error terjadi.
            exc (StarletteHTTPException): HTTPException bawaan, biasanya dari raise manual
                atau dari internal FastAPI sendiri.

        Returns:
            JSONResponse: Response error sesuai status_code dari HTTPException-nya.
        """
        return _build_exceptions_response(
            status_code=exc.status_code,
            error_code="HTTP_ERROR",
            message=str(exc.detail),
        )

    # --- 4. Handler buat error yang GAK TERDUGA sama sekali (bug, exception tak terhandle) ---
    # ini "jaring pengaman" terakhir, nangkep semua Exception yang lolos dari handler di atas
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Jaring pengaman terakhir buat error tak terduga (bug, exception tak terhandle).

        PENTING: di production, JANGAN pernah kirim str(exc) mentah ke client,
        karena bisa bocorin detail internal (query SQL, path file, dll).

        Args:
            request (Request): Request yang lagi diproses saat error terjadi.
            exc (Exception): Exception apapun yang lolos dari 3 handler sebelumnya.

        Returns:
            JSONResponse: Response error generik dengan status 500.
        """
        # PENTING: di production, JANGAN pernah kirim str(exc) ke client
        # karena bisa bocorin detail internal (query SQL, path file, dll)
        message = str(exc) if settings.DEBUG else "Terjadi kesalahan pada server"

        return _build_exceptions_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
            message=message,
            detail=repr(exc),  # traceback singkat, cuma muncul di DEBUG
        )
