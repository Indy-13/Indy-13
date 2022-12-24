import os
import requests

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


class PhotosAPIHelper:
    def __init__(self, client_secrets_file, logger):

        self.__logger = logger
        self.__api_name = "photoslibrary"
        self.__api_version = "v1"
        self.__scopes = [
            "https://www.googleapis.com/auth/photoslibrary",
            "https://www.googleapis.com/auth/photoslibrary.sharing",
        ]
        self.__client_secrets_file = client_secrets_file

        self.__pickle_file = f"/home/ubuntu/EmailDownloader/token_{self.__api_name}_{self.__api_version}.pickle"
        self.__service = self.__create_service()

        self.__album_cache = dict()

    def __create_service(self):
        cred = self.__get_credentials()

        try:
            service = build(
                self.__api_name,
                self.__api_version,
                credentials=cred,
                static_discovery=False,
            )
            self.__logger.log_message(
                1,
                "INFO",
                "Service created successfully",
            )
            return service
        except Exception as e:
            self.__logger.log_message(
                1,
                "ERROR",
                f"Create service failed: {e}",
            )
        return None

    def __get_credentials(self):

        cred = None

        if os.path.exists(self.__pickle_file):
            with open(self.__pickle_file, "rb") as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__client_secrets_file, self.__scopes
                )
                cred = flow.run_local_server()

            with open(self.__pickle_file, "wb") as token:
                pickle.dump(cred, token)

        return cred

    def get_album_id(self, album_name):

        album_id = self.__album_cache.get(album_name)

        if not album_id:
            existing_albums = self.get_albums()

            for album in existing_albums:
                self.__album_cache[album.get("title").lower()] = album.get("id")

            album_id = self.__album_cache.get(album_name)

            if not album_id:
                album_id = self.create_album(album_name)
                self.__album_cache[album_name] = album_id

        return album_id

    def get_albums(self):
        response = self.__service.albums().list(excludeNonAppCreatedData=True).execute()
        albums = response.get("albums", [])

        return albums

    def create_album(self, album_name):
        request_body = {"album": {"title": album_name}}

        response = self.__service.albums().create(body=request_body).execute()

        return response.get("id")

    def get_service(self):
        return self.__service

    def add_image_to_album(self, album_id, file_name, image_data):
        upload_token = self.upload_image_data(image_data)
        return self.create_image_in_album(album_id, file_name, upload_token)

    def upload_image_data(self, image_data):
        upload_url = "https://photoslibrary.googleapis.com/v1/uploads"
        access_token = self.__get_credentials().token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/octet-stream",
            "X-Goog-Upload-Content-Type": "mime-type",
            "X-Goog-Upload-Protocol": "raw",
        }

        response = requests.post(url=upload_url, headers=headers, data=image_data)

        return response.content.decode("utf-8")

    def create_image_in_album(self, album_id, file_name, upload_token):
        request_body = {
            "albumId": album_id,
            "newMediaItems": [
                {
                    "description": file_name,
                    "simpleMediaItem": {
                        "fileName": file_name,
                        "uploadToken": upload_token,
                    },
                }
            ],
        }

        create_response = (
            self.__service.mediaItems().batchCreate(body=request_body).execute()
        )

        return create_response
