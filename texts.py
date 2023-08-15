registration: dict = {(2023, 8, 2): 'Олимпиада Систематика',
                      (2023, 8, 4): 'Олимпиада по биоллогии'
                      }

starts: dict = {(2023, 8, 3): 'Олимпиада Систематика',
                (2023, 8, 5): 'Олимпиада по биоллогии'
                }
ru_months = {'01': 'января',
             '02': 'февраля',
             '03': 'марта',
             '04': 'апреля',
             '05': 'мая',
             '06': 'июня',
             '07': 'июля',
             '08': 'августа',
             '09': 'сентября',
             '10': 'октября',
             '11': 'ноября',
             '12': 'декабря'}

update_status: dict = {'olymp_query': 'SELECT num, date_start, date_finish FROM olympiads',
                       'olymp_activ': 'UPDATE olympiads SET status_ol = 1 WHERE num ==',
                       'olymp_disact': 'UPDATE olympiads SET status_ol = 0 WHERE num ==',
                       'reg_query': 'SELECT num, start_reg, finish_reg FROM olympiads',
                       'reg_activ': 'UPDATE olympiads SET status_reg = 1 WHERE num ==',
                       'reg_disact': 'UPDATE olympiads SET status_reg = 0 WHERE num =='}