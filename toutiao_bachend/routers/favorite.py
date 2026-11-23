from fastapi import APIRouter
from fastapi import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
from services import favorite as favorite_service
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix='/api/favorite', tags=['favorite'])


@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    is_favorite = await favorite_service.check_favorite(db, user.id, news_id)
    return success_response(message="Favorite check successful", data=FavoriteCheckResponse(is_favorite=is_favorite))


@router.post("/add")
async def add_favorite(
        request: FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite_service.add_favorite(db, user.id, request.news_id)
    return success_response(message="Favorite added successfully", data=result)


@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # 业务规则（未收藏时抛业务错误）在 service 层处理
    removed = await favorite_service.remove_favorite(db, user.id, news_id)
    return success_response(message="Favorite removed successfully", data={"removed": removed})


@router.get("/list")
async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, alias="pageSize", ge=1, le=100),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    favorites, total, has_more = await favorite_service.get_favorite_list(db, user.id, page, page_size)
    return success_response(
        message="获取收藏列表成功",
        data={"list": favorites, "total": total, "hasMore": has_more}
    )


@router.delete("/clear")
async def clear_favorites(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    removed_count = await favorite_service.clear_favorites(db, user.id)
    return success_response(message="收藏列表已清空", data={"removed": removed_count})
