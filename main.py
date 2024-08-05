import os
from uuid import uuid4

from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

# Base directory for uploads
BASE_UPLOAD_DIRECTORY = "cat_images"

# Make sure the base upload directory exists
os.makedirs(BASE_UPLOAD_DIRECTORY, exist_ok=True)


@app.post("/upload/")
async def upload_cat_image(image: UploadFile = File(...), category: str = Form(...)):
    # Create category directory if it doesn't exist
    category_directory = os.path.join(BASE_UPLOAD_DIRECTORY, category)
    os.makedirs(category_directory, exist_ok=True)

    # Generate an ID for the image and create the full path
    image_id = str(uuid4())
    image_path = os.path.join(category_directory, f"{image_id}_{image.filename}")

    # Save the image
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())

    return JSONResponse(
        content={"message": f"Cat image {image_id}_{image.filename} is now stored in {category} category"})


@app.post("/download/")
async def download_cat_image(image_id_with_filename: str = Form(...), category: str = Form(...)):
    # Create the file path
    file_path = os.path.join(BASE_UPLOAD_DIRECTORY, category, image_id_with_filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path, media_type='application/octet-stream', filename=image_id_with_filename)

