import os
import pytest
from fastapi.testclient import TestClient
from main import app, BASE_UPLOAD_DIRECTORY

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Ensure the base upload directory is clean before each test
    if os.path.exists(BASE_UPLOAD_DIRECTORY):
        for root, dirs, files in os.walk(BASE_UPLOAD_DIRECTORY, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(BASE_UPLOAD_DIRECTORY)

    yield

    # Teardown: Clean up the base upload directory after each test
    if os.path.exists(BASE_UPLOAD_DIRECTORY):
        for root, dirs, files in os.walk(BASE_UPLOAD_DIRECTORY, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def test_upload_cat_image():
    # Create a temporary image
    image_content = b"test_image_content"
    image_filename = "test_image.png"
    category = "happy"

    # Send a POST request to upload the image
    response = client.post(
        "/upload/",
        files={"image": (image_filename, image_content, "image/png")},
        data={"category": category}
    )

    # Assert the response
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "is now stored in happy category" in response_json["message"]

    # Extract the image ID from the upload response
    image_id_with_filename = response_json["message"].split()[2]
    image_id = image_id_with_filename.split('_')[0]

    # Assert the image is saved in the correct category directory
    category_directory = os.path.join(BASE_UPLOAD_DIRECTORY, category)
    saved_files = os.listdir(category_directory)
    assert len(saved_files) == 1
    saved_file = saved_files[0]
    assert saved_file.startswith(image_id)
    assert saved_file.endswith(image_filename)

    with open(os.path.join(category_directory, saved_file), "rb") as f:
        assert f.read() == image_content


def test_download_cat_image():
    # Create a temporary image file
    image_content = b"test_image_content"
    image_filename = "test_image.png"
    category = "happy"

    # First, upload the image
    upload_response = client.post(
        "/upload/",
        files={"image": (image_filename, image_content, "image/png")},
        data={"category": category}
    )
    assert upload_response.status_code == 200

    # Extract the image ID and filename from the upload response
    image_id_with_filename = upload_response.json()["message"].split()[2]

    # Send a POST request to download the image
    download_response = client.post(
        "/download/",
        data={"image_id_with_filename": image_id_with_filename, "category": category}
    )

    # Assert the response
    assert download_response.status_code == 200
    assert download_response.content == image_content
    assert download_response.headers["content-type"] == "application/octet-stream"

    # Test downloading a non-existent image
    non_existent_response = client.post(
        "/download/",
        data={"image_id_with_filename": "non_existent_id.png", "category": category}
    )
    assert non_existent_response.status_code == 404
    assert non_existent_response.json() == {"detail": "Image not found"}
