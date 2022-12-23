from photos_api_helper import PhotosAPIHelper

CREDS_FILE = "client_secret.json"


class TestPhotosAPIHelper:
    def test_create_service(self):
        api_helper = PhotosAPIHelper(CREDS_FILE)

        service = api_helper.get_service()

        assert service is not None

    def test_get_albums(self):
        api_helper = PhotosAPIHelper(CREDS_FILE)

        albums = api_helper.get_albums()

        assert len(albums) > 0

    def test_get_album_id(self):
        api_helper = PhotosAPIHelper(CREDS_FILE)

        album_id = api_helper.get_album_id("_aaa_tobi_test_album")

        assert album_id is not None

    def test_add_image_to_album(self):
        api_helper = PhotosAPIHelper(CREDS_FILE)

        image_data = open("my_image.jfif", "rb").read()
        album_id = "AAz4npHl7_YxUX3jhHbjuwoJ9K-rPwtMSgwDKvIRpGZRkzILF01Ajb3pRrKVQNWkA-cUu7ZpoJAF"

        response = api_helper.add_image_to_album(album_id, "FirstImage", image_data)

        assert (
            response.get("newMediaItemResults")[0].get("status").get("message")
            == "Success"
        )
