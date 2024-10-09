from fastapi import HTTPException

class Unauthorized(HTTPException):
    status_code=401
    detail="Не авторизован"
