from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message:str = "Success", data = None):
    content = {
            "code": 200,
            "message": message,
            "data": data
    }
    # 将内容转换为JSON响应
    return JSONResponse(content=jsonable_encoder(content))
