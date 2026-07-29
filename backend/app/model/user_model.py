import uuid  # buat generate UUID
from datetime import datetime  # buat timestamp

from sqlalchemy import DateTime, Enum, String, func  # buat tipe column dan fucntion SQL
from sqlalchemy.orm import (  # cara orm modern SQLALCHEMY nulis kolom + tipe data
    Mapped,
    mapped_column,
)

from app.config.database import Base  # import Base class dari database.py


# model class User
class User(Base):
    __tablename__ = "User"  # nama tabel di DB

    # primary Key yg dipake oleh internal server
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,  # buat primary key
        default=uuid.uuid7,  # generate UUID otomatis
    )

    # public id yang dipake oleh client
    public_id: Mapped[uuid.UUID] = mapped_column(
        unique=True,  # buat unique
        default=uuid.uuid4,  # generate UUID otomatis
        nullable=False,  # wajib ada
    )

    # email user
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,  # wajib ada
        unique=True,  # buat unique
    )

    # password user
    password: Mapped[str | None] = mapped_column(
        String,
        nullable=True,  # opsional karena ad oauth
    )

    # name
    name: Mapped[str | None] = mapped_column(
        String,
        nullable=True,  # boleh null
    )

    # avatar_url
    avatar_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,  # boleh null
    )

    # auth provider
    auth_provider: Mapped[str] = mapped_column(
        Enum("email", "google", name="auth_provider_enum"),
        nullable=False,
    )

    # id google auth
    google_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,  # boleh null
    )

    # created_at
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # updated_at
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
