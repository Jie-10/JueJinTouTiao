from fastapi import APIRouter
from fastapi import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from schemas.history import HistoryAddRequest
from services import history as history_service
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix='/api/history', tags=['history'])


@router.post("/add")
async def add_history(
        request: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await history_service.add_history(db, user.id, request.news_id)
    return success_response(message="浏览历史添加成功", data=result)


@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, alias="pageSize", ge=1, le=100),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    histories, total, has_more = await history_service.get_history_list(db, user.id, page, page_size)
    return success_response(
        message="获取浏览历史成功",
        data={"list": histories, "total": total, "hasMore": has_more}
    )


@router.delete("/delete/{news_id}")
async def remove_history(
        news_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # 业务规则（记录不存在时抛业务错误）在 service 层处理
    removed = await history_service.remove_history(db, user.id, news_id)
    return success_response(message="浏览历史删除成功", data={"removed": removed})


@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    removed_count = await history_service.clear_history(db, user.id)
    return success_response(message="浏览历史已清空", data={"removed": removed_count})
