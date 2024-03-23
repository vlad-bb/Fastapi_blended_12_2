from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, and_, or_

from src.contacts.models import Contact
from src.contacts.schemas import ContactSchema


async def create_contact(body: ContactSchema, db: AsyncSession) -> Contact:
    contact = Contact(
        name=body.name,
        second_name=body.second_name,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        address=body.address
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def get_contacts(skip: int, limit: int, db: AsyncSession):
    contacts = await db.execute(select(Contact).offset(skip).limit(limit))
    return contacts.scalars().all()


async def get_contact_by_id(contact_id: int, db: AsyncSession):
    contact = await db.get(Contact, contact_id)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession) -> Contact | None:
    contact = await db.get(Contact, contact_id)
    if contact:
        contact.name = body.name
        contact.second_name = body.second_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.address = body.address
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession) -> Contact | None:
    contact = await db.get(Contact, contact_id)
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contact(param: str, value: str, db: AsyncSession):
    filter_criteria = {
        'id': Contact.id,
        'name': Contact.name,
        'second_name': Contact.second_name,
        'email': Contact.email,
        'phone': Contact.phone,
    }
    contact = await db.execute(select(Contact).filter(filter_criteria[param].like(f"%{value}%")))
    return contact.scalars().all()


async def get_upcoming_birthdays(db: AsyncSession):
    current_date = datetime.now().date()
    next_week = current_date + timedelta(days=7)
    current_month = current_date.month
    next_month = (current_month % 12) + 1
    query = select(Contact).where(
        or_(
            and_(
                extract('month', Contact.birthday) == current_date.month,
                extract('day', Contact.birthday).between(current_date.day, 31)
            ),
            and_(
                extract('month', Contact.birthday) == next_month,
                extract('day', Contact.birthday).between(1, next_week.day)
            )
        )
    )
    contacts = await db.execute(query)
    return contacts.scalars().all()
