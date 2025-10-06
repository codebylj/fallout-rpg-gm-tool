from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Vault(Base):
    __tablename__ = "vaults"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vault_number: Mapped[str] = mapped_column(String(255), unique=True)
    status: Mapped[str] = mapped_column(String(255))
    security_level: Mapped[int] = mapped_column(Integer)
    door_status: Mapped[str] = mapped_column(String(255))
    overseer_password: Mapped[str] = mapped_column(String(255))
    entries: Mapped[list["LogEntry"]] = relationship(back_populates="vault",
                                                     cascade="all, delete-orphan")


class LogEntry(Base):
    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(10), nullable=False)
    date: Mapped[str] = mapped_column(String(10))
    population: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(String(255))
    vault_id: Mapped[int] = mapped_column(ForeignKey("vaults.id"))
    vault: Mapped["Vault"] = relationship(back_populates="entries")
