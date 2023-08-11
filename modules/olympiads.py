import sqlite3 as sq
import datetime
from texts import ru_months


queries: list = ['SELECT name, date_start, date_finish FROM olympiads', #olympiads and dates
                 'SELECT name, start_reg, finish_reg FROM olympiads',   #registrations and dates
                 'SELECT num, date_start, date_finish FROM olympiads', #numbers of olympiads and dates
                 'SELECT num, start_reg, finish_reg FROM olympiads',    #numbers of registrations and dates
                 'UPDATE olympiads SET status_ol = "on" WHERE num in "{list_num}"',
                 'UPDATE olympiads SET status_reg = "on" WHERE num in "{list_num}"']

#приведение дат к читаемому виду
def conv_output(func, ru_months: dict):
    string: str = ''
    for item in func:
        for i in range(3):
            date_start = item[1].split('-')
            date_finsh = item[2].split('-')
            string = f'{item[0]}: {date_start[-1]} {ru_months[date_start[1]]}'
            if item[1] == item[2]:
                break
            else:
                string += f' - {date_finsh[-1]} {ru_months[date_finsh[1]]}'
    return string


#function connection with DB and output query
def send_dates(sql: str):
    with sq.connect('db.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = cursor.execute(sql).fetchall()
        return conv_output(query, ru_months)

print(send_dates(queries[0]))
print(send_dates(queries[1]))


#function for change status of olympiads and registarations
def db_find_olymp(sql: str, ):
    with sq.connect('db.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        conv = '%Y-%m-%d'
        olymps: list = cursor.execute(sql).fetchall()
        print(olymps)
        for item in olymps:
            start = datetime.datetime.strptime(item[1], conv)
            finish = datetime.datetime.strptime(item[2], conv)
            delta1 = start - datetime.datetime.now()
            delta2 = finish - datetime.datetime.now()
            if (delta1.days != delta2.days and delta1.days <= 7 and delta2.days > 0) or delta1.days <= 7:
                cursor.execute(f'UPDATE olympiads SET status_reg = "on" WHERE num == "{item[0]}"')
            else:
                cursor.execute(f'UPDATE olympiads SET status_reg = "off" WHERE num == "{item[0]}"')



db_find_olymp(queries[3])