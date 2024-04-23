from gui import txt_log
import stock
import re
from numpy import isnan
from tkinter import messagebox as mb

# TODO: write pattern description for the regex
pattern = re.compile(r"=[^\d]?'?(\d+)'?")  # regex object to match operand type


def purge_path():
    stock.file_path = ""


def verify_symtab_integrity():
    """
    Checks for missing values in the symbol table, reports the errors and cleans the table for PASS#2\n
    :return: None, generates fatal error and terminates the program in case the symbol is not defined
    """
    for i in range(stock.symtable.pool_count):
        addr = stock.symtable.tab.at[i, "Address"]
        if isnan(addr):
            generate_error("SND")


def isregister(reg):
    """
    Checks if the supplied operand is a register or not\n
    :param reg: Supplied operand
    :return: boolean, indicating if the supplied operand is a register or not
    """
    try:
        stock.optable.lookup(reg, "TYPE")
    except KeyError:
        return False
    else:
        return True


def eval_operand(opnd):
    """
    Classifies a given operand into Constant, Symbol, Register or Literal. Performs auxiliary operations
    (e.g. Addition of literal to LITTAB) if required.\n
    :param opnd: Supplied operand
    :return: 'X': Type of operand
    'VAL': a number in case of a constant/register/literal/symbol indicating value/opcode/index
    """

    regx = pattern.search(opnd)
    if regx:
        literal = regx.group(1)
        stock.litable.append(literal)
        return "L", stock.litable.pool_count - 1
    elif opnd.isnumeric():
        return "C", opnd
    elif isregister(opnd):
        return "REG", stock.optable.lookup(opnd, "Opcode")
    # elif stock.optable.lookup(opnd, 'Type') == 'RG':
    #     return 'REG', stock.optable.lookup(opnd, 'Opcode')
    else:
        try:
            index = stock.symtable.lookup(opnd)
        except KeyError:
            stock.symtable.append(opnd, "Variable")
            index = stock.symtable.pool_count - 1
        return "S", index


def generate_error(msg, fatal=False):
    """
    Facilitates error generation and reporting
    :param msg: A given message, describing the error reported
    :param fatal: Flag indicating whether or not the error is fatal
    :return:
    """

    # prints the message in the program log
    txt_log.insert("%d.0" % stock.log_counter, msg + "\n")
    stock.log_counter += 1

    # routine to disable execution in case of a fatal error
    if fatal:
        mb.showwarning(
            "Program termination", "Fatal error generated, terminating program"
        )
        # call some method to terminate the assembly and save error log


def verify_token_integrity(required, available):
    """
    Verifies if the number of supplied tokens matches the number of required tokens
    :param required: Number of tokens required by the instruction
    :param available: Number of tokens supplied to the instruction
    :return: boolean, True if supplied tokens match the required tokens
    """
    if available < required:
        stock.errtable.report_error("INO")
        return False

    elif available > required:
        stock.errtable.report_error("TOO")
        return False

    return True


# TODO: Fix literal parsing
def string_parser(line):
    """
    Parses a given line to extract tokens and inform the type of instruction
    :param line: Given line to parse
    :return: boolean: True if a label is present in the line
             type of instruction
             list of tokens
    """
    if line[0] == ";":
        return False, "C", line

    tokens = re.split(r"\W+", line)
    tokens = list(filter(lambda x: x != "", tokens))

    try:
        type_U = stock.optable.tab.loc[tokens[0], "Type"]
    except KeyError:
        try:
            type_L = stock.optable.tab.loc[tokens[1], "Type"]
        except KeyError:
            stock.errtable.report_error("ILM")
            return False, "INV", []
        else:
            return True, type_L, tokens
    else:
        # insert dummy label to always get the mnemonic at index:1
        tokens.insert(0, "DUMMY LABEL")
        return False, type_U, tokens


# TODO: Potentially redundant code ahead! Refactor*


def IS_handler(mnem, tokens):
    """
    Handles imperative statements in the program
    :param mnem: Operation mnemonic
    :param tokens: A list of tokens supplied as operands to the instruction
    :return: None, all changes are made inplace
    """
    # TODO: document further code
    if verify_token_integrity(int(stock.optable.tab.at[mnem, "Operands"]), len(tokens)):

        mnem_opc = stock.optable.lookup(mnem, "Opcode")
        addr = stock.loc_counter

        stock.ictable.append(addr, "IS", mnem_opc)

        for opnd in tokens:
            cls, token_opc = eval_operand(opnd)
            stock.ictable.append(addr, cls, token_opc)

        ins_len = int(
            stock.optable.tab.at[mnem, "Length"]
        )  # fetch instruction length for that mnemonic
        stock.loc_counter += ins_len


def AD_handler(directive, tokens):
    """
    Handles directive statements in the program
    :param directive: Supplied directive
    :param tokens: Accompanying tokens
    :return: None, all changes are made inplace
    """

    # TODO: document further code
    addr = stock.loc_counter
    directive_opc = stock.optable.lookup(directive, "Opcode")
    stock.ictable.append(addr, "AD", directive_opc)

    directive = directive.casefold()

    if directive == "start":
        cls, token_opc = eval_operand(tokens[0])
        stock.ictable.append(addr, cls, token_opc)

        stock.add_start = int(token_opc)
        stock.loc_counter = stock.add_start

    elif directive == "org":
        cls, token_opc = eval_operand(tokens[0])
        stock.ictable.append(addr, cls, token_opc)

        stock.loc_counter = int(token_opc)

    # elif directive == 'equ':

    elif directive == "ltorg":
        stock.litable.fill_address()

        # TODO: Change location counter update value. Update dynamically based on instruction length
        stock.loc_counter += 1


def DL_handler(decl, tokens):
    """
    Handles declarative statements in the program
    :param decl: Declaration type (DS/DC)
    :param tokens: Accompanying tokens
    :return: None, all changes are made inplace
    """

    # TODO: document further code
    if verify_token_integrity(2, len(tokens)):
        addr = stock.loc_counter

        if decl == "DC":
            stock.symtable.fill_address(tokens[0], addr, tokens[1])
            stock.ictable.append(addr, "DL", "02")

        elif decl == "DS":
            pass

        for opnd in tokens:
            cls, token_opc = eval_operand(opnd)
            stock.ictable.append(addr, cls, token_opc)
