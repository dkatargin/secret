import datetime

import psycopg2
import psycopg2.extras

import crypt
import settings

cipher = crypt.AESCipher()


def db_connect():
    psycopg2.extras.register_uuid()
    connection = psycopg2.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_ADDR,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    cursor = connection.cursor()
    return cursor, connection


def db_save(uid, text, expires):
    conn = None
    ciphertext = cipher.encrypt(text)

    try:
        cursor, conn = db_connect()
        postgres_insert_query = """ INSERT INTO {} (UID, TEXT, EXPIRES) VALUES (%s,%s,%s)""".format(settings.DB_TABLE)
        record_to_insert = (uid, ciphertext, expires)
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def db_pop(uid):
    plaintext = ""
    conn = None
    try:
        # select data
        cursor, conn = db_connect()
        postgres_select_query = """ SELECT text FROM {} WHERE uid=%s""".format(settings.DB_TABLE)
        record_to_select = (uid,)
        cursor.execute(postgres_select_query, record_to_select)
        data_list = cursor.fetchall()
        if len(data_list) == 0:
            return plaintext
        plaintext = cipher.decrypt(data_list[0][0])
        # remove data
        postgres_delete_query = """ DELETE FROM {} WHERE uid=%s""".format(settings.DB_TABLE)
        record_to_delete = (uid,)
        cursor.execute(postgres_delete_query, record_to_delete)
        conn.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return plaintext


def clean_expired():
    now = datetime.datetime.now()
    cursor, conn = db_connect()
    postgres_select_query = """ SELECT uid FROM {} WHERE expires <= %s""".format(settings.DB_TABLE)
    record_to_select = (now,)
    cursor.execute(postgres_select_query, record_to_select)
    data_list = cursor.fetchall()
    if len(data_list) == 0:
        return

    for i in data_list:
        uid = i[0]
        postgres_delete_query = """ DELETE FROM {} WHERE uid=%s""".format(settings.DB_TABLE)
        record_to_delete = (uid,)
        cursor.execute(postgres_delete_query, record_to_delete)
        conn.commit()
    cursor.close()
    if conn is not None:
        conn.close()
    return
