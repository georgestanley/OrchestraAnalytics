from tkinter import *
from tkinter.ttk import *
import sqlite3


def build_gui():
    window = Tk()
    window.title("Orchestra Tours Data - Dr. Friedemann Pestel")
    window.geometry('350x200')
    lbl = Label(window, text="Please select your option",
                font=('Arial Bold', 00))
    lbl.grid(column=0, row=0)

    txt = Entry(window, width=10, state='disabled')
    txt.grid(column=0, row=1)
    txt.focus()

    combo = Combobox(window)
    combo['values'] = (1, 2, 3, 4, 5, "Text")
    combo.current(2)  # set the selected item
    combo.grid(column=1, row=3)
    x = combo.get()

    btn = Button(window, text='Fetch Query1', command=query1())
    btn.grid(column=1, row=1)
    window.mainloop()  # goes on an endless loop unless closed..important to add


def clicked():
    res = "Welcome to" + txt.get()
    lbl.configure(text=x)


def query1():
    sqlite_select_query = """SELECT * from Countries"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    window.lbl.configure(text=len(records))
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for x in records:
        print(x)


if __name__ == '__main__':
    try:
        sqliteConnection = sqlite3.connect('C:\\sqlite\\test_1.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    build_gui()
    cursor.close()
