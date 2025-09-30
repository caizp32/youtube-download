from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from yt_dlp import YoutubeDL

app = FastAPI()
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="templates")

def download_youtube(url: str) -> str:
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,  # 不下载整个播放列表
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download")
async def download(url: str = Form(...)):
    try:
        file_path = download_youtube(url)
        return FileResponse(file_path, filename=os.path.basename(file_path))
    except Exception as e:
        return HTMLResponse(f"<h2>下载失败: {e}</h2>", status_code=400)
