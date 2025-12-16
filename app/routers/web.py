from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/web",
    tags=["web"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/temp2", response_class=HTMLResponse)
async def temp2(request: Request):
    return templates.TemplateResponse("version2.html", {"request": request})
    
@router.get("/temp3", response_class=HTMLResponse, include_in_schema=False)
async def temp3(request: Request):
    return templates.TemplateResponse("version3.html", {"request": request})

@router.get("/temp4", response_class=HTMLResponse, include_in_schema=False)
async def temp4(request: Request):
    return templates.TemplateResponse("version4.html", {"request": request})

@router.get("/temp5", response_class=HTMLResponse, include_in_schema=False)
async def temp5(request: Request):
    return templates.TemplateResponse("version5.html", {"request": request})