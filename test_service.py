import time
import platform
from imbox import Imbox  # pip install imbox
from logger import Logger

import os
import requests

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from photos_api_helper import PhotosAPIHelper

CREDS_FILE = "client_secret_fotopasti_fotky.json"

current_patform = str(platform.system()).lower()

if current_patform == "windows":
    logger_config = {"LOG_FILE": r"c:\Temp\EmailDownloader.log"}
elif current_patform == "linux":
    logger_config = {"LOG_FILE": "/home/ubuntu/EmailDownloader/EmailDownloader.log"}
else:
    logger_config = {"LOG_FILE": "EmailDownloader.log"}

logger = Logger(logger_config)

# api_helper = PhotosAPIHelper(CREDS_FILE, logger)


while True:
    print("This is a test python file!")
    time.sleep(20)
