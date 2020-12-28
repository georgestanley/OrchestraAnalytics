"""
source: https://dev-qa.com/871565/how-to-display-table-from-database-sqlite-in-tkinter-window
"""
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk


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

'''
with sqlite3.connect('C:\\sqlite\\test_1.db') as connection:
    cursor = connection.cursor()
    cursor.execute(" WITH total as\n"
                   "    ( select Orchestra,sum(counts) as total\n"
                   "    from (select Orchestra, conductor, count(*) counts\n"
                   "from programs_all pa, conductors c\n"
                   "where pa.event_id = c.event_id\n"
                   "group by Orchestra,conductor)\n"
                   "    group by Orchestra )\n"
                   "\n"
                   "select total.Orchestra,Conductor,total.total, counts ,\n"
                   "    round(((counts *1.0) /total.total)*100,2) as share\n"
                   "from (select Orchestra, conductor, count(*) counts\n"
                   "from programs_all pa, conductors c\n"
                   "where pa.event_id = c.event_id\n"
                   "group by Orchestra,conductor) pageviews,\n"
                   "    total\n"
                   "where pageviews.Orchestra=total.Orchestra\n"
                   "order by total.Orchestra")
    data = (row for row in cursor.fetchall())
'''

root = tk.Tk()
table = Table(root, headings=('Фамилия', 'Имя', 'Отчество', 'das', 'die'), rows=data)
table.pack(expand=tk.YES, fill=tk.BOTH)

root.mainloop()
