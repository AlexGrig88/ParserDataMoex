import time
from bs4 import BeautifulSoup
from services.table_extractor import get_htmltables_for_currencies
from services.mailer import Mailer
from services.excel_creator import ExcelCreator


# выбрать данные основного клиринга
def extract_main_clearing_table(raw_table):
    return [[row[0], float(row[3]), row[4]] for row in raw_table]


# создать одну таблицу из двух с вычисленным результирующем столбцом
def create_composite_table(table1, table2):
    result_table = []
    for i in range(len(table1)):
        result_table.append(table1[i] + table2[i] + [round(table1[i][1] / table2[i][1], 5)])
    return result_table


def main():
    currency_pairs = ["USD/RUB", "JPY/RUB"]
    htmltables = get_htmltables_for_currencies(currency_pairs)  # получаем список из 2-ух html таблиц
    two_tables = []
    for table_html in htmltables:                   # в цикле создаём таблицы python
        soup = BeautifulSoup(table_html, 'lxml')    # создаём объект, чтобы распарсить данные
        table = soup.find_all('table')[0]           # находим таблицу по тегу

        data_table = []
        for row in table.find_all('tr'):            # находим строки по тегу
            data_row = []
            for data in row.find_all('td'):         # находим ячейки по тегу
                data_row.append(data.text)
            if len(data_row) != 0:
                data_table.append(data_row)         # добавляем строку с данными в таблицу
        two_tables.append(extract_main_clearing_table(data_table))

    c_table = create_composite_table(two_tables[0], two_tables[1])  # создаём результирующую таблицу

    # создаём объект ExcelCreator, настраиваем необходимое форматирование и сохраняем в excel файл
    xl_creator = ExcelCreator()
    xl_creator.create_headers(currency_pairs)
    xl_creator.fill_data(c_table)

    xl_creator.format_number_as_finance()
    xl_creator.adjust_column_widths(required_alignment=True)
    filename = "Тестовый_отчет.xlsx"
    xl_creator.save(filename)
    xl_creator.check_autosum(filename)

    time.sleep(1)

    # Отправляем полученную таблицу себе на почту
    my_server = "smtp.gmail.com"
    email_sender = "grigxia86@gmail.com"
    with open(r"C:\Users\UserGrig\passwords\password_smtp.txt", "r") as f:
        my_password = f.read()

    mailer = Mailer(my_server, email_sender, my_password)
    result = mailer.send_mail(
        email_recipient="sacha-grig@yandex.ru",
        message=f'В результирующей таблице {ru_format(xl_creator.row_counter)}',
        path_to_file=filename
    )
    print(result)   # логируем результат


# указываем количество строк в Excel в правильном склонении.
def ru_format(num):
    postfix = ""
    if num % 100 == 11:
        postfix = f"{num} строк"
    elif num % 10 == 1:
        postfix = f"{num} строка"
    elif num % 10 == 0 or num % 10 in range(5, 10) or num % 100 in (12, 13, 14):
        postfix = f"{num} строк"
    else:
        postfix = f"{num} строки"
    return postfix


if __name__ == "__main__":
    main()

