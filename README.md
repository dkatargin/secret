# 🙊 SECRET
![python3.8](https://img.shields.io/badge/python-3.8-green?logo=python)
![fastapi](https://img.shields.io/badge/Backned-FastAPI-green)
![fastapi](https://img.shields.io/badge/Frontend-Static_HTML-green)
![postgres](https://img.shields.io/badge/DB-PostgreSQL-blue)
![aes-encryption](https://img.shields.io/badge/encryption-AES-blue)

Super minimal secured secret storage

### Usage
First of all change secrets in ```backend/settings.py```. Configure PostgreSQL with  ```etc/schema.sql```.  
Setup uvicorn and run server.   
Add crontab rules from ```etc/crontab``` for auto-cleanup expired secrets.
