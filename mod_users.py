import sqlite3 as sq


def db_table_val(user_id: int, state: str):
    conn = sq.connect('db.db', check_same_thread=False)
    cursor = conn.cursor()
    user = cursor.execute(f'SELECT 1 FROM users WHERE user_id == "{user_id}"').fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id, state) VALUES (?, ?)', (user_id, state))
    conn.commit()
    conn.close()

def db_change_state(user_id: int):
    with sq.connect('db.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        state = cursor.execute(f'SELECT state FROM users WHERE user_id == "{user_id}"').fetchall()
        if state[0][0] == 'not_ignore':
            #change to 'ignore'
            cursor.execute(f'UPDATE users SET state = "ignore" WHERE user_id == "{user_id}"')
            text = 'Вы отказались от уведомлений.'
        else:
            #change to 'not_ignore'
            cursor.execute(f'UPDATE users SET state = "not_ignore" WHERE user_id == "{user_id}"')
            text = 'Вы согласились на уведомления.'
    return text
