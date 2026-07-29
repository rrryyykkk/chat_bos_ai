import uuid

from backend.app.model.conversation_model import Conversation
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Message(Base):
    __tablename__ = "Message"

    # id primary key
    id: Mapped[uuid.uuid7] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # public id
    public_id: Mapped[uuid.UUID] = mapped_column(
        unique=True,
        default=uuid.uuid4,
        nullable=False,
    )
    # id user
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    # ForeignKey ke conversations.id -> pesan ini masuk ke percakapan yang mana
    # ondelete="CASCADE" -> kalau conversation dihapus, semua message di dalamnya ikut kehapus
    conservation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conservation.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Text dipakai (bukan String) karena isi pesan bisa panjang, gak dibatasi jumlah karakter
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # nullable=True karena token usage cuma keisi buat message dari assistant (bukan dari user)
    input_token: Mapped[int | None] = mapped_column(int, nullable=True)
    output_token: Mapped[int | None] = mapped_column(int, nullable=True)

    # gak ada updated_at, karena message sifatnya sekali kirim, gak pernah diedit setelahnya
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # relationship (BUKAN kolom database, cuma "jembatan" di Python)
    # banyak message -> balik ke satu conversation (kebalikan dari relationship di Conversation)
    conservation: Mapped["Conversation"] = relationship(back_populates="message")
