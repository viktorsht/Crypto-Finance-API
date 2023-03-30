from typing import List
from asyncio import gather
from fastapi import APIRouter, HTTPException
from servicos import AssetService, UserService, FavoriteService
from schemas import DaySummaryOutput, UserCreateInput,StandartOutput, ErrorOutput, UserFavoriteAddInput, UserListOutput

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')

@user_router.post('/create', response_model=StandartOutput, responses={400 : {'model' : ErrorOutput}})
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)
        return StandartOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.delete('/delete/{user_id}', response_model=StandartOutput, responses={400 : {'model' : ErrorOutput}})
async def user_delete(user_id:int):
    try:
        await UserService.delete_user(user_id)
        return StandartOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@user_router.post('/favorite/add', response_model=StandartOutput, responses={400 : {'model' : ErrorOutput}})
async def user_favorite_add(favorite_add: UserFavoriteAddInput):
    try:
        await FavoriteService.add_favorite(user_id=favorite_add.user_id, symbol=favorite_add.symbol)
        return StandartOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@user_router.delete('/favorite/remove/{user_id}', response_model=StandartOutput, responses={400 : {'model' : ErrorOutput}})
async def user_favorite_remove(user_id:int, symbol: str):
    try:
        await FavoriteService.remove_favorite(user_id=user_id, symbol=symbol)
        return StandartOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.get('/list', response_model=List[UserListOutput], responses={400: {'model': ErrorOutput}})
async def user_list():
    try:
        return await UserService.list_user()
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@assets_router.get('/day_summary/{user_id}', response_model=List[DaySummaryOutput], responses={400: {'model': ErrorOutput}})
async def day_summary(user_id:int):
    try:
        user = await UserService.get_user_id(user_id)
        favorites_symbols = [favorite.symbol for favorite in user.favorites]
        response = []
        tasks = [AssetService.day_summary(symbol=symbol) for symbol in favorites_symbols]
        return await gather(*tasks)
    except Exception as error:
        raise HTTPException(400, detail=str(error))