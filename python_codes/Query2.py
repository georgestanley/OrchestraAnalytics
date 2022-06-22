from matplotlib import pyplot as plt
import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
import sqlite3
from SqlConnection import sqliteConnection


# import table_demo as td

class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER, width=100)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def query_2():
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           'and place is not null\n'
                           'group by Orchestra\n'
                           '    )\n'
                           '    group by Orchestra ),\n'
                           '\n'
                           'pageviews2 as\n'
                           '(select Orchestra,place City , count(distinct pa.event_id) counts\n'
                           'from programs_all pa\n'
                           'where place is not null\n'
                           'group by Orchestra,City)\n'
                           '\n'
                           'select total.Orchestra,City,total.total, counts ,\n'
                           '    round(((counts *1.0) /total.total)*100,2) as share\n'
                           'from pageviews2,\n'
                           '    total\n'
                           'where pageviews2.Orchestra=total.Orchestra\n'
                           'order by total.Orchestra, share desc')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    data = (row for row in cursor.fetchall())
    cursor.close()
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'City', 'Total', 'Count', 'Share'), rows=data)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_dates():
    """
    Gets the dates and returns queery4 output filtered between the two input dates
    """
    # TODO: ADD a check clause to handle if wrong date format inputted

    d1_val = d1.get()
    d2_val = d2.get()
    # d1_val = '1900-01-01'
    # d2_val = '1905-12-31'
    print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           'and place is not null\n'
                           'and date_of_event  between \''
                           + d1_val
                           + '\' and \''
                           + d2_val
                           + '\' \n'
                             'group by Orchestra\n'
                             '    )\n'
                             '    group by Orchestra ),\n'
                             '\n'
                             'pageviews2 as\n'
                             '(select Orchestra,place City , count(distinct pa.event_id) counts\n'
                             'from programs_all pa\n'
                             'where place is not null\n'
                             'and date_of_event  between \''
                           + d1_val
                           + '\' and \''
                           + d2_val
                           + '\' \n'
                             'group by Orchestra,City)\n'
                             '\n'
                             'select total.Orchestra,City,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc')
    print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'City', 'Total', 'Count', 'Share'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_dates_csv():
    d1_val = d1.get()
    d2_val = d2.get()
    # print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           'and place is not null\n'
                           'and date_of_event  between \''
                           + d1_val
                           + '\' and \''
                           + d2_val
                           + '\' \n'
                             'group by Orchestra\n'
                             '    )\n'
                             '    group by Orchestra ),\n'
                             '\n'
                             'pageviews2 as\n'
                             '(select Orchestra,place City , count(distinct pa.event_id) counts\n'
                             'from programs_all pa\n'
                             'where place is not null\n'
                             'and date_of_event  between \''
                           + d1_val
                           + '\' and \''
                           + d2_val
                           + '\' \n'
                             'group by Orchestra,City)\n'
                             '\n'
                             'select total.Orchestra,City,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc')
    # print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    # print(rows)
    csvWriter = csv.writer(open("output.csv", "w", encoding="utf-8"), lineterminator='\n')
    csvWriter.writerows(x)
    print('output printed')
    cursor.close()


def get_chart():
    """
    Creates a chart
    """
    d1_val = d1.get()
    d2_val = d2.get()
    n = int(top_n.get())
    print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           'and place is not null\n'
                           'and date_of_event  between \''
                           + d1_val
                           + '\' and \''
                           + d2_val
                           + '\' \n'
                             'group by Orchestra\n'
                             '    )\n'
                             '    group by Orchestra ),\n'
                             '\n'
                             'pageviews2 as\n'
                             '(select Orchestra,place City , count(distinct pa.event_id) counts\n'
                             'from programs_all pa\n'
                             'where place is not null\n'
                             'and date_of_event  between \''
                           + d1_val
                           + '\' and \''
                           + d2_val
                           + '\' \n'
                             'group by Orchestra,City)\n'
                             '\n'
                             'select City , sum(counts) from ( \n'
                             'select total.Orchestra,City,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc) \n'
                             'group by city order by sum(counts)desc;')
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
    if len(values) > n:
        v_others = sum(values[n:])
        values[n:] = ''
        data[n:] = ''
        data.append('Others')
        values.append(v_others)

    print(orchestra)
    print(data)
    print(values)
    fig = plt.figure(figsize=(10, 7))
    plt.pie(values, labels=data, autopct='%1.1f%%')
    plt.show()


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

    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           'and place is not null\n'
                           'and date_of_event  between \''
                           + d3_val
                           +
                           '\' and \''
                           + d4_val
                           + '\' \n'
                             '    and pa.orchestra in '
                           + append_string
                           + '\n'
                             'group by Orchestra\n'
                             '    )\n'
                             '    group by Orchestra ),\n'
                             '\n'
                             'pageviews2 as\n'
                             '(select Orchestra,place City , count(distinct pa.event_id) counts\n'
                             'from programs_all pa\n'
                             'where place is not null\n'
                             'and date_of_event  between \''
                           + d3_val
                           +
                           '\' and \''
                           + d4_val
                           + '\' \n'
                             '    and pa.orchestra in '
                           + append_string
                           + '\n'
                             'group by Orchestra,City)\n'
                             '\n'
                             'select total.Orchestra,City,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc;')
    print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'City', 'Total-Works', 'Work-Count', 'Share'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def populate_city_list():
    """
        Loads a list of all countries
        :return: List of all countries
        """
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = '''select distinct place city from programs_all order by city ;'''
    x = cursor.execute(sqlite_select_Query)
    cities = ['Choose a City']
    for row in x:
        cities.append(row[0])
    return cities


"""
def get_charts_all_data():
    d1_val = d5.get()
    d2_val = d6.get()
    n = int(top_n3.get())
    print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()

    # print('SQL query = ', sqlite_select_Query)
    sqlite_select_Query = ('WITH total as\n'
                           '    (select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '        ,pa.event_id, count(*) counts\n'
                           '        from programs_all pa, program_list pl, mappings_csv mc\n'
                           '        where 1=1\n'
                           '        and pa.event_id = pl.event_id\n'
                           '        and pl.program = mc.link\n'
                           'and date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'
                             '        --and pa.orchestra in (\'Vienna Philharmonic\')\n'
                             '        group by Orchestra)\n'
                             '    group by Orchestra ),\n'
                             'pageviews2 as\n'
                             '    (select Orchestra, first_name||\' \'||last_name Composer, count( pa.event_id) counts\n'
                             '    from programs_all pa, program_list pl, mappings_csv mc\n'
                             '    where pa.event_id = pl.event_id\n'
                             '    and pl.program= mc.link\n'
                             'and date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'
                             '    --and pa.orchestra in (\'Vienna Philharmonic\')\n'
                             '    group by Orchestra,composer)\n'
                             '    select Composer , sum (counts) from (\n'
                             'select total.Orchestra,Composer,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc\n'
                             ')group by Composer order by sum(counts) desc \n'
                             ';')
    sqlite_select_Query = (' WITH total as\n'
                           '    (select sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '        ,pa.event_id, count(*) counts\n'
                           '        from programs_all pa, program_list pl, mappings_csv mc\n'
                           '        where 1=1\n'
                           '        and pa.event_id = pl.event_id\n'
                           '        and pl.program = mc.link\n'
                           'and date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'
                           '        group by Orchestra)\n'
                           '    ),\n'
                           '    \n'
                           'pageviews2 as\n'
                           '    (select  first_name||\' \'||last_name Composer, count( pa.event_id) counts\n'
                           '    from programs_all pa, program_list pl, mappings_csv mc\n'
                           '    where pa.event_id = pl.event_id\n'
                           '    and pl.program= mc.link\n'
                           'and date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'
                           '    group by composer)\n'
                            '    select Composer , sum (counts) from (\n'
                           'select Composer,total.total, counts ,\n'
                           '    round(((counts *1.0) /total.total)*100,2) as share\n'
                           'from pageviews2,\n'
                           '    total\n'
                           'order by share desc \n'
                           ')group by Composer order by sum(counts) desc \n')
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
    if len(values) > n:
        v_others = sum(values[n:])
        values[n:] = ''
        data[n:] = ''
        data.append('Others')
        values.append(v_others)

    print(orchestra)
    print(data)
    print(values)
    # counts = Counter(orchestra)
    # counts = [[x,orchestra.count(x)] for x in set(orchestra)]
    # print(type(counts))

    fig = plt.figure(figsize=(10, 7))
    plt.pie(values, labels=data, autopct='%1.1f%%')
    plt.show()
"""


def get_chart_orchestra_wise():
    d3_val = d3.get()
    d4_val = d4.get()
    n = int(top_n2.get()) if top_n2.get().isnumeric() else 10  ###TODO : add error catch block
    # d3_val = '1900-01-01'
    # d4_val = '1905-12-31'
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

    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           'and place is not null\n'
                           'and date_of_event  between \''
                           + d3_val
                           +
                           '\' and \''
                           + d4_val
                           + '\' \n'
                             '    and pa.orchestra in '
                           + append_string
                           + '\n'
                             'group by Orchestra\n'
                             '    )\n'
                             '    group by Orchestra ),\n'
                             '\n'
                             'pageviews2 as\n'
                             '(select Orchestra,place City , count(distinct pa.event_id) counts\n'
                             'from programs_all pa\n'
                             'where place is not null\n'
                             'and date_of_event  between \''
                           + d3_val
                           +
                           '\' and \''
                           + d4_val
                           + '\' \n'
                             '    and pa.orchestra in '
                           + append_string
                           + '\n'
                             'group by Orchestra,City)\n'
                             '\n'
                             'select City , sum(counts) from ( \n'
                             'select total.Orchestra,City,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc) \n'
                             'group by city order by sum(counts)desc;')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = []
    values = []
    i = 0
    for row in x:
        data.append(row[0])
        values.append(row[1])

    if len(values) > n:
        v_others = sum(values[n:])
        values[n:] = ''
        data[n:] = ''
        data.append('Others')
        values.append(v_others)
    print(data)
    print(values)
    # counts = Counter(orchestra)
    # counts = [[x,orchestra.count(x)] for x in set(orchestra)]
    # print(type(counts))

    fig = plt.figure(figsize=(10, 7))
    plt.pie(values, labels=data, autopct='%1.1f%%')
    plt.show()

def get_city_data():

    city = w1.get()  # GET the composer name

    cursor = sqliteConnection.cursor()

    sqlite_select_Query = (
            'select pa.orchestra,pa.event_id,pa.date_of_event, pa.place,pa.country,pl.program, c.conductor, m.title\n'
            'from programs_all pa  \n'
            'left outer join  program_list pl on pa.event_id=pl.event_id\n'
            'left outer join conductors c on pa.event_id=c.event_id\n'
            'left outer join mappings_csv m on pl.program=m.link\n'
            'where pa.place =\'' + city + '\' order by pa.date_of_event')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root,
                  headings=('Orchestra', 'Event-ID', 'Date', 'city', 'Country', 'Work abbrv.', 'Conductor', 'Work'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

def get_city_data_timewise():
    city = w2.get()  # GET the composer name#
    d5_val = d5.get()
    d6_val = d6.get()
    cursor = sqliteConnection.cursor()

    sqlite_select_Query = (
            'select pa.orchestra,pa.event_id,pa.date_of_event, pa.place,pa.country,pl.program, c.conductor, m.title\n'
            'from programs_all pa  \n'
            'left outer join  program_list pl on pa.event_id=pl.event_id\n'
            'left outer join conductors c on pa.event_id=c.event_id\n'
            'left outer join mappings_csv m on pl.program=m.link\n'
            'where pa.place =\'' + city + '\''
            'and pa.date_of_event between\'' + d5_val+ '\' and \''+ d6_val+ '\' order by pa.date_of_event'
    )
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root,
                  headings=('Orchestra', 'Event-ID', 'Date', 'city', 'Country', 'Work abbrv.', 'Conductor', 'Work'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
    return

if __name__ == '__main__':
    try:
        # sqliteConnection = sqlite3.connect('C:\\sqlite\\test_1.db')
        # sqliteConnection = sqlite3.connect('test_1.db')
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
    window.title("Orchestra Tours Data - Dr. Friedemann Pestel - City Analytics")
    window.geometry('1200x500')

    # print("Query output is")

    lbl = Label(window, text="Orchestra(s)+Cities, "
                             " within a period of choice; "
                             " results both in absolute and "
                             "\n proportional figures",
                font=('Arial Bold', 10))
    lbl.grid(column=0, row=0, columnspan=2)

    btn = Button(window, text='Fetch Query1', command=query_2)
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
    top_n = Entry(window)
    top_n.insert(END, 'Input for top X results')
    top_n.grid(column=5, row=2, sticky='W')
    btn = Button(window, text='Create Chart', command=get_chart)
    btn.grid(column=6, row=2)

    row_n = 3
    lbl2 = Label(window, text="Query_3 :: Query Orchestra-wise", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=3, sticky=E + W + S + N, rowspan=5)

    d3 = Entry(window)
    d4 = Entry(window)
    d3.grid(column=1, row=row_n, sticky='W', rowspan=5)
    d4.grid(column=2, row=row_n, sticky='W', rowspan=5)

    c1 = IntVar()
    Checkbutton(window, text="Vienna Philharmonic", variable=c1).grid(row=row_n + 4, column=3, sticky=W)
    c2 = IntVar()
    Checkbutton(window, text="Bamberg Symphony", variable=c2).grid(row=row_n, column=3, sticky=W)
    c3 = IntVar()
    Checkbutton(window, text="Philharmonia Hungarica", variable=c3).grid(row=row_n + 3, column=3, sticky=W)
    c4 = IntVar()
    Checkbutton(window, text="Gewandhaus Leipzig", variable=c4).grid(row=row_n + 2, column=3, sticky=W)
    c5 = IntVar()
    Checkbutton(window, text="Berlin Philharmonic", variable=c5).grid(row=row_n + 1, column=3, sticky=W)

    btn = Button(window, text='Fetch Query3', command=get_checkbox)
    btn.grid(column=4, row=row_n, sticky='W', rowspan=5)
    top_n2 = Entry(window)
    top_n2.insert(END, 'Input for top X results')
    top_n2.grid(column=5, row=row_n, sticky='W', rowspan=5)
    btn = Button(window, text='Get Charts', command=get_chart_orchestra_wise)
    btn.grid(column=6, row=row_n, sticky='W', rowspan=5)

    # proportionwise for all orch combined
    # row_n= 8
    # lbl2 = Label(window, text="Query_4 :: Query with date Range in format YYYY-MM-DD", borderwidth=2, relief='ridge')
    # lbl2.grid(column=0, row=row_n, sticky=E + W + S + N)

    # d5 = Entry(window)
    # d6 = Entry(window)
    # d5.grid(column=1, row=row_n, sticky='W')
    # d6.grid(column=2, row=row_n, sticky='W')
    # btn = Button(window, text='Fetch Query4', command=get_dates_all_data)
    # btn.grid(column=4, row=row_n)
    # top_n3 = Entry(window)
    # top_n3.insert(END, 'Input for top X results')
    # top_n3.grid(column=5, row=row_n, sticky='W')
    # btn = Button(window, text='Create Chart', command=get_charts_all_data)
    # btn.grid(column=6, row=row_n)

    # Part4:
    # Get COnductor name as input.
    # Produce list of all orchestras
    row_n = 9
    lbl4 = Label(window, text="")
    lbl4.grid(row=row_n, column=0, sticky=E + W + S + N)

    row_n = 10
    choices = populate_city_list()
    variable = StringVar(window)  # Creates a TKinter Variable
    variable.set(choices[0])  # set default value
    lbl3 = Label(window, text="Query the entire database for the given City", borderwidth=2, relief='ridge')
    lbl3.grid(row=row_n, column=0, sticky=E + W + S + N)
    # popupMenu = OptionMenu(window, variable, *choices)
    w1 = ttk.Combobox(window, values=choices)
    w1.grid(row=row_n, column=1)
    btn = Button(window, text='Execute', command=get_city_data)
    btn.grid(column=2, row=row_n)

    row_n = 11
    lbl4 = Label(window, text="")
    lbl4.grid(row=row_n, column=0, sticky=E + W + S + N)

    row_n = 13
    choices = populate_city_list()
    variable = StringVar(window)  # Creates a TKinter Variable
    variable.set(choices[0])  # set default value
    lbl4 = Label(window, text="Query the entire database for the given City between Time-Period", borderwidth=2, relief='ridge')
    lbl4.grid(row=row_n, column=0, sticky=E + W + S + N)
    # popupMenu = OptionMenu(window, variable, *choices)
    w2 = ttk.Combobox(window, values=choices)
    w2.grid(row=row_n, column=1)
    d5 = Entry(window)
    d6 = Entry(window)
    d5.grid(column=3, row=row_n, sticky='W')
    d6.grid(column=4, row=row_n, sticky='W')
    btn = Button(window, text='Execute', command=get_city_data_timewise)
    btn.grid(column=5, row=row_n)

    row_n = 12
    lbl3 = Label(window, text="City")
    lbl3.grid(row=row_n, column=1, sticky=N + E + W + S, columnspan=2)
    lbl3 = Label(window, text="From (YYYY-MM-DD)")
    lbl3.grid(row=row_n, column=3, sticky=N + E + W + S)
    lbl3 = Label(window, text="To (YYYY-MM-DD)")
    lbl3.grid(row=row_n, column=4, sticky=N + E + W + S)

    window.mainloop()

    sqliteConnection.close()
