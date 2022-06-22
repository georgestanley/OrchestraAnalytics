from matplotlib import pyplot as plt
import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
import sqlite3
from SqlConnection import sqliteConnection
from Table import Table


# import table_demo as td

class SSG(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def get_all_data():

    cursor = sqliteConnection.cursor()

    sqlite_select_Query = ("with total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "group by Orchestra, Country)\n"
                           "group by Orchestra )\n"
                           "\n"
                           "select total.Orchestra,Country,total.total, counts,\n"
                           "    round(((counts *1.0) /total.total)*100,2) as share\n"
                           "from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "group by Orchestra, Country) pageviews,\n"
                           "    total\n"
                           "where pageviews.Orchestra=total.Orchestra\n"
                           "order by total.Orchestra, share desc")

    cursor.execute(sqlite_select_Query)
    print('query = ', sqlite_select_Query)
    data = (row for row in cursor.fetchall())
    cursor.close()
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'Conductor', 'Total', 'Count', 'Share'), rows=data)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_dates():
    """
    Gets the dates and returns query1 output filtered between the two input dates
    """
    # TODO: ADD a check clause to handle if wrong date format inputted

    d1_val = d1.get()
    d2_val = d2.get()
    print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ("with total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "    and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                                                                                                 "group by Orchestra, Country)\n"
                                                                                                 "group by Orchestra )\n"
                                                                                                 "\n"
                                                                                                 "select total.Orchestra,Country,total.total, counts,\n"
                                                                                                 "    round(((counts *1.0) /total.total)*100,2) as share\n"
                                                                                                 "from (select \n"
                                                                                                 "    Orchestra,\n"
                                                                                                 "    Country,\n"
                                                                                                 "    count(*) counts\n"
                                                                                                 "from programs_all\n"
                                                                                                 "where 1=1\n"
                                                                                                 "and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                                                                                                                                                                   "group by Orchestra, Country) pageviews,\n"
                                                                                                                                                                   "    total\n"
                                                                                                                                                                   "where pageviews.Orchestra=total.Orchestra\n"
                                                                                                                                                                   "order by total.Orchestra, share desc")
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'Conductor', 'Total', 'Count', 'Share'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_dates_csv():
    d1_val = d1.get()
    d2_val = d2.get()
    # print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ("with total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "    and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                                                                                                 "group by Orchestra, Country)\n"
                                                                                                 "group by Orchestra )\n"
                                                                                                 "\n"
                                                                                                 "select total.Orchestra,Country,total.total, counts,\n"
                                                                                                 "    round(((counts *1.0) /total.total)*100,2) as share\n"
                                                                                                 "from (select \n"
                                                                                                 "    Orchestra,\n"
                                                                                                 "    Country,\n"
                                                                                                 "    count(*) counts\n"
                                                                                                 "from programs_all\n"
                                                                                                 "where 1=1\n"
                                                                                                 "and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                                                                                                                                                                   "group by Orchestra, Country) pageviews,\n"
                                                                                                                                                                   "    total\n"
                                                                                                                                                                   "where pageviews.Orchestra=total.Orchestra\n"
                                                                                                                                                                   "order by total.Orchestra, share desc")
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    # print(rows)
    csvWriter = csv.writer(open("output.csv", "w"), lineterminator='\n')
    csvWriter.writerows(x)
    cursor.close()


def get_checkbox():
    d3_val = d3.get()
    d4_val = d4.get()
    var1 = c1.get()
    var2 = c2.get()
    var3 = c3.get()
    var4 = c4.get()
    var5 = c5.get()
    print(var1, var2, var3, var4, var5)

    append_string = ""
    if var1 == 1:
        append_string = "\"Bamberg Symphony\""
    if var2 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Berlin Philharmonic\""
    if var3 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Gewandhaus Leipzig\""
    if var4 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Philharmonia Hungarica\""
    if var5 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Vienna Philharmonic\""
    append_string = "(" + append_string + ")"
    print(append_string)

    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ("with total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "and Orchestra in \n" + append_string +
                           "    and date_of_event  between \'" + d3_val + "\' and \'" + d4_val + "\' \n"
                                                                                                 "group by Orchestra, Country)\n"
                                                                                                 "group by Orchestra )\n"
                                                                                                 "\n"
                                                                                                 "select total.Orchestra,Country,total.total, counts,\n"
                                                                                                 "    round(((counts *1.0) /total.total)*100,2) as share\n"
                                                                                                 "from (select \n"
                                                                                                 "    Orchestra,\n"
                                                                                                 "    Country,\n"
                                                                                                 "    count(*) counts\n"
                                                                                                 "from programs_all\n"
                                                                                                 "where 1=1\n"
                                                                                                 "    and date_of_event  between \'" + d3_val + "\' and \'" + d4_val + "\' \n"
                                                                                                                                                                       "group by Orchestra, Country) pageviews,\n"
                                                                                                                                                                       "    total\n"
                                                                                                                                                                       "where pageviews.Orchestra=total.Orchestra\n"
                                                                                                                                                                       "order by total.Orchestra, share desc"
                           )
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'Conductor', 'Total', 'Count', 'Share'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_chart():
    """
    Creates a chart

    """
    d1_val = d1.get()
    d2_val = d2.get()
    # d1_val = '1900-01-01'
    # d2_val = '1900-12-31'
    print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()

    # print('SQL query = ', sqlite_select_Query)
    sqlite_select_Query = ("with total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "--and Orchestra in ('Vienna Philharmonic')\n"
                           "and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                                                                                             "group by Orchestra, Country)\n"
                                                                                             "group by Orchestra )\n"
                                                                                             "\n"
                                                                                             "select Country, sum(counts) xxx\n"
                                                                                             "from  (\n"
                                                                                             "select total.Orchestra,Country,total.total, counts,\n"
                                                                                             "    round(((counts *1.0) /total.total)*100,2) as share\n"
                                                                                             "from (select \n"
                                                                                             "    Orchestra,\n"
                                                                                             "    Country,\n"
                                                                                             "    count(*) counts\n"
                                                                                             "from programs_all\n"
                                                                                             "where 1=1\n"
                                                                                             "    and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                                                                                                                                                                   "group by Orchestra, Country) pageviews,\n"
                                                                                                                                                                   "    total\n"
                                                                                                                                                                   "where pageviews.Orchestra=total.Orchestra\n"
                                                                                                                                                                   "order by total.Orchestra, share desc) \n"
                                                                                                                                                                   "group by country")
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    # data = (row for row in x)
    orchestra = []
    data = []
    values = []
    i = 0
    for row in x:
        # orchestra.append(row[0])
        data.append(row[0])
        values.append(row[1])
    print(orchestra)
    print(data)
    print(values)
    # counts = Counter(orchestra)
    # counts = [[x,orchestra.count(x)] for x in set(orchestra)]
    # print(type(counts))

    fig = plt.figure(figsize=(10, 7))
    plt.pie(values, labels=data, autopct='%1.1f%%')
    '''
    Use this below block of code if you need to fetch data of multiple orchestras together
    and later dsiplay them are seaprate graphs

    data1 = []
    values1 = []
    a_prev = ''
    i = 0
    figs = []

    for a,b,c  in zip(orchestra,data,values):
        #print(a,b,c)
        if a_prev == a or a_prev == '':
            data1.append(b)
            values1.append(c)
            a_prev = a
            #print(data1,values1)
        elif a_prev != a :
            figs.append( plt.figure(figsize=(10, 7)))
            #print(values1,data1)
            plt.pie(values1, labels=data1,autopct='%1.1f%%')
            plt.title(a_prev)
            a_prev = a
            data1 = [b]
            values1 = [c]

    figs.append(plt.figure(figsize=(10, 7)))
    plt.pie(values1, labels=data1,autopct='%1.1f%%')
    plt.title(a_prev)
    #print(values1, data1)
    '''

    # Creating plot
    # fig = plt.figure(figsize=(10, 7))
    # plt.pie(values, labels=data)

    # show plot
    plt.show()


def get_chart_orchestra_wise():
    d3_val = d3.get()
    d4_val = d4.get()
    # d3_val = '1900-01-01'
    # d4_val = '1900-12-31'
    print('d1 =', d3_val, 'd2=', d4_val)
    cursor = sqliteConnection.cursor()

    var1 = c1.get()
    var2 = c2.get()
    var3 = c3.get()
    var4 = c4.get()
    var5 = c5.get()
    print(var1, var2, var3, var4, var5)

    append_string = ""
    if var1 == 1:
        append_string = "\"Bamberg Symphony\""
    if var2 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Berlin Philharmonic\""
    if var3 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Gewandhaus Leipzig\""
    if var4 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Philharmonia Hungarica\""
    if var5 == 1:
        append_string = append_string + ("," if len(append_string) > 0 else "") + "\"Vienna Philharmonic\""
    append_string = "(" + append_string + ")"
    print(append_string)

    sqlite_select_Query = ("\n"
                           "with total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select \n"
                           "    Orchestra,\n"
                           "    Country,\n"
                           "    count(*) counts\n"
                           "from programs_all\n"
                           "where 1=1\n"
                           "--and Orchestra in ('Vienna Philharmonic')\n"
                           "    and date_of_event  between \'" + d3_val + "\' and \'" + d4_val + "\' \n"
                                                                                                 "group by Orchestra, Country)\n"
                                                                                                 "group by Orchestra )\n"
                                                                                                 "\n"
                                                                                                 "select total.Orchestra,Country,total.total, counts,\n"
                                                                                                 "    round(((counts *1.0) /total.total)*100,2) as share\n"
                                                                                                 "from (select \n"
                                                                                                 "    Orchestra,\n"
                                                                                                 "    Country,\n"
                                                                                                 "    count(*) counts\n"
                                                                                                 "from programs_all\n"
                                                                                                 "where 1=1\n"
                                                                                                 "    and date_of_event  between \'" + d3_val + "\' and \'" + d4_val + "\' \n"
                                                                                                                                                                       "group by Orchestra, Country) pageviews,\n"
                                                                                                                                                                       "    total\n"
                                                                                                                                                                       "where pageviews.Orchestra=total.Orchestra\n"
                                                                                                                                                                       "and total.Orchestra in \n" + append_string +
                           "order by total.Orchestra, share desc;\n")

    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = []
    values = []
    i = 0
    for row in x:
        data.append(row[1])
        values.append(row[4])
    print(data)
    print(values)
    # counts = Counter(orchestra)
    # counts = [[x,orchestra.count(x)] for x in set(orchestra)]
    # print(type(counts))

    fig = plt.figure(figsize=(10, 7))
    plt.pie(values, labels=data, autopct='%1.1f%%')
    plt.show()


def populate_country_list():
    """
    Loads a list of all countries
    :return: List of all countries
    """
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = '''select distinct country from programs_all order by country;'''
    x = cursor.execute(sqlite_select_Query)
    countries = ['Choose a country']
    for row in x:
        countries.append(row[0])
    return countries


def get_country_data():
    country = variable.get()  # GET the country name
    if country == 'None':
        country = 'null'
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = (
            'select pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra,group_concat(pl.program) program, '
            'group_concat(distinct c.conductor) conductor\n '
            'from programs_all pa, program_list pl ,conductors c\n'
            'where 1=1\n'
            'and pa.event_id=pl.event_id\n'
            'and pa.event_id=c.event_id\n'
            'and pa.country = \'' + country + '\'\n'
                                              'group by pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra;')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Event-ID', 'Date', 'Country', 'City', 'Orchestra', 'Program', 'Conductor'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Orchestra Tours Data - Dr. Friedemann Pestel")
    window.geometry('1000x500')

    cursor = sqliteConnection.cursor()
    #print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)

    # print("Query output is")

    lbl = Label(window, text="Orchestra(s)+Country, "
                             " within a period of choice; "
                             " results both in absolute and "
                             "\n proportional figures",
                font=('Arial Bold', 10))
    lbl.grid(column=0, row=0, columnspan=2)

    btn = Button(window, text='Fetch Query1', command=get_all_data)
    btn.grid(column=1, row=1)

    lbl2 = Label(window, text="Query_1 :: Query whole database", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=1, sticky=E + W + S + N)

    lbl2 = Label(window, text="Query_2 :: Query with date Range in format YYYY-MM-DD", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=2, sticky=E + W + S + N)

    d1 = Entry(window)
    d2 = Entry(window)
    d1.grid(column=1, row=2, sticky='W')
    d2.grid(column=2, row=2, sticky='W')
    btn = Button(window, text='Fetch Query2', command=get_dates)
    btn.grid(column=3, row=2)
    btn = Button(window, text='Download as CSV', command=get_dates_csv)
    btn.grid(column=4, row=2)
    btn = Button(window, text='Create Chart', command=get_chart)
    btn.grid(column=5, row=2)

    # Query Orchestra-wise
    row_n = 3
    lbl2 = Label(window, text="Query_3 :: Query Orchestra-wise", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=row_n, sticky=E + W + S + N, rowspan=5)

    c1 = IntVar()
    Checkbutton(window, text="Bamberg Symphony", variable=c1).grid(row=row_n, column=3, sticky=W)  # 5
    c2 = IntVar()
    Checkbutton(window, text="Berlin Philharmonic", variable=c2).grid(row=row_n + 1, column=3, sticky=W)  # 1
    c3 = IntVar()
    Checkbutton(window, text="Gewandhaus Leipzig", variable=c3).grid(row=row_n + 2, column=3, sticky=W)  # 4
    c4 = IntVar()
    Checkbutton(window, text="Philharmonia Hungarica", variable=c4).grid(row=row_n + 3, column=3, sticky=W)  # 3
    c5 = IntVar()
    Checkbutton(window, text="Vienna Philharmonic", variable=c5).grid(row=row_n + 4, column=3, sticky=W)  # 2

    btn = Button(window, text='Fetch Query3', command=get_checkbox)
    btn.grid(column=4, row=row_n, rowspan=5)

    d3 = Entry(window)
    d4 = Entry(window)
    d3.grid(column=1, row=row_n, sticky='W', rowspan=5)
    d4.grid(column=2, row=row_n, sticky='W', rowspan=5)
    btn = Button(window, text='Get Charts', command=get_chart_orchestra_wise)
    btn.grid(column=5, row=row_n, rowspan=5)

    # Part4: Display the country names and drop down list. User selects country. Software
    # displays the list of concerts played in the country
    row_n = 8
    choices = populate_country_list()
    variable = StringVar(window)  # Creates a TKinter Variable
    variable.set(choices[0])  # set default value
    # tkvar.set('Pizza')  # set the default option
    lbl3 = Label(window, text="Query4 :: Query the entire database for the given Country")
    lbl3.grid(row=row_n, column=0)
    popupMenu = OptionMenu(window, variable, *choices)
    popupMenu.grid(row=row_n, column=1)
    btn = Button(window, text='Execute', command=get_country_data)
    btn.grid(column=2, row=row_n)

    window.mainloop()
    sqliteConnection.close()
