import sqlite3 as sq
#from create_bot import bot
import datetime

def sql_start():
    global base, cur
    base = sq.connect('data.db')
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    #base.execute('CREATE TABLE IF NOT EXISTS wait(counter INTEGER PRIMARY KEY AUTOINCREMENT, checkPay TEXT, name TEXT, age TEXT, studio TEXT, phone TEXT,eMail TEXT, id TEXT)')
    #base.execute('CREATE TABLE IF NOT EXISTS sweets(counter INTEGER PRIMARY KEY AUTOINCREMENT, checkPay TEXT, name TEXT, age TEXT, studio TEXT, phone TEXT,eMail TEXT, id TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS scheduled_mailing (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, launch_time TEXT, flag INTEGER)')
    base.commit()

async def sql_check_scheduled_mailing(user_id):
    cur.execute('SELECT user_id FROM scheduled_mailing WHERE user_id = ?', (user_id,))
    existing_user = cur.fetchone()
    return existing_user is not None

async def sql_add_scheduled_mailing(user_id):
    launch_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not await sql_check_scheduled_mailing(user_id):
        cur.execute('INSERT INTO scheduled_mailing (user_id, launch_time, flag) VALUES (?, ?, ?)', (user_id, launch_time, 0))
        base.commit()
    else:
        pass

async def sql_read_scheduled_mailing():
    cur.execute('SELECT user_id, launch_time, flag FROM scheduled_mailing')
    rows = cur.fetchall()
    return rows

async def sql_remove_scheduled_mailing(user_id):
    cur.execute('DELETE FROM scheduled_mailing WHERE user_id = ?', (user_id,))
    base.commit()

async def sql_update1_scheduled_mailing(user_id):
    cur.execute('UPDATE scheduled_mailing SET flag = 1 WHERE user_id = ?', (user_id,))
    base.commit()

async def sql_update2_scheduled_mailing(user_id):
    cur.execute('UPDATE scheduled_mailing SET flag = 2 WHERE user_id = ?', (user_id,))
    base.commit()