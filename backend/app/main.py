from contextlib import asynccontextmanager  # buat bikin context manager pakai async def

from fastapi import FastAPI
from sqlalchemy import text  # buat nulis raw SQL query

from app.config.database import engine  # engine koneksi ke database (dari database.py)


# lifespan = kode yang jalan saat app start & saat app mati (startup & shutdown)
@asynccontextmanager
async def lifeSpan(app: FastAPI):
    # -- startup --
    # bagian ini jalan sekali pas aplikasi pertama kali nyala
    try:
        async with engine.begin() as conn:  # buka koneksi ke database
            await conn.execute(
                text("SELECT 1")
            )  # test query simpel buat cek koneksi hidup
            print("Connected to database")
    except Exception as e:
        # kalau gagal connect, tampilkan errornya biar gampang debug
        print("Failed to connect to database:", {e})
        raise  # lempar lagi errornya biar app berhenti (nggak jalan tanpa DB)

    yield  # <- di titik ini aplikasi mulai jalan (nerima request2), sampai app dimatikan

    # -- shutdown --
    # bagian ini jalan sekali pas aplikasi dimatikan (Ctrl+C / server stop)
    await engine.dispose()  # tutup semua koneksi database dengan rapi
    print("Database connection closed")


# bikin instance aplikasi FastAPI, daftarkan lifeSpan biar startup/shutdown-nya kepakai
app = FastAPI(lifespan=lifeSpan)


# -- route/endpoint dasar --
# akses ke "/" bakal manggil fungsi ini
@app.get("/")
async def root():
    return {"message": "Hello World"}
