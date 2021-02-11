import datetime
import uuid
import psycopg2
from fastapi import FastAPI

app = FastAPI()

def db_connect():
    connection = psycopg2.connect(user="secret",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="")
   return cursor, connection

def db_save(uid, text, expires):
    try:
        cursor, conn =  db_connect()
        postgres_insert_query = """ INSERT INTO secrets (UID, TEXT, EXPIRES) VALUES (%s,%s,%s)"""
        record_to_insert = (uid, text, expires)
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    

def db_pop(uid):
    result = None
    try:
        # select data
        cursor, conn =  db_connect()
        postgres_select_query = """ SELECT text FROM secrets WHERE uid=%s"""
        record_to_select = (uid,)
        cursor.execute(postgres_select_query, record_to_select)    
        data_list = cursor.fetchall()
        result = data_list[0]
        # remove data
        postgres_delete_query = """ DELETE FROM secrets WHERE uid=%s"""
        record_to_delete = (uid,)
        cursor.execute(postgres_delete_query, record_to_delete)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result


@app.post("/save/")
def save_secret(secret_form):
    id = uuid.uuid4()
    expires = datetime.datetime.now() + datetime.timedelta(days=secret_form.ttl)
    db_save(id, secret_form.text, expires)
    return "https://secret.exo.icu/load/{}".format(id)

@app.get("/get/{uid}")
def get_secret(uid: str):
    text = db_pop(uid)
    return text