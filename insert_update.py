import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
import sqlite3
from Query4 import Table


def get_to_be_deleted_data():
    d1_val = d1.get()
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = (
            "select pa.event_id,pa.date_of_event,pa.country,pa.place,pa.orchestra,pl.program,c.conductor \n"
            "from programs_all pa, program_list pl, conductors c\n"
            "where pa.event_id =pl.event_id\n"
            "and pa.event_id = c.event_id and pa.event_id =" + d1_val + ";")
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Event-ID', 'Date Of Event', 'Country', 'Place', 'Orchestra', 'Program', 'Conductor'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def delete_data():
    d1_val = d1.get()
    cursor = sqliteConnection.cursor()
    sql_query1 = ("delete from programs_all where event_id ='" + d1_val + "';")
    sql_query2 = ("delete from  program_list where event_id ='" + d1_val + "';")
    sql_query3 = ("delete from conductors where event_id ='" + d1_val + "';")
    print(sql_query1, sql_query2, sql_query3)
    cursor.execute(sql_query1)
    cursor.execute(sql_query2)
    cursor.execute(sql_query3)
    sqliteConnection.commit()
    cursor.close()


def insert_data():
    cursor = sqliteConnection.cursor()
    e1_val = e1.get()
    e2_val = e2.get()
    e3_val = e3.get()
    e4_val = e4.get()
    e5_val = e5.get()
    e6_val = e6.get()

    insert_query = ("insert into programs_temp (Datum, Land, Ort, Dirigent, Program,Orchestra ) values ('"
                    + e1_val + "','"
                    + e2_val + "','"
                    + e3_val + "','"
                    + e4_val + "','"
                    + e5_val + "','"
                    + e6_val + "');")
    print(insert_query)
    cursor.execute(insert_query)

    max_event_id_query = ("select max(event_id) from programs_temp;")
    cursor.execute(max_event_id_query)
    event_id = cursor.fetchall()
    event_id = event_id[0][0]
    print(event_id)

    insert_query = "insert into programs_all (Event_id, date_of_event, country, place, Orchestra) values (" + str(
        event_id) + ",'" + e1_val + "','" + e2_val + "','" + e3_val + "','" + e6_val + "');"
    print(insert_query)
    cursor.execute(insert_query)

    if len(e5_val) > 0:
        insert_query = (
                "insert into program_list (Event_id, program) values (" + str(event_id) + ",'" + e5_val + "');")
        print(insert_query)
        cursor.execute(insert_query)
    if len(e4_val) > 0:
        insert_query = (
                "insert into conductors (Event_id, conductor) values (" + str(event_id) + ",'" + e4_val + "');")
        print(insert_query)
        cursor.execute(insert_query)

    sqliteConnection.commit()
    lbl6 = Label(window, text='Success')
    lbl6.grid(row=10)
    cursor.close()


if __name__ == '__main__':
    try:
        sqliteConnection = sqlite3.connect('C:\\sqlite\\test_1.db')
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
    window.title("Data Modification - Dr. Friedemann Pestel")
    window.geometry('1000x400')

    lbl1 = Label(window, text="DELETE", font=("bold"))
    lbl2 = Label(window, text="Enter the Event-Id of the record \n you wish to delete")
    lbl1.grid(column=0, row=0)
    lbl2.grid(column=0, row=1)

    d1 = Entry(window)
    d1.grid(column=1, row=1)

    btn = Button(window, text='View Records to be Deleted', command=get_to_be_deleted_data)
    btn.grid(column=0, row=3, columnspan=3, sticky=N + E + W + S)
    btn = Button(window, text='DELETE', command=delete_data)
    btn.grid(column=0, row=4, columnspan=3, sticky=N + E + W + S)

    lbl3 = Label(window, text='Insert', font="Bold")
    lbl3.grid(row=5, padx=5, pady=5, columnspan=7)
    lbl4 = Label(lbl3, text="Enter the following details for a new Data Record")
    lbl3.grid(row=6, padx=5, pady=5, columnspan=7)

    e1 = Entry(window)
    e2 = Entry(window)
    e3 = Entry(window)
    e4 = Entry(window)
    e5 = Entry(window)
    e6 = Entry(window)

    e1.grid(row=8, column=0, sticky=N + E + W + S)
    e2.grid(row=8, column=1)
    e3.grid(row=8, column=2)
    e4.grid(row=8, column=3)
    e5.grid(row=8, column=4)
    e6.grid(row=8, column=5)

    lbl_date = Label(window, text="Date :: YYYY-MM-DD")
    lbl_Country = Label(window, text="Country")
    lbl_Place = Label(window, text="Place")
    lbl_Orch = Label(window, text="Conductor")
    lbl_prog = Label(window, text="Program")
    lbl_cond = Label(window, text="Orchestra")

    lbl_date.grid(row=7, column=0)
    lbl_Country.grid(row=7, column=1)
    lbl_Place.grid(row=7, column=2)
    lbl_Orch.grid(row=7, column=3)
    lbl_prog.grid(row=7, column=4)
    lbl_cond.grid(row=7, column=5)

    btn = Button(window, text='Insert Record', command=insert_data)
    btn.grid(column=3, row=9, columnspan=2, sticky=N + E + W + S)

    window.mainloop()
    sqliteConnection.close()
