from sqlalchemy.ext.asyncio import (
    AsyncSession,  # class buat bikin "sesi" komunikasi ke database secara async
    async_sessionmaker,  # "pabrik" buat generate AsyncSession baru tiap dibutuhkan
    create_async_engine,  # fungsi buat bikin engine (koneksi pool ke database)
)
from sqlalchemy.orm import (
    DeclarativeBase,
)  # class dasar yang di-inherit semua model tabel (User, dll)

from app.config.setting import settings  # object berisi semua env variable dari .env


# -- Base Class --
# semua model nanti inherit dari class ini
class Base(DeclarativeBase):
    pass


# -- engine --
# engine buat komunikasi ke database
engine = create_async_engine(
    settings.DATABASE_URL,  # string koneksi ke database
    echo=settings.DEBUG,  # untuk menampilkan perintah SQL di terminal
    future=True,
)


# session factory
# sistem pooling yg berguna untuk membuat sesi baru tiap dibutuhkan,
# Session = "obrolan" sementara ke DB buat satu request (buka - query - commit/rollback - tutup)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,  # session ini nanti pakai koneksi dari "engine" yang sudah dibuat sebelumnya
    class_=AsyncSession,  # tipe session yang dipakai = AsyncSession (yang tadi di-import)
    expire_on_commit=False,  # NONAKTIFKAN auto-expire, object masih bisa diakses setelah commit tanpa query ulang
    autoflush=False,  # NONAKTIFKAN auto-flush, flush cuma jalan kalau manual panggil commit()/flush()
)


# dependency buat FastAPI
# dipakai di router lewat: db: AsyncSession = Depends(get_db)
# catatan: ini try/finally, BUKAN try/except (catch) — finally selalu jalan baik sukses maupun error
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
