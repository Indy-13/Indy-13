#!/bin/bash

sudo cp email_downloader_py.service /lib/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable test-py.service

sudo systemctl start test-py.service