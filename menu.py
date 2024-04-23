# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 02:26:13 2020

@author: sarth
"""

import gui
import assembler_pass
import tables
import stock
import modules
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
import pandas as pd


def clean():
    with open(stock.file_path, mode="r+", encoding="utf-8") as f:
        f_c = f.read().rstrip("\n")
    with open(stock.file_path, mode="w", encoding="utf-8") as f:
        f.write(f_c)


def save_file():
    try:
        with open(stock.file_path, mode="w", encoding="utf-8") as f:
            f.write(gui.txt_main.get("1.0", tk.END))
        clean()

    except FileNotFoundError:
        mb.showwarning("Error", "No file currently opened")


def save_as():
    try:
        path = filedialog.asksaveasfilename()
        if path == "":
            raise FileNotFoundError
        else:
            stock.file_path = path
            save_file()
            gui.frm_main.config(text=stock.file_path)

    except FileNotFoundError:
        mb.showwarning("Error", "Locate a valid file to save")


def refresh():
    try:
        with open(stock.file_path, mode="r", encoding="utf-8") as f:
            gui.frm_main.config(text=f.name)
            gui.txt_main.delete("1.0", tk.END)

            l = 1
            for line in f:
                gui.txt_main.insert("%d.0" % l, line + "\n")
                l += 1

    except FileNotFoundError:
        mb.showerror("Error", "No file currently opened")
        gui.chk_src.deselect()


def open_file():
    try:
        path = filedialog.askopenfilename()
        if path == "":
            raise FileNotFoundError
        else:
            stock.file_path = path
            refresh()

            stock.src_loaded = True

            gui.chk_src.select()

            modules.generate_error("Source file loaded!")

    except FileNotFoundError:
        stock.src_loaded = False
        mb.showwarning("Error", "Locate a valid file to open")


def import_optab():
    try:
        path = filedialog.askopenfilename()
        if path == "":
            raise FileNotFoundError

        stock.optable = tables.optab(path)

        gui.chk_optab.select()

        stock.optable_loaded = True

        modules.generate_error("Machine Opcode Table loaded!")

    except (FileNotFoundError, KeyError):
        gui.chk_optab.deselect()
        stock.optable_loaded = False
        mb.showwarning("Error", "Locate a valid file to load")


def export_tables():
    try:
        path = filedialog.asksaveasfilename(
            title="Symbol Table save location", defaultextension=".csv"
        )

        if path == "":
            raise FileNotFoundError

        stock.symtable.to_csv(path)

        modules.generate_error("Symbol Table saved to: %s" % path)

    except FileNotFoundError:
        mb.showwarning("Error", "Choose a valid directory")
        modules.generate_error("Symbol Table not exported")

    try:
        path = filedialog.asksaveasfilename(
            title="Literal Table save location", defaultextension=".csv"
        )

        if path == "":
            raise FileNotFoundError

        stock.litable.to_csv(path)

        modules.generate_error("Literal Table saved to: %s" % path)

    except FileNotFoundError:
        mb.showwarning("Error", "Choose a valid directory")
        modules.generate_error("Literal Table not exported")


class SourceNotLoadedError(Exception):
    """
    Custom error to signal that source file is not loaded prior to assembly
    """

    pass


class OptabNotLoadedError(Exception):
    """
    Custom error to signal that OPTAB is not loaded prior to assembly
    """

    pass


def save_and_assemble():
    try:
        if not stock.src_loaded:
            raise SourceNotLoadedError
        if not stock.optable_loaded:
            raise OptabNotLoadedError

        assembler_pass.pass_one()
        assembler_pass.pass_two()

        with open(stock.output_file_path, mode="r", encoding="utf-8") as f:
            gui.frm_output.config(text=f.name)
            gui.txt_output.delete("1.0", tk.END)

            l = 1
            for line in f:
                gui.txt_output.insert("%d.0" % l, line + "\n")
                l += 1

    except SourceNotLoadedError:
        modules.generate_error("Source file not loaded")
    except OptabNotLoadedError:
        modules.generate_error("Opcode table not loaded")
    except KeyError:
        modules.generate_error("Invalid path for IC table")
    # except:
    #     modules.generate_error("Assembly unsuccessful. Check input for errors")
    else:
        modules.generate_error("Assembly successful")


gui.btn_open.config(command=open_file)
gui.btn_save.config(command=save_file)
gui.btn_refresh.config(command=refresh)
gui.btn_save_as.config(command=save_as)
gui.btn_optab.config(command=import_optab)
gui.btn_symtab.config(command=export_tables)
gui.btn_assemble.config(command=save_and_assemble)
