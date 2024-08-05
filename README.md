# Cat Image Microservice

This repository contains a FastAPI microservice for uploading and downloading cat images by category.

## Communication Contract

### Uploading Cat Images

#### Request

To upload a cat image, send a POST request to `/upload/` with the following form data:
- `image`: The image file to be uploaded (required).
- `category`: The category under which the image should be stored (required).

##### Example Request

```bash
import requests

url = "http://127.0.0.1:8000/upload/"
files = {"image": open("/path/to/your/cat_image.png", "rb")}
data = {"category": "happy"}
response = requests.post(url, files=files, data=data)

```
##### Example Response

```bash
{
  "message": "Cat image <image_id>_<filename>.png is now stored in happy category"
}
```

### Downloading Cat Images

#### Request

To download a cat image, send a POST request to `/download/` with the following form data:
- `image_id_with_filename`: The image id to be retrieved (required).
- `category`: The category under which the image should be retrieved from (required).

##### Example Request

```bash
import requests

url = "http://127.0.0.1:8000/download/"
data = {
    "category": "happy",
    "image_id_with_filename": "<image_id>_<filename>.jpg"
}
response = requests.post(url, data=data)
```
##### Example Response

![alt text](https://pngimg.com/uploads/cat/cat_PNG50424.png)

### UML Diagram
![Alt text](/UML/UML.png?raw=true "UML Diagram")