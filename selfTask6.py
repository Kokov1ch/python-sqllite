import sqlite3
import pandas as pd
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("library.sqlite")
df = pd.read_sql('''
SELECT title Название, available_numbers Количество, count(borrow_date) Количество_выдачи FROM book
LEFT JOIN book_reader USING (book_id)
GROUP BY book_id
ORDER BY Количество_выдачи DESC, Название, Количество
''', con)
print(df)
# закрываем соединение с базой
con.close()