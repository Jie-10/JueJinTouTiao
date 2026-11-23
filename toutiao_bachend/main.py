from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册异常处理器
register_exception_handlers(app)


# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有域名
    allow_credentials=True, # 允许跨域请求携带认证信息cookies
    allow_methods=["*"], # 允许所有请求方法
    allow_headers=["*"], # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 挂载新闻路由
app.include_router(news.router)

app.include_router(users.router)

app.include_router(favorite.router)

app.include_router(history.router)
