from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from connect import get_async_session
from src.contacts.enums import SearchParams
from src.contacts.schemas import ContactSchema, ContactResponceSchema
from src.contacts import repository as contacts_repository


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post('/', response_model=ContactResponceSchema)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_async_session)):
    return await contacts_repository.create_contact(body, db)


@router.get('/', response_model=list[ContactResponceSchema])
async def read_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    return await contacts_repository.get_contacts(skip, limit, db)


@router.get('/{contact_id}', response_model=ContactResponceSchema)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    return await contacts_repository.get_contact_by_id(contact_id, db)


@router.put('/{contact_id}', response_model=ContactResponceSchema)
async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession = Depends(get_async_session)):
    contact = await contacts_repository.update_contact(contact_id, body, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact


@router.delete('/{contact_id}', response_model=ContactResponceSchema)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    contact = await contacts_repository.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get('/search/', response_model=list[ContactResponceSchema])
async def search_contact(param: SearchParams, value: str, db: AsyncSession = Depends(get_async_session)):
    contact = await contacts_repository.search_contact(param, value, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact


@router.get('/birthday/', response_model=list[ContactResponceSchema])
async def birthday_contact(db: AsyncSession = Depends(get_async_session)):
    return await contacts_repository.get_upcoming_birthdays(db)
