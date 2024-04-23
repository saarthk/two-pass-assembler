# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:05:56 2020

@author: sarth
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog

window = tk.Tk()

# MAIN MENU

frm_buttons = tk.Frame()

icons = {
    "open": tk.PhotoImage(file="assets/open.png"),
    "save": tk.PhotoImage(file="assets/save.png"),
    "saveas": tk.PhotoImage(file="assets/saveas.png"),
    "symtab": tk.PhotoImage(file="assets/symtab.png"),
    "display": tk.PhotoImage(file="assets/display.png"),
    "refresh": tk.PhotoImage(file="assets/refresh.png"),
    "assemble": tk.PhotoImage(file="assets/assemble.png"),
    "opcode": tk.PhotoImage(file="assets/opcode.png"),
}

btn_open = tk.Button(
    master=frm_buttons, image=icons["open"], text="Open", compound=tk.TOP
)
btn_save = tk.Button(
    master=frm_buttons, image=icons["save"], text="Save", compound=tk.TOP
)
btn_save_as = tk.Button(
    master=frm_buttons, image=icons["saveas"], text="Save As", compound=tk.TOP
)
btn_symtab = tk.Button(
    master=frm_buttons, image=icons["symtab"], text="Export Tables", compound=tk.TOP
)
btn_optab = tk.Button(
    master=frm_buttons,
    image=icons["opcode"],
    text="Import Opcode Table",
    compound=tk.TOP,
)
btn_refresh = tk.Button(
    master=frm_buttons, image=icons["refresh"], text="Refresh", compound=tk.TOP
)
btn_assemble = tk.Button(
    master=frm_buttons,
    image=icons["assemble"],
    text="Save and assemble",
    compound=tk.TOP,
)

btn_open.grid(column=0, row=0, padx=2)
btn_save.grid(column=1, row=0, padx=2)
btn_save_as.grid(column=2, row=0, padx=2)
btn_refresh.grid(column=3, row=0, padx=2)
btn_optab.grid(column=4, row=0, padx=2)
btn_symtab.grid(column=5, row=0, padx=2)
btn_assemble.grid(column=6, row=0, padx=2)

# END OF MAIN MENU


# INPUT CONTAINERS

frm_edit = tk.Frame()

frm_main = tk.LabelFrame(master=frm_edit, text="Input file")
txt_main = ScrolledText(master=frm_main)

frm_output = tk.LabelFrame(master=frm_edit, text="Output file")
txt_output = ScrolledText(master=frm_output, state="disabled", bg="#d6dbdf")

frm_log = tk.LabelFrame(text="Log")
txt_log = ScrolledText(master=frm_log)
frm_log_sub = tk.Frame(master=frm_log)
chk_src = tk.Checkbutton(master=frm_log_sub, text="Source file", state=tk.DISABLED)
chk_optab = tk.Checkbutton(master=frm_log_sub, text="Opcode Table", state=tk.DISABLED)

# END OF INPUT CONTAINERS


# WIDGET PACKING

frm_buttons.pack(expand=tk.YES)

frm_main.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, padx=5, pady=10)
txt_main.pack(expand=tk.YES, fill=tk.BOTH)

frm_output.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, padx=5, pady=10)
txt_output.pack(expand=tk.YES, fill=tk.BOTH)

frm_edit.pack(expand=tk.YES)

frm_log.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=10)
txt_log.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
frm_log_sub.pack(side=tk.RIGHT, expand=tk.YES)
chk_src.pack(side=tk.TOP, expand=tk.YES)
chk_optab.pack(side=tk.TOP, expand=tk.YES)

# END OF WIDGET PACKING
