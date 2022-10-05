import sqlite3
import pandas as pd
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("library.sqlite")
# выбираем и выводим записи из таблиц author, reader
df = pd.read_sql('''
SELECT title Название, reader_name Читатель, borrow_date Дата FROM book
JOIN book_reader USING (book_id)
JOIN reader USING (reader_id)
WHERE borrow_date LIKE '%-10-%'
ORDER BY borrow_date, reader_name, title
''', con)
print(df)
# закрываем соединение с базой
con.close()
