import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
import sqlite3


# import table_demo as td

class Table(tk.Frame):
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


def query_4():
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ("WITH total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select Orchestra\n"
                           "    ,event_id, count(*) counts\n"
                           "from programs_all pa\n"
                           "where 1=1\n"
                           "group by Orchestra\n"
                           "    )\n"
                           "    group by Orchestra ),\n"
                           "\n"
                           "pageviews2 as\n"
                           "(select Orchestra, conductor, count(distinct pa.event_id) counts\n"
                           "from programs_all pa, conductors c\n"
                           "where pa.event_id = c.event_id\n"
                           "group by Orchestra,conductor)\n"
                           "\n"
                           "select total.Orchestra,Conductor,total.total, counts ,\n"
                           "    round(((counts *1.0) /total.total)*100,2) as share\n"
                           "from pageviews2,\n"
                           "    total\n"
                           "where pageviews2.Orchestra=total.Orchestra\n"
                           "order by total.Orchestra, share desc")
    cursor.execute(sqlite_select_Query)
    data = (row for row in cursor.fetchall())
    cursor.close()
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'Conductor', 'Total', 'Count', 'Share'), rows=data)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_dates():
    """
    Gets the dates and returns queery4 output filtered between the two input dates
    """
    # TODO: ADD a check clause to handle if wrong date format inputted

    d1_val = d1.get()
    d2_val = d2.get()
    print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ("WITH total as\n"
                           "    ( select Orchestra,sum(counts) as total\n"
                           "    from (select Orchestra\n"
                           "    ,event_id, count(*) counts\n"
                           "from programs_all pa\n"
                           "where 1=1\n"
                           "    and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                         "group by Orchestra\n"
                         "    )\n"
                         "    group by Orchestra ),\n"
                         "\n"
                         "pageviews2 as\n"
                         "(select Orchestra, conductor, count(distinct pa.event_id) counts\n"
                         "from programs_all pa, conductors c\n"
                         "where pa.event_id = c.event_id\n"
                        "    and date_of_event  between \'" + d1_val + "\' and \'" + d2_val + "\' \n"
                         "group by Orchestra,conductor)\n"
                         "\n"
                         "select total.Orchestra,Conductor,total.total, counts ,\n"
                         "    round(((counts *1.0) /total.total)*100,2) as share\n"
                         "from pageviews2,\n"
                         "    total\n"
                         "where pageviews2.Orchestra=total.Orchestra\n"
                         "order by total.Orchestra, share desc")
    print('SQL query = ', sqlite_select_Query)
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
    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra, conductor, count(*) counts\n'
                           'from programs_all pa, conductors c\n'
                           'where pa.event_id = c.event_id\n'
                           'and date_of_event  between \'' + d1_val +
                           # '1900-01-01\' '
                           '\' and \'' + d2_val +
                           # '1920-01-01\'\n'
                           '\' group by Orchestra,conductor)\n'
                           '    group by Orchestra )\n'
                           '\n'
                           'select total.Orchestra,Conductor,total.total, counts ,\n'
                           '    round(((counts *1.0) /total.total)*100,2) as share\n'
                           'from (select Orchestra, conductor, count(*) counts\n'
                           'from programs_all pa, conductors c\n'
                           'where pa.event_id = c.event_id\n'
                           'group by Orchestra,conductor) pageviews,\n'
                           '    total\n'
                           'where pageviews.Orchestra=total.Orchestra\n'
                           'order by total.Orchestra;'
                           )
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
    sqlite_select_Query = ('\n'
                           'WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra, conductor, count(*) counts\n'
                           '        from programs_all pa, conductors c\n'
                           '        where pa.event_id = c.event_id\n'
                           '        and orchestra in '+append_string+'\n'
                           '        and date_of_event  between \''+d3_val+'\' and \''+d4_val+'\' \n'
                           '        group by Orchestra,conductor)\n'
                           '    group by Orchestra )\n'
                           '\n'
                           'select total.Orchestra,Conductor,total.total, counts ,\n'
                           '    round(((counts *1.0) /total.total)*100,2) as share\n'
                           'from (select Orchestra, conductor, count(*) counts\n'
                           '    from programs_all pa, conductors c\n'
                           '    where pa.event_id = c.event_id\n'
                            '        and orchestra in '+append_string+'\n'
                           '        and date_of_event  between \''+d3_val+'\' and \''+d4_val+'\' \n'
                           'group by Orchestra,conductor) pageviews,\n'
                           '    total\n'
                           'where pageviews.Orchestra=total.Orchestra\n'
                           'order by total.Orchestra,counts desc'
                           )
    sqlite_select_Query = ('WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,event_id, count(*) counts\n'
                           'from programs_all pa\n'
                           'where 1=1\n'
                           '        and date_of_event  between \''+d3_val+'\' and \''+d4_val+'\' \n'
                           '        and orchestra in '+append_string+'\n'
                           'group by Orchestra\n'
                           '    )\n'
                           '    group by Orchestra),\n'
                           '\n'
                           'pageviews2 as\n'
                           '(select Orchestra, conductor, count(distinct pa.event_id) counts\n'
                           'from programs_all pa, conductors c\n'
                           'where pa.event_id = c.event_id\n'
                           '        and date_of_event  between \''+d3_val+'\' and \''+d4_val+'\' \n'
                           '        and orchestra in '+append_string+'\n'
                           'group by Orchestra,conductor)\n'
                           '\n'
                           'select total.Orchestra,Conductor,total.total, counts ,\n'
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
    table = Table(root, headings=('Orchestra', 'Conductor', 'Total', 'Count', 'Share'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

def populate_conductor_list():
    """
        Loads a list of all countries
        :return: List of all countries
        """
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = '''select distinct conductor from conductors order by conductor;'''
    x = cursor.execute(sqlite_select_Query)
    conductors = ['Choose a Conductor']
    for row in x:
        conductors.append(row[0])
    return conductors

def get_conductor_data():
    # TODO: replace the sql query to obtain conductors data

    conductor = variable.get()  # GET the country name
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = (
        'select pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra,group_concat(pl.program) program, group_concat(distinct c.conductor) conductor\n'
        ' from programs_all pa \n'
        '     left  join program_list pl on pa.event_id=pl.event_id\n'
        '     left  join conductors c on pa.event_id=c.event_id\n'
        'where 1=1\n'
        'and c.conductor =\''+conductor+'\'\n'
        'group by pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra')
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
    try:
        ##sqliteConnection = sqlite3.connect('C:\\sqlite\\test_1.db')
        sqliteConnection = sqlite3.connect('test_1.db')
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
    window.title("Orchestra Tours Data - Dr. Friedemann Pestel")
    window.geometry('1000x500')

    # print("Query output is")

    lbl = Label(window, text="Orchestra(s)+conductor, "
                             " within a period of choice; "
                             " results both in absolute and "
                             "\n proportional figures",
                font=('Arial Bold', 10))
    lbl.grid(column=0, row=0, columnspan=2)

    btn = Button(window, text='Fetch Query1', command=query_4)
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

    #
    row_n=3
    lbl2 = Label(window, text="Query_3 :: Query Orchestra-wise", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=row_n, sticky=E + W + S + N, rowspan=5)
    d3 = Entry(window)
    d4 = Entry(window)
    d3.grid(column=1, row=row_n, sticky='W', rowspan=5)
    d4.grid(column=2, row=row_n, sticky='W', rowspan=5)

    c1 = IntVar()
    Checkbutton(window, text="Vienna Philharmonic", variable=c1).grid(row=row_n+4, column=4, sticky=W)
    c2 = IntVar()
    Checkbutton(window, text="Bamberg Symphony", variable=c2).grid(row=row_n, column=4, sticky=W)
    c3 = IntVar()
    Checkbutton(window, text="Philharmonia Hungarica", variable=c3).grid(row=row_n+3, column=4, sticky=W)
    c4 = IntVar()
    Checkbutton(window, text="Gewandhaus Leipzig", variable=c4).grid(row=row_n+2, column=4, sticky=W)
    c5 = IntVar()
    Checkbutton(window, text="Berlin Philharmonic", variable=c5).grid(row=row_n+1, column=4, sticky=W)

    btn = Button(window, text='Fetch Query3', command=get_checkbox)
    btn.grid(column=3, row=3, rowspan=5)

    # Part4:
    # Get COnductor name as input.
    # Produce list of all orchestras

    row_n = 8
    choices = populate_conductor_list()
    variable = StringVar(window)  # Creates a TKinter Variable
    variable.set(choices[0])  # set default value
    lbl3 = Label(window, text="Query the entire database for the given Conductor")
    lbl3.grid(row=row_n, column=0)
    popupMenu = OptionMenu(window, variable, *choices)
    popupMenu.grid(row=row_n, column=1)
    btn = Button(window, text='Execute', command=get_conductor_data)
    btn.grid(column=2, row=row_n)

    window.mainloop()

    sqliteConnection.close()
