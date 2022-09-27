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
cursor.execute('''SELECT book.title,book_reader.borrow_date, book_reader.return_date, (julianday(book_reader.return_date) - julianday(book_reader.borrow_date)) AS days FROM book
                    JOIN book_reader ON book_reader.book_id=book.book_id
                    WHERE book_reader.reader_id=:readerId AND book_reader.return_date IS NOT NULL
                    order by days desc''', {"readerId": 6})
print(cursor.fetchall())
# закрываем соединение с базой
con.close()