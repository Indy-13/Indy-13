#!/bin/bash

sudo cp email_downloader_py.service /lib/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable email_downloader_py.service

sudo systemctl start email_downloader_py.service