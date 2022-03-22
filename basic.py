from sys import *
import time

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
    if ".scor" in filename:
        data = open(filename, "r").read()
        data += "<EOF>"
        return data
    else:
        print("FILE ERROR: No file with that name")
        time.sleep(5)
        exit()

def lex(filecontents):
    state = 0
    isexpr = 0
    varstarted = 0
    tok = ""
    string = ""
    expr = ""
    n = ""
    var = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tok = ""
        elif tok == "!" and state == 0:
            tokens.append("NOT")
            tok = ""
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            elif tokens[-2] == "NOT":
                tokens[-2] = "NOTEQ"
            else:
                tokens.append("EQUALS")
            tok = ""
        elif tok == "$" and state == 0:
            varstarted = 1
            var += tok
            tok = ""
        elif varstarted == 1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    varstarted = 0
            var += tok
            tok = ""
        elif tok == "PRINT" or tok == "print":
            tokens.append("PRINT")
            tok = ""
        elif tok == "INPUT" or tok == "input":
            tokens.append("INPUT")
            tok = ""
        elif tok == "ENDIF" or tok == "endif":
            tokens.append("ENDIF")
            tok = ""
        elif tok == "IF" or tok == "if":
            tokens.append("IF")
            tok = ""
        elif tok == "THEN" or tok == "then":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tokens.append("THEN")
            tok = ""
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\t":
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    print(tokens)
    #return ""
    return tokens

def evalExpression(expr):
    return eval(expr)

def doPRINT(toPRINT):
    if(toPRINT[0:6] == "STRING"):
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif(toPRINT[0:3] == "NUM"):
        toPRINT = toPRINT[4:]
    elif(toPRINT[0:4] == "EXPR"):
        toPRINT = evalExpression(toPRINT[5:])
    print(toPRINT)

def doASSIGN(varname, varvalue):
    symbols[varname[4:]] = varvalue

def getVARIABLE(varname):
    varname = varname[4:]
    if varname in symbols:
        return symbols[varname]
    else:
        return "VARIABLE ERROR: Undefined Variable"
        exit()

def getINPUT(string, varname):
    i = input(string[1:-1] + " ")
    symbols[varname] = "STRING:\"" + i + "\""

def parse(toks):
    i = 0
    while(i < len(toks)):
        if toks[i] == "ENDIF":
            pass
            i += 1
        elif toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
            if toks[i+1][0:6] == "STRING":
                doPRINT(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doPRINT(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                doPRINT(toks[i+1])
            elif toks[i+1][0:3] == "VAR":
                doPRINT(getVARIABLE(toks[i+1]))
            i += 2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i+2][0:6] == "STRING":
                doASSIGN(toks[i],toks[i+2])
            elif toks[i+2][0:3] == "NUM":
                doASSIGN(toks[i],toks[i+2])
            elif toks[i+2][0:4] == "EXPR":
                doASSIGN(toks[i],"NUM:"+str(evalExpression(toks[i+2][5:])))
            elif toks[i+2][0:3] == "VAR":
                doASSIGN(toks[i],getVARIABLE(toks[i+2]))
            i += 3
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
            getINPUT(toks[i+1][7:],toks[i+2][4:])
            i += 3
        elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM EQEQ NUM THEN" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:3] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NOTEQ NUM NUM THEN":
            if toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] == "NUM EQEQ NUM":
                if toks[i+1][4:] == toks[i+3][4:]:
                    pass
                else:
                    while True:
                        if toks[i+5] != "ENDIF":
                            toks.remove(toks[i+5])
                        else:
                            break
            elif toks[i+1] + " " + toks[i+2][0:3] + " " + toks[i+3][0:3] == "NOTEQ NUM NUM":
                if toks[i+2][4:] != toks[i+3][4:]:
                    pass
                else:
                    while True:
                        if toks[i+5] != "ENDIF":
                            toks.remove(toks[i+5])
                        else:
                            break
            i += 5
            
def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)

run()
