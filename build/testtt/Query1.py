from tkinter import *
import tkinter as tk
from SqlConnection import sqliteConnection

def get_all_data():
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ("some sql query")
    cursor.execute(sqlite_select_Query)
    data = (row for row in cursor.fetchall())
    cursor.close()
    root = tk.Tk()
    root.mainloop()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Window Title")
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)

    btn = Button(window, text='Fetch Query1', command=get_all_data)
    btn.grid(column=1, row=1)

    window.mainloop()
    sqliteConnection.close()
