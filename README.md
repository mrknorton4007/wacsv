# WhatsApp ChatStorage Viewer
Browse your WhatsApp Desktop backups.

## Config
1. Set the correct timezone and date format in `wacsv/__init__.py` file.
2. Copy `ChatStorage.sqlite` inside the `instance` folder.

## Virtualenv

    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt

## Run server

    (.venv) gunicorn
