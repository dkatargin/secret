import datetime
import uuid

from fastapi import FastAPI, Form, HTTPException

import db

app = FastAPI()


@app.post("/save/")
def save_secret(text: str = Form("secret_form"), ttl: int = Form("secret_form")):
    if 31 < ttl < 0:
        raise HTTPException(status_code=400, detail="wrong ttl value")
    uid = uuid.uuid4()
    expires = datetime.datetime.now() + datetime.timedelta(days=ttl)
    try:
        db.db_save(uid, text, expires)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "https://secret.exo.icu/get/{}".format(uid)


@app.get("/get/{uid}")
def get_secret(uid: str):
    text = db.db_pop(uid)
    if not text:
        raise HTTPException(status_code=404, detail="secret not found")
    return text
