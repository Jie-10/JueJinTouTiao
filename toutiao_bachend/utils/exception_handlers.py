from fastapi import HTTPException
from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, uncaught_exception_handler
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def register_exception_handlers(app):
        """注册异常处理程序"""
        app.add_exception_handler(HTTPException, http_exception_handler) # 业务层面的异常处理
        app.add_exception_handler(IntegrityError, integrity_error_handler) # 数据库完整性约束错误
        app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler) # SQLAlchemy数据库错误
        app.add_exception_handler(Exception, uncaught_exception_handler)# 其他未捕获的异常
