from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    birthday: Mapped[date] = mapped_column()
    address: Mapped[str] = mapped_column(nullable=True)
