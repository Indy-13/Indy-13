import os
import platform
import time
from imbox import Imbox  # pip install imbox
from logger import Logger
from photos_api_helper import PhotosAPIHelper

current_patform = str(platform.system()).lower()

if current_patform == "windows":
    logger_config = {"LOG_FILE": r"c:\Temp\EmailDownloader.log"}
    CREDS_FILE = "client_secret_fotopasti_fotky.json"
elif current_patform == "linux":
    logger_config = {"LOG_FILE": "/home/ubuntu/EmailDownloader/EmailDownloader.log"}
    CREDS_FILE = "/home/ubuntu/EmailDownloader/client_secret_fotopasti_fotky.json"
else:
    logger_config = {"LOG_FILE": "EmailDownloader.log"}

logger = Logger(logger_config)

api_helper = PhotosAPIHelper(CREDS_FILE, logger)

host = "imap.gmail.com"
username = "fotopasti.fotky@gmail.com"
password = "gxjcgvcqnlrycjdi"

logger.log_message(
    1,
    "INFO",
    "Starting email loop...",
)

while True:
    mail = Imbox(
        host,
        port=993,
        username=username,
        password=password,
        ssl=True,
        ssl_context=None,
        starttls=False,
    )
    messages = mail.messages(unread=True)

    for (uid, email_message) in messages:
        mail.mark_seen(uid)

        email_sender = email_message.sent_from[0].get("email").split("@")[0].lower()

        for idx, attachment in enumerate(email_message.attachments):
            try:
                att_type = attachment.get("content-type").lower()
                if att_type == "application/octet-stream":
                    att_fn = attachment.get("filename")
                    if not att_fn:
                        image_id = email_message.subject.split("-")[-1]
                        att_fn = (
                            image_id
                            if str(image_id).lower().endswith(".jpg")
                            else f"{image_id}.jpg"
                        )
                    extension = os.path.splitext(att_fn)[1]
                    if extension.lower() == ".jpg":
                        album_id = api_helper.get_album_id(email_sender)
                        logger.log_message(
                            1,
                            "INFO",
                            f"Uploading image: {att_fn}",
                        )
                        image_data = attachment.get("content").read()
                        api_helper.add_image_to_album(album_id, att_fn, image_data)
            except Exception as e:
                logger.log_message(
                    1,
                    "ERROR",
                    f"Attachement processing failed: {e}",
                )

    mail.logout()
    time.sleep(60)
