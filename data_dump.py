import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
import sqlite3
from Table import Table
from SqlConnection import sqliteConnection


def get_checkbox():
    var1 = c1.get()
    var2 = c2.get()
    var3 = c3.get()
    var4 = c4.get()
    var5 = c5.get()
    print(var1, var2, var3, var4, var5)

    append_string = ""
    if var1 == 1:
        append_string = "\"Vienna Philharmonic\""
    if var2 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Bamberg Symphony\""
    if var3 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Philharmonia Hungarica\""
    if var4 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Gewandhaus Leipzig\""
    if var5 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Berlin Philharmonic\""
    append_string = "(" + append_string + ")"
    print(append_string)

    cursor = sqliteConnection.cursor()
    sqlite_select_Query = (
            "select pa.event_id,pa.date_of_event,pa.country, pa.place, pa.orchestra, pl.program,c.conductor \n"
            "from programs_all pa, program_list pl, conductors c\n"
            "where pa.event_id =pl.event_id\n"
            "and pa.event_id = c.event_id\n"
            "and pa.Orchestra in " + append_string + ";"
    )
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Event-ID', 'Date Of Event', 'Country', 'Place', 'Orchestra', 'Program', 'Conductor'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

def get_checkbox_csv():
    var1 = c1.get()
    var2 = c2.get()
    var3 = c3.get()
    var4 = c4.get()
    var5 = c5.get()
    print(var1, var2, var3, var4, var5)

    append_string = ""
    if var1 == 1:
        append_string = "\"Vienna Philharmonic\""
    if var2 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Bamberg Symphony\""
    if var3 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Philharmonia Hungarica\""
    if var4 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Gewandhaus Leipzig\""
    if var5 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Berlin Philharmonic\""
    append_string = "(" + append_string + ")"
    print(append_string)

    cursor = sqliteConnection.cursor()
    sqlite_select_Query = (
            "select pa.event_id,pa.date_of_event,pa.country, pa.place, pa.orchestra, pl.program,c.conductor \n"
            "from programs_all pa, program_list pl, conductors c\n"
            "where pa.event_id =pl.event_id\n"
            "and pa.event_id = c.event_id\n"
            "and pa.Orchestra in " + append_string + ";"
    )
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    csvWriter = csv.writer(open("output.csv", "w",  encoding="utf-8"),lineterminator='\n')
    csvWriter.writerows(x)
    cursor.close()



if __name__ == '__main__':
    try:
        #sqliteConnection = sqlite3.connect('test_1.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    window = tk.Tk()
    window.title("Data Dump  - Dr. Friedemann Pestel")
    window.geometry('1000x400')

    lbl2 = Label(window, text="Here you would be able to obtain a complete data dump for the respective Orchestra "
                              "that has been queried", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=0, sticky=E + W + S + N, columnspan=3, rowspan=2)

    c1 = IntVar()
    Checkbutton(window, text="Vienna Philharmonic", variable=c1).grid(row=3, column=1, sticky=W)
    c2 = IntVar()
    Checkbutton(window, text="Bamberg Symphony", variable=c2).grid(row=4, column=1, sticky=W)
    c3 = IntVar()
    Checkbutton(window, text="Philharmonia Hungarica", variable=c3).grid(row=5, column=1, sticky=W)
    c4 = IntVar()
    Checkbutton(window, text="Gewandhaus Leipzig", variable=c4).grid(row=6, column=1, sticky=W)
    c5 = IntVar()
    Checkbutton(window, text="Berlin Philharmonic", variable=c5).grid(row=7, column=1, sticky=W)

    btn = Button(window, text='Fetch Data dump', command=get_checkbox)
    btn.grid(column=2, row=3, rowspan=5)

    btn = Button(window, text='Export as CSV', command=get_checkbox_csv)
    btn.grid(column=3, row=3, rowspan=5)

    lbl3 = Label(window, text="Tip :: Note down the Event-ID of the record you wish to DELETE or UPDATE. \n You will have to DELETE the record first and later INSERT it back to update", borderwidth=2, relief='ridge')
    lbl3.grid(column=0, row=8, sticky=E + W + S + N, columnspan=3, rowspan=2)

    window.mainloop()
    sqliteConnection.close()
