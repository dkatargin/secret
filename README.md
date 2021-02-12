# 🙊 SECRET
![python3.8](https://img.shields.io/badge/python-3.8-green?logo=python)
![fastapi](https://img.shields.io/badge/Backend-FastAPI-blue)
![fastapi](https://img.shields.io/badge/Frontend-Static_HTML-blue)
![postgres](https://img.shields.io/badge/DB-PostgreSQL-blue)
![aes-encryption](https://img.shields.io/badge/encryption-AES-blue)

Super minimal secured secret storage

### Usage cases
The main case is one-time sharing secret with your friend. After first read message will be destroyed 
(be careful with messengers preview) also you can set time-to-live of message for some secure reasons.

### Setup
First of all change secrets in ```backend/settings.py```. Configure PostgreSQL with  ```etc/schema.sql```.  
Setup uvicorn and run server.   
Add crontab rules from ```etc/crontab``` for auto-cleanup expired secrets.

### Developers ext
You can change DB backend on any, just rewrite functions in ```backend/db.py``` file.
