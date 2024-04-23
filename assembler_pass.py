import stock as s
import modules as md
import re


def pass_one():
    with open(file=s.file_path, mode="r", encoding="utf-8") as f:
        for line in f:
            is_lbl, ins_typ, tokens = md.string_parser(line)

            if ins_typ == "C":
                continue
            elif is_lbl:
                try:
                    s.symtable.lookup(tokens[0])
                except KeyError:
                    s.symtable.append(tokens[0], "Block Label", address=s.loc_counter)
                    s.ictable.append(s.loc_counter, "S", s.symtable.pool_count - 1)
                else:
                    s.errtable.report_error("DS")

            elif ins_typ == "INV":
                s.errtable.report_error("ILM")
                continue

            # TODO: Remove redundancy*
            if ins_typ == "IS":
                md.IS_handler(tokens[1], tokens[2:])
            elif ins_typ == "AD":
                md.AD_handler(tokens[1], tokens[2:])
            elif ins_typ == "DL":
                md.DL_handler(tokens[1], tokens[2:])

        s.litable.fill_address()
        md.verify_symtab_integrity()
        s.ictable.write_to_file(s.ic_file_path)


def pass_two():
    IS_MATCH = re.compile(r"IS\W*(\d+)")
    AD_MATCH = re.compile(r"AD\W0*3")

    REG_PAT = re.compile(r"RG\W*(\d+)")
    SYM_PAT = re.compile(r"[^I]S\W*(\d+)")
    LIT_PAT = re.compile(r"L\W*(\d+)")
    CONS_PAT = re.compile(r"C\W*(\d+)")

    with open(file=s.ic_file_path, mode="r", encoding="utf-8") as f:
        with open(file=s.output_file_path, mode="w+", encoding="utf-8") as out_f:
            for line in f:
                out_line = ""

                if IS_MATCH.search(line):
                    opc = IS_MATCH.search(line).group(1)
                    out_line += "{0} ".format(opc)

                    # moves iterator from beginning of the string to the end of (IS, xx) instruction
                    for st in IS_MATCH.finditer(line):
                        pass
                    line = line[st.end() :]

                    regs = REG_PAT.findall(
                        line
                    )  # 'regs' is a list of numbers which match the regex pattern for registers
                    if regs:
                        # append 'xx' from (RG, xx) statement to the output line
                        out_line += "{0} ".format(regs[0])
                    if not regs:
                        # in case a register is not one of the operands, append '00' to the output line
                        out_line += "00 "

                    syms = SYM_PAT.findall(line)  # similar to 'regs'
                    # if the IC line contains symbols, for each symbol,
                    # append its corresponding address from SYMTAB to the output line
                    for sym_index in syms:

                        sym_addr = s.symtable.tab.loc[int(sym_index), "Address"]
                        out_line += "{0} ".format(sym_addr)

                    lits = LIT_PAT.findall(line)  # similar to 'regs'
                    # if the IC line contains literals, for each literal,
                    # append its corresponding address from LITTAB to the output line
                    for lit_index in lits:

                        lit_addr = s.litable.loc[int(lit_index), "Address"]
                        out_line += "{0} ".format(lit_addr)

                    cons = CONS_PAT.findall(line)  # similar to 'regs'
                    # if the IC line contains constants, for each constant,
                    # append its corresponding value to the output line
                    for con in cons:
                        out_line += "{0} ".format(con)

                elif AD_MATCH.search(line):
                    # print("LTORG Assembler Directive")
                    #
                    out_line += "00 00 "

                    cons = CONS_PAT.findall(line)
                    for con in cons:
                        out_line += "{0} ".format(con)

                # print(out_line)
                if out_line:
                    out_f.write(out_line + "\n")
