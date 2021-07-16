import datetime
import sqlite3


# 데이터 저장
def save_score(score):
    global now_time
    insert_task_query = "INSERT INTO scores VALUES (?, ?)"
    now_time = str(datetime.datetime.now())
    insert_task_data = (score, now_time)
    runQuery(insert_task_query, insert_task_data)

# 데이터 불러오기
def load_scores():
    load_tasks_query = "SELECT score, date FROM scores ORDER BY score DESC, date DESC LIMIT 10"
    my_scores = runQuery(load_tasks_query, receive=True)

    return my_scores

# 데이터베이스 연결
def runQuery(sql, data=None, receive=False):
    conn = sqlite3.connect("scoresdata.db")
    cursor = conn.cursor()
    if data:
        cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    if receive:
        return cursor.fetchall()
    else:
        conn.commit()

    conn.close()

# 데이터베이스가 없는 경우 DB 생성
def firstTimeDB():
    create_tables = "CREATE TABLE scores (score INTEGER, date TEXT)"
    runQuery(create_tables)