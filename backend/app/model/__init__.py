# file ini buat nampung semua model yang dipakai di aplikasi jdi nnti manggilnya lwt ini

from .conversation_model import Conversation
from .message_model import Message
from .user_model import User

# kenapa perlu import semua model di sini?
# -> Alembic (tool migration) baca Base.metadata buat tau tabel apa aja yang harus dibikin.
# -> Base.metadata cuma "kenal" model yang PERNAH di-import ke memory Python.
# -> Kalau model gak pernah diimport di mana pun, Alembic gak akan lihat tabel itu sama sekali,
#    jadi migration-nya bisa gagal/gak lengkap.

# kenapa ada "# noqa: F401"?
# -> Ruff/linter biasanya komplain "imported but unused" karena User, Conversation, Message
#    gak dipakai langsung di file ini. Padahal justru itu tujuannya (buat di-import ke Alembic).
# -> noqa: F401 artinya "abaikan warning unused-import khusus baris ini"

__all__ = ["Conversation", "Message", "User"]
# __all__ nentuin apa aja yang ikut ke-export kalau ada yang nulis: from model import *
