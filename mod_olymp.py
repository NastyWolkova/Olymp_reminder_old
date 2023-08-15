import sqlite3 as sq
import datetime
from texts import ru_months


queries: list = ['SELECT name, date_start, date_finish FROM olympiads', #olympiads and dates
                 'SELECT name, start_reg, finish_reg FROM olympiads',   #registrations and dates
                 'SELECT num, date_start, date_finish FROM olympiads', #numbers of olympiads and dates
                 'SELECT num, start_reg, finish_reg FROM olympiads',    #numbers of registrations and dates
                 'UPDATE olympiads SET status_ol = 1 WHERE num in "{list_num}"',
                 'UPDATE olympiads SET status_reg = 1 WHERE num in "{list_num}"']

#приведение дат к читаемому виду
def conv_output(func, ru_months: dict):
    string: str = ''
    result: list = []
    for item in func:
        date_start = item[1].split('-')
        date_finsh = item[2].split('-')
        string = f'{item[0]}: {date_start[2]} {ru_months[date_start[1]]}'
        if item[1] != item[2]:
            string += f' - {date_finsh[-1]} {ru_months[date_finsh[1]]}'
        string += f', {item[3]}, {item[4]}'
        result.append(string)
    return result


#function connection with DB and output query
def send_dates(sql: str) -> list:
    with sq.connect('db.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = cursor.execute(sql).fetchall()
        print(query)
        return conv_output(query, ru_months)


#function for change status of olympiads and registarations
def change_status_olymp():
    with sq.connect('db.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        conv = '%Y-%m-%d'
        olymps = cursor.execute('SELECT num, date_start, date_finish FROM olympiads').fetchall()
        print(olymps, type(olymps))
        score: int = 0
        for item in olymps:
            start = datetime.datetime.strptime(item[1], conv)
            finish = datetime.datetime.strptime(item[2], conv)
            delta1 = start - datetime.datetime.now()
            delta2 = finish - datetime.datetime.now()
            if (delta1.days >= 0 and delta1.days < 7) or (delta1.days < 0 and delta2.days >= 0):
                cursor.execute(f'UPDATE olympiads SET status_ol = 1 WHERE num == "{item[0]}"')
                score += 1
            else:
                cursor.execute(f'UPDATE olympiads SET status_ol = 0 WHERE num == "{item[0]}"')
    return score

def change_status_reg():
    with sq.connect('db.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        conv = '%Y-%m-%d'
        olymps = cursor.execute('SELECT num, start_reg, finish_reg FROM olympiads').fetchall()
        print(olymps)
        score: int = 0
        for item in olymps:
            start = datetime.datetime.strptime(item[1], conv)
            finish = datetime.datetime.strptime(item[2], conv)
            delta1 = start - datetime.datetime.now()
            delta2 = finish - datetime.datetime.now()
            print(delta1, delta2)
            if (delta1.days >= 0 and delta1.days < 7) or (delta1.days < 0 and delta2.days >= 0):
                cursor.execute(f'UPDATE olympiads SET status_reg = 1 WHERE num == "{item[0]}"')
                score += 1
            else:
                cursor.execute(f'UPDATE olympiads SET status_reg = 0 WHERE num == "{item[0]}"')
    return score
