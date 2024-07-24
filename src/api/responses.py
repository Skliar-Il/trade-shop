from fastapi.responses import JSONResponse
from fastapi import status


async def status_ok(detail: str):
    
    if detail:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": detail})
    
    return JSONResponse(status_code=status.HTTP_200_OK)


async def status_error_401(detail):
    
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": detail})

async def status_error_500(detail):
    
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": detail})

async def status_error_404():
    
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": "error", 
                                                                        "detail": "not found"})