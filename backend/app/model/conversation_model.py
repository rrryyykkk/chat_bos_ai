import uuid  # buat generate UUID
from datetime import datetime  # buat timestamp

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    func,
)  # buat tipe column dan fucntion SQL
from sqlalchemy.orm import (  # cara orm modern SQLALCHEMY nulis kolom + tipe data
    Mapped,
    mapped_column,
    relationship,
)

from app.config.database import Base  # import Base class dari database.py
from app.model.message_model import Message


class Conversation(Base):
    __tablename__ = "Conversation"

    # primary key
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid7,
    )
    # public id
    public_id: Mapped[uuid.UUID] = mapped_column(
        unique=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # ForeignKey ke tabel users.id -> nunjukin conversation ini punya siapa
    # ondelete="CASCADE" -> kalau user-nya dihapus, semua conversation dia ikut kehapus otomatis
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # nullable=True karena title auto-generate dari pesan pertama, jadi pas dibuat masih kosong
    title: Mapped[str | None] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationship (BUKAN kolom database, cuma "jembatan" di Python)
    # satu conversation -> punya banyak messages
    # back_populates -> nyambung ke relationship "conversation" di model Message (dua arah)
    # cascade "all, delete-orphan" -> kalau conversation dihapus, semua message-nya ikut kehapus
    message: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )
