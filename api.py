from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import os

from easyocr import Reader
import numpy as np
import cv2 as cv
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.post("/uploadfiles/")
async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
    #uploaded_files = []

    for file in files:
        reader = Reader(["ru"], model_storage_directory='/home/ivan/project/python/neural_netwok/hack/models',
                              user_network_directory='/home/ivan/project/python/neural_netwok/hack/user_model')

        contents = await file.read()
        stream = io.BytesIO(contents)
    
        nparr = np.asarray(bytearray(stream.read()), dtype="uint8")
        image = cv.imdecode(nparr, cv.IMREAD_COLOR)

        answer = reader.readtext(image, detail=0)

        #uploaded_files.append({"name": file.filename, "contents": contents})
    return templates.TemplateResponse("uploaded_files.html", {"request": request, "files": answer})

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)