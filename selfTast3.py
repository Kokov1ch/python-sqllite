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
cursor.execute('''SELECT genre_name, max(res)
FROM (SELECT genre_name, count(book_id) res FROM genre
JOIN book USING (genre_id)
JOIN book_reader USING (book_id)
GROUP BY genre_id
ORDER BY genre_name)''')
print(cursor.fetchall())
# закрываем соединение с базой
con.close()