from fastapi.responses import JSONResponse
from fastapi import status


async def status_ok(detail):
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": detail})


async def status_error_401(detail):
    
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": detail})