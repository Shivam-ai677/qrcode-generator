
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import qrcode
from pathlib import Path
from urllib.parse import urlparse
import time

app = FastAPI()

# Project directories
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
QR_DIR = STATIC_DIR / "qrcodes"

# Create QR folder if it doesn't exist
QR_DIR.mkdir(parents=True, exist_ok=True)

# HTML templates setup
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Static files setup
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "qr_generated": False,
            "error": None
        }
    )


# Generate QR code
@app.post("/generate", response_class=HTMLResponse)
def generate_qr(request: Request, url: str = Form(...)):

    url = url.strip()

    # URL validation
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "qr_generated": False,
                "error": "Please enter a valid URL starting with http:// or https://"
            }
        )

    # Generate QR code
    qr = qrcode.make(url)

    # Save QR image
    qr_path = QR_DIR / "qrcode.png"
    qr.save(qr_path)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "qr_generated": True,
            "error": None,
            "qr_version": int(time.time())
        }
    )


# Download QR code
@app.get("/download")
def download_qr():

     class qr_path:
         ...

     if not qr_path.exists():
        return HTMLResponse(
            content="Please generate a QR code first.",
            status_code=404
        )

     return FileResponse(
        path=qr_path,
        media_type="image/png",
        filename="my_qrcode.png"
    )
