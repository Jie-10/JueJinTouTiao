import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status


# 开发模式：返回详细错误信息
# 生产模式：返回简化信息错误
DEBUG_MODE = True  # 教学项目保持开启


# 业务层面的异常处理
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )

# 数据库完整性约束错误
async def integrity_error_handler(request: Request, exc: IntegrityError):

    error_msg = str(exc.orig)

    # 判断具体的约束错误类型
    if 'username_UNIQUE' in error_msg or 'Duplicate entry' in error_msg:
        detail = "用户名已存在"
    elif 'FOREIGN KEY' in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    # 开发模式下返回详细信息错误
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_msg": error_msg,
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data,
        },
    )

# SQLAlchemy数据库错误
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    error_msg = str(exc)
    detail = "数据库操作失败，请检查输入"

    # 开发模式下返回详细信息错误
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_msg": str(exc),
            "traceback": traceback.format_exc(), # 格式化异常信息为字符串，方便日志记录和调试
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": detail,
            "data": error_data,
        },
    )

# 处理所有未捕获的异常
async def uncaught_exception_handler(request: Request, exc: Exception):

    error_msg = str(exc)
    detail = "服务器错误，请检查输入"

    # 开发模式下返回详细信息错误
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_msg": error_msg,
            "traceback": traceback.format_exc(), # 格式化异常信息为字符串，方便日志记录和调试
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": detail,
            "data": error_data,
        },
    )
