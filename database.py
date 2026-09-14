from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Boolean, DateTime, Text
from datetime import datetime
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    log_channel: Mapped[str | None] = mapped_column(String, nullable=True)
    tz: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(BigInteger, index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    actor_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    target_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw: Mapped[str | None] = mapped_column(Text, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
