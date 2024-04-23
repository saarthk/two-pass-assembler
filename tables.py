import pandas as pd
from numpy import NaN, isnan
from _collections import defaultdict


class optab:
    """
    Manages the OPTAB for the program
    """

    tab = pd.DataFrame()  # table attribute

    def __init__(self, path):
        self.tab = pd.read_csv(path, dtype="str").set_index("Mnemonic")

    def lookup(self, key, col):
        """
        Looks for an attribute(stored in col) for a particular mnemonic\n
        Raises KeyError in case the requested mnemonic is absent\n
        :param key: Requested mnemonic
        :param col: Attribute (e.g. Operands, Length, Opcode) to be accessed
        :return: Value of the attribute for the requested mnemonic
        """
        return self.tab.loc[key, col]


class littab:
    """
    Manages the LITTAB for the program
    """

    tab = pd.DataFrame(columns=["Literal", "Address"])  # table attribute
    pool_count = 0  # counter to keep track of the number of entries

    def append(self, literal, address=NaN):
        """
        Wrapper around pandas DataFrame.append() method to populate Literal Table using program output\n
        :param literal: Literal to be added
        :param address: Address of the literal, default is NaN to indicate missing address
        :return: None, all changes are made inplace
        """
        self.tab = self.tab.append(
            {"Literal": literal, "Address": address}, ignore_index=True
        )
        self.pool_count += 1

    def fill_address(self):
        """
        Fills missing addresses upon signal by the LTORG/END statement\n
        IC table is updated with corresponding intermediate code\n
        Assignments are made incrementally starting from current value of location counter\n
        :return: None, all assignments are made inplace
        """
        from stock import (
            loc_counter,
            ictable,
        )  # Importing deferred to avoid circular imports

        for i in range(self.pool_count):
            if isnan(self.tab.at[i, "Address"]):
                self.tab.at[i, "Address"] = loc_counter

                # TODO: Patch the quick-fix- LTORG is explicitly assigned to 03, DC is explicitly assigned to 02
                ictable.append(loc_counter, "AD", "03")
                ictable.append(loc_counter, "DL", "02")
                ictable.append(loc_counter, "C", self.tab.loc[i, "Literal"])

                # TODO: Update location counter dynamically, depending upon instruction length
                loc_counter += 1

    def lookup(self, literal):
        """
        Queries the table for presence of the requested symbol\n
        :param literal: Requested literal
        :return: index value if the literal is present in the table, else raises KeyError
        """
        index = self.tab.loc[self.tab["Literal"] == literal].index.tolist()
        if index:
            return index[0]
        raise KeyError

    def verify(self):
        """
        Verifies the table for missing addresses\n
        :return: boolean, indicating a fully-filled/unfilled table
        """
        for i in range(self.pool_count):
            if isnan(self.tab.at[i, "Address"]):
                return False
        return True

    def display_tab(self):
        """
        Pretty prints the table
        :return: None
        """
        print(self.tab)


class symtab:
    """
    Manages the SYMTAB for the program
    """

    tab = pd.DataFrame(
        columns=["Symbol", "Type", "Value", "Address"]
    )  # table attribute
    pool_count = 0  # counter to keep track of the number of entries

    def append(self, symbol, typ, value=NaN, address=NaN):
        """
        Wrapper around the pandas DataFrame.append() method to populate the Symbol Table using program output\n
        :param symbol: Symbol to be stored
        :param typ: Type of the symbol
        :param value: Value, in case of a Variable
        :param address: Address of the symbol
        :return: None, all changes are made inplace
        """
        self.tab = self.tab.append(
            {"Symbol": symbol, "Type": typ, "Value": value, "Address": address},
            ignore_index=True,
        )
        self.pool_count += 1

    def fill_address(self, symbol, address, value):
        """
        Fills the address and value of a Variable in case of forward referencing\n
        Creates a new entry in SYMTAB in case of no prior description (no forward referencing)\n
        :param symbol: Requested symbol
        :param address: Address to be added
        :param value: Value of the variable
        :return: None, all changes are made inplace
        """

        try:
            index = self.lookup(symbol)
        except KeyError:
            self.append(symbol, "Variable", value, address)
        else:
            self.tab.loc[index, "Address"] = address
            self.tab.loc[index, "Value"] = value

    def lookup(self, symbol):
        """
        Queries the table for presence of the requested symbol\n
        :param symbol: Requested symbol
        :return: index value if the symbol is present in the table, else raises KeyError
        """
        index = self.tab.loc[self.tab["Symbol"] == symbol].index.tolist()
        if index:
            return index[0]
        raise KeyError

    def display_tab(self):
        print(self.tab)


class errtab:
    """
    Defines and manages the Error Table for the program
    """

    tab = pd.DataFrame()

    def __init__(self, path):
        self.tab = pd.read_csv(path).set_index("Key")

    # TODO: Minor changes to reporting mechanism
    def report_error(self, key):
        """
        Verbosely describes an error, given a key and determines if fatal\n
        :param key: A key which abbreviates a particular error
        :return: A full description of the error along with a flag for fatal/non-fatal indication
        """
        dsc, ftl = self.tab.loc[key]
        return dsc, ftl


class intercodetab:
    """
    Manages the intermediate code as a DataFrame object
    """

    # IC Table implementation using 'defaultdict'
    # Orphan addresses are assigned a list by default using a lambda function
    tab = defaultdict(lambda: [])

    def remove_addr(self, address):
        """
        Removes the given address if present
        :param address: Address to be removed
        :return:
        """
        try:
            del self.tab[address]
        except KeyError:
            pass

    def append(self, address, a, b):
        """
        Appends the tuple (a, b) to a particular address. Creates new address if given address doesn't already exist
        :param address: Address to be appended
        :param a: First tuple parameter
        :param b: Second tuple parameter
        :return:
        """
        self.tab[address].append((a, b))

    def write_to_file(self, path):
        with open(file=path, mode="w+", encoding="utf-8") as f:
            for addr, contents in self.tab.items():
                out_line = r"{address}: {token}".format(
                    address=addr, token=str(contents).strip("[]")
                )
                f.write(out_line + "\n")
