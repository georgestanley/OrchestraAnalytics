from tkinter import *
import tkinter as tk
import Query1

def get_Q1():
    exec(open('Query1.py').read())

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Homepage")
    window.geometry('1000x700')
    btn1 = Button(window, text='1. Orchestra(s)+country', height=7, width=60, command=get_Q1)
    btn1.grid(column=1, row=1)
    window.mainloop()
