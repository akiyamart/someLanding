from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.models import UserCreate, DeletedUserResponse, ShowUser
from src.db.dals import UserDAL
from src.db.session import get_db 


user_router = APIRouter()

async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session: 
        async with session.begin(): 
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name = body.name,
                surname = body.surname,
                email = body.email,
            )
            return ShowUser(
                user_id = user.user_id,
                name = user.name, 
                surname = user.surname, 
                email = user.email, 
                is_active = user.is_active,
            )
    
async def _delete_user(user_id, db):
    async with db as session: 
        async with session.begin(): 
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return deleted_user_id
        
@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser: 
    return await _create_new_user(body, db)

@user_router.delete("/", response_model=DeletedUserResponse)
async def delete_user(user_id: UUID): 
    pass