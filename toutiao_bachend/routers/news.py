from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from services import news as news_service
from utils.response import success_response

# 创建一个 APIRouter 实例
# prefix:路由前缀（API接口规范文档）
# tags:路由分组标签
router = APIRouter(prefix="/api/news", tags=["news"])

# 接口实现流程
# 1. 模块化路由 --> API接口规范文档
# 2. 定义模型类 --> 数据库表（数据库设计文档）
# 3. crud 层封装数据库操作，service 层封装业务逻辑（含缓存策略）
# 4. 路由处理函数调用 service，统一用 success_response 响应结果


@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    news_category = await news_service.get_categories(db, skip, limit)
    return success_response(message="获取新闻分类成功", data=news_category)


@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, alias="pageSize", ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    # 分页换算、缓存策略、总量统计、是否还有更多均在 service 层完成
    news_list, total, has_more = await news_service.get_news_list(db, category_id, page, page_size)
    return success_response(
        message="获取新闻列表成功",
        data={
            'list': news_list,
            'total': total,
            'hasMore': has_more,
        }
    )


@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    # 查询详情 + 浏览量+1 + 相关新闻的编排在 service 层完成
    news_detail = await news_service.get_news_detail(db, news_id)
    return success_response(message="获取新闻详情成功", data=news_detail)
