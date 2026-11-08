from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60))
    role: Mapped[str] = mapped_column(
        String(20), 
        default="requester", 
        server_default="requester"
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="user", 
        passive_deletes="all"
    )

    __table_args__ = (
        CheckConstraint("length(trim(first_name)) > 0", name="ck_users_first_name"),
        CheckConstraint("length(trim(last_name)) > 0", name="ck_users_last_name"),
        CheckConstraint("role IN ('requester', 'staff')", name="ck_users_role"),
        UniqueConstraint("first_name", "last_name", name="uq_users_first_name_last_name"),
    )

class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="service", 
        passive_deletes="all"
    )

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="ck_services_name"),
    )

class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT")
    )
    file_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str | None] = mapped_column(String(36), unique=True)
    color_mode: Mapped[str] = mapped_column(String(10))
    copies: Mapped[int] = mapped_column(default=1, server_default="1")
    paper_type: Mapped[str] = mapped_column(String(50))
    paper_size: Mapped[str] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20), default="waiting", server_default="waiting"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    printing_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint("length(trim(file_name)) > 0", name="ck_tickets_file_name"),
        CheckConstraint(r"stored_name ~ '^[0-9a-f]{32}\.pdf$'", name="ck_tickets_stored_name"),
        CheckConstraint("color_mode IN ('Grayscale', 'Colored')", name="ck_tickets_color_mode"),
        CheckConstraint("copies BETWEEN 1 AND 100", name="ck_tickets_copies"),
        CheckConstraint(
            "paper_type IN ('Bond Paper', 'Photo Paper', 'Sticker Paper', 'Cardstock')",
            name="ck_tickets_paper_type",
        ),
        CheckConstraint("paper_size IN ('Short', 'A4', 'Long')", name="ck_tickets_paper_size"),
        CheckConstraint("notes IS NULL OR length(notes) <= 300", name="ck_tickets_notes"),
        CheckConstraint(
            "status IN ('waiting', 'printing', 'ready', 'done', 'cancelled')",
            name="ck_tickets_status",
        ),
        CheckConstraint(
            "printing_at IS NULL OR printing_at >= created_at",
            name="ck_tickets_printing_at_after_created",
        ),
        CheckConstraint(
            "ready_at IS NULL OR ready_at >= created_at",
            name="ck_tickets_ready_at_after_created",
        ),
        CheckConstraint(
            "finished_at IS NULL OR finished_at >= created_at",
            name="ck_tickets_finished_at_after_created",
        ),
        Index(
            "uq_tickets_one_printing",
            "service_id",
            unique=True,
            postgresql_where=text("status = 'printing'"),
        ),
    )