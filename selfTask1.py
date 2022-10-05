import sqlite3
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("library.sqlite")
# открываем файл с дампом базой двнных
f_damp = open('library.db','r', encoding ='utf-8-sig')
# читаем данные из файла
damp = f_damp.read()
# закрываем файл с дампом
f_damp.close()
# запускаем запросы
con.executescript(damp)
# сохраняем информацию в базе данных
con.commit()
# создаем курсор
cursor = con.cursor()
cursor.execute('''
SELECT genre_name,count(book.book_id), sum(book.available_numbers), min(book.year_publication) FROM genre
JOIN book USING(genre_id)
GROUP BY book.genre_id''')
print(cursor.fetchall())
# закрываем соединение с базой
con.close()