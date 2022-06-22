from tkinter import *
import tkinter as tk
import os


# from SqlConnection import sqliteConnection

def service_func():
    print('service func')


def get_Q1():
    # exec(open('Query1.py').read())
    os.startfile("Query1.exe")


def get_Q2():
    os.startfile("dist/Query2.exe")


def get_Q3():
    os.startfile("D:\\Friedemann\\OrchestraAnalytics\\dist\\Query3.exe")


def get_Q4():
    os.startfile("dist/Query4.exe")


def get_Q5():
    os.startfile("dist/query5.exe")


def get_Q6():
    os.startfile("dist/Query6.exe")


def get_Q7():
    os.startfile("dist/Query7.exe")


def get_Q8():
    os.startfile("dist/Query8.exe")


def get_Q9():
    os.startfile("dist/Query9.exe")


def get_Q10():
    os.startfile("dist/Query10.exe")


if __name__ == '__main__':
    service_func()

    window = tk.Tk()
    window.title("Orchestra Tours Data - Dr. Friedemann Pestel")
    window.geometry('1000x700')

    btn1 = Button(window, text='1. Orchestra(s)+country', height=7, width=60, command=get_Q1)
    btn1.grid(column=1, row=1)

    btn2 = Button(window, text='2.	Orchestra(s)+city', height=7, width=60, command=get_Q2)
    btn2.grid(column=2, row=1)
    # row2
    btn3 = Button(window, text='3.	Orchestra(s)+continent', height=7, width=60, command=get_Q3)
    btn3.grid(column=1, row=2)
    btn4 = Button(window, text='4.	Orchestra(s)+conductor', height=7, width=60, command=get_Q4)
    btn4.grid(column=2, row=2)
    # row3
    btn5 = Button(window, text='5.	Orchestra(s)+composer', height=7, width=60, command=get_Q5)
    btn5.grid(column=1, row=3)
    btn6 = Button(window, text='6.	Orchestra(s)+work', height=7, width=60, command=get_Q6)
    btn6.grid(column=2, row=3)
    # row4
    btn7 = Button(window, text='7.	Orchestra(s)+nationality of composers', height=7, width=60, command=get_Q7)
    btn7.grid(column=1, row=4)
    btn8 = Button(window, text='8.	Orchestra(s)+average age of works', height=7, width=60, command=get_Q8)
    btn8.grid(column=2, row=4)
    # row5
    btn9 = Button(window, text='9.Orchestra(s)+proportion of works 50 years and younger ', height=7, width=60,
                  command=get_Q9)
    btn9.grid(column=1, row=5)
    btn10 = Button(window, text='10.Orchestra(s)+proportion of works 30 years and younger ', height=7, width=60,
                   command=get_Q10)
    btn10.grid(column=2, row=5)

    window.mainloop()
