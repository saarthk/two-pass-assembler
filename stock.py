# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:27:20 2020

@author: sarth
"""

import tables

# counters
# TODO: Change location counter value to default
loc_counter = 0
log_counter = 1
# end of counters

# global variables
# TODO: Change file path to default
file_path = "sample_input.txt"
output_file_path = "output.txt"
ic_file_path = "ic.txt"
optable = tables.optab("optab.csv")
symtable = tables.symtab()  # {'Man':[1,2], 'Woman':[3,4]}
litable = tables.littab()
errtable = tables.errtab("err.csv")
ictable = tables.intercodetab()
# end of global variables

# flags
src_loaded = False
optable_loaded = False
# end of flags

# miscellaneous
add_start = 0
# end of miscellaneous
