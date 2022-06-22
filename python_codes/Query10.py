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


def query_10():
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('with q1 as (\n'
                           'select orchestra, count(*) total_events from (\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,'
                           '  date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link)\n'
                           'group by orchestra\n'
                           ')\n'
                           ',q2 as (\n'
                           'select orchestra, count(*) total_underage_events from (\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  '
                           'date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and age <=30)\n'
                           'group by orchestra\n'
                           ')\n'
                           'select q1.orchestra ,q1.total_events, q2.total_underage_events,  '
                           'round (((q2.total_underage_events*1.0) / q1.total_events ) *100,2) percent\n'
                           'from q1, q2\n'
                           'where q1.orchestra=q2.orchestra')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    data = (row for row in cursor.fetchall())
    cursor.close()
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'Total Works played', 'Works below 30 yrs', 'Percentage'), rows=data)
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
    sqlite_select_Query = ('with q1 as (\n'
                           'select orchestra, count(*) total_events from (\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  '
                           'date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and pa.date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'     
                           ')\n'
                           'group by orchestra\n'
                           ')\n'
                           ',q2 as (\n'
                           'select orchestra, count(*) total_underage_events from (\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  '
                           'date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and age <=30\n'
                           'and pa.date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'
                           ')\n'
                           'group by orchestra\n'
                           ')\n'
                           'select q1.orchestra ,q1.total_events, q2.total_underage_events,  '
                           'round (((q2.total_underage_events*1.0) / q1.total_events ) *100,2) percent\n'
                           'from q1, q2\n'
                           'where q1.orchestra=q2.orchestra')
    print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Orchestra', 'Total Works played', 'Works below 30 yrs', 'Percentage'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_dates_csv():
    d1_val = d1.get()
    d2_val = d2.get()
    # print('d1 =', d1_val, 'd2=', d2_val)
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('with q1 as (\n'
                           'select orchestra, count(*) total_events from (\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  '
                           'date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and pa.date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'     
                           ')\n'
                           'group by orchestra\n'
                           ')\n'
                           ',q2 as (\n'
                           'select orchestra, count(*) total_underage_events from (\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  '
                           'date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and age <=30\n'
                           'and pa.date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'
                           ')\n'
                           'group by orchestra\n'
                           ')\n'
                           'select q1.orchestra ,q1.total_events, q2.total_underage_events,  '
                           'round (((q2.total_underage_events*1.0) / q1.total_events ) *100,2) percent\n'
                           'from q1, q2\n'
                           'where q1.orchestra=q2.orchestra')

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

    # print('SQL query = ', sqlite_select_Query)

    sqlite_select_Query = ('select orchestra, round(avg(age),2) from\n'
                           '(\n'
                           'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  date_of_event -mc.composition_or_premiere_date age\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and pa.date_of_event  between \''
                           + d1_val
                           +
                           '\' and \''
                           + d2_val
                           + '\' \n'                           ')\n'
                             'group by orchestra')
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
    plt.bar(data, values , width = 0.5)
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


    sqlite_select_Query = (
        'select pa.orchestra, pa.date_of_event,pl.program, mc.composition_or_premiere_date,  date_of_event -mc.composition_or_premiere_date age\n'
        'from programs_all pa, program_list pl, mappings_csv mc\n'
        'where 1=1\n'
        'and pa.event_id = pl.event_id\n'
        'and pl.program=mc.link\n'
        'and age <=30\n'
        'and pa.date_of_event  between \''+d3_val+'\' and \''+d4_val+'\' \n'
        'and pa.orchestra in' + append_string  )
    print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=('Orchestra','Date of Event', 'Work', 'Compositon year', 'Age'), rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


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

    sqlite_select_Query = ('\n'
                           'WITH total as\n'
                           '    ( select Orchestra,sum(counts) as total\n'
                           '    from (select Orchestra\n'
                           '    ,pa.event_id, count(*) counts\n'
                           'from programs_all pa, program_list pl\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pa.date_of_event  between \''
                           + d3_val
                           +
                           '\' and \''
                           + d4_val
                           + '\' \n'
                             '    and pa.orchestra in '
                           + append_string
                           + '\n'                           'group by Orchestra\n'
                             '    )\n'
                             '    group by Orchestra ),\n'
                             '\n'
                             'pageviews2 as\n'
                             '(select Orchestra,mc.Nationality , count(*) counts\n'
                             'from programs_all pa, program_list pl left outer join mappings_csv mc on pl.program=mc.link\n'
                             'where pa.event_id = pl.event_id\n'
                             'and pa.date_of_event  between \''
                           + d3_val
                           +
                           '\' and \''
                           + d4_val
                           + '\' \n'
                             '    and pa.orchestra in '
                           + append_string
                           + '\n'                           'group by Orchestra,Nationality\n'
                             ')\n'
                             '\n'
                             '\n'
                             'select Nationality,sum(counts) from ('
                             'select total.Orchestra,Nationality,total.total, counts ,\n'
                             '    round(((counts *1.0) /total.total)*100,2) as share\n'
                             'from pageviews2,\n'
                             '    total\n'
                             'where pageviews2.Orchestra=total.Orchestra\n'
                             'order by total.Orchestra, share desc)\n group by nationality order by sum(counts) desc'
                             ';')
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


def populate_country_list():
    """
        Loads a list of all countries
        :return: List of all countries
        """
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = '''select distinct  nationality from mappings_csv order by nationality ;'''
    x = cursor.execute(sqlite_select_Query)
    conductors = ['Choose a Country']
    for row in x:
        conductors.append(row[0])
    return conductors


def get_nationality_data():
    # TODO: replace the sql query to obtain conductors data

    country = popupMenu.get()  # GET the composer name
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = (
        'select pa.*, mc.last_name || \' \'||mc.first_name composer, pl.program,mc.Genre,mc.composition_or_premiere_date\n'
        'from programs_all pa, program_list pl, mappings_csv mc\n'
        'where 1=1\n'
        'and pa.event_id = pl.event_id\n'
        'and pl.program=mc.link\n'
        'and mc.Nationality = \'' + country + '\'')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=(
        'Event-ID', 'Date', 'Country', 'City', 'Orchestra', 'Composer', 'Program', 'Genre', 'Composition/premiere Year'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


def get_validation_result():
    ### not needed.
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = ('select a.event_id,a.program,b.orchestra,b.date_of_event from (\n'
                           'select * from program_list where lower(program) not in (select lower(link) from mappings_csv))a , programs_all b\n'
                           'where a.event_id=b.event_id')
    print(sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root, headings=(
        'Event-ID', 'Program', 'Orchestra', 'Date'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

def get_composer_data_datewise():
    country = popupMenu2.get()  # GET the composer name
    d3_val = d5.get()
    d4_val = d6.get()
    var1 = c6.get()
    var2 = c7.get()
    var3 = c8.get()
    var4 = c9.get()
    var5 = c10.get()
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

    sqlite_select_Query = ('select pa.*, mc.last_name ||\'' '\'||mc.first_name composer, pl.program,mc.Genre,mc.composition_or_premiere_date\n'
                           'from programs_all pa, program_list pl, mappings_csv mc\n'
                           'where 1=1\n'
                           'and pa.event_id = pl.event_id\n'
                           'and pl.program=mc.link\n'
                           'and mc.nationality = \''+country+'\' \n'
                           'and pa.date_of_event between \''+d3_val+'\' and \''+d4_val+'\''
                           'and pa.orchestra in '+append_string+''
                           )
    print('SQL query = ', sqlite_select_Query)
    cursor.execute(sqlite_select_Query)
    x = cursor.fetchall()
    data = (row for row in x)
    root = tk.Tk()
    table = Table(root,
                  headings=('Event-ID', 'Date', 'Country', 'City', 'Orchestra', 'Composer', 'Program', 'Genre', 'Composition/premiere Year'),
                  rows=data)
    # print('record count =', type(data))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()



if __name__ == '__main__':
    try:
        ##sqliteConnection = sqlite3.connect('C:\\sqlite\\test_1.db')
        ##sqliteConnection = sqlite3.connect('test_1.db')
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
    window.title("Composer-Nationality Analytics")
    window.geometry('1200x500')

    # print("Query output is")

    lbl = Label(window, text="Orchestra(s)+proportion of works 30 years "
                             "and younger \n at the date they were "
                             "performed within the chosen time period",
                font=('Arial Bold', 10))
    lbl.grid(column=0, row=0, columnspan=2)

    btn = Button(window, text='Fetch Query1', command=query_10)
    btn.grid(column=1, row=1)

    lbl2 = Label(window, text="Query_1 :: Query whole database", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=1, sticky=E + W + S + N)

    lbl2 = Label(window, text="")
    lbl2.grid(column=0, row=2, sticky=E + W + S + N)
    row_n = 3
    lbl2 = Label(window, text="From")
    lbl2.grid(column=1, row=row_n)
    lbl2 = Label(window, text="To")
    lbl2.grid(column=2, row=row_n)


    row_n =4
    lbl2 = Label(window, text="Query_2 :: Query with date Range in format YYYY-MM-DD", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=row_n, sticky=E + W + S + N)

    d1 = Entry(window , width=20)
    d2 = Entry(window , width=20)
    d1.grid(column=1, row=row_n,  padx = 20 )
    d2.grid(column=2, row=row_n, padx = 20 )
    btn = Button(window, text='Fetch Query2', command=get_dates)
    btn.grid(column=3, row=row_n)
    btn = Button(window, text='Download as CSV', command=get_dates_csv)
    btn.grid(column=4, row=row_n)


    row_n = 5
    lbl2 = Label(window, text="", borderwidth=2)
    lbl2.grid(column=0, row=row_n, sticky=E + W + S + N)

    row_n = 6
    lbl2 = Label(window, text="Query_3::View List of events", borderwidth=2, relief='ridge')
    lbl2.grid(column=0, row=row_n, sticky=E + W + S + N)

    d3 = Entry(window)
    d4 = Entry(window)
    d3.grid(column=1, row=row_n, sticky='W')
    d4.grid(column=2, row=row_n, sticky='W')
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

    window.mainloop()
    sqliteConnection.close()
