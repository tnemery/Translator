import fileinput
import translator

# note fix binop protest2.in

#   Python Lexer
#   Written by: Thomas Emery
#   CS 480
#   Oregon State University
#
#
#   Description: Work in progress to tokenize a language
#                tokenizes and parses tokens to IBTL

def checknum(myS):
    try:
        float(myS)
        return True
    except ValueError:
        return False

def reservedWords():
    myHash['+'] = 'PLUS'
    myHash['-'] = 'MINUS'
    myHash['/'] = 'DIVIDE'
    myHash['*'] = 'MULT'
    myHash['^'] = 'POWER'
    myHash['%'] = 'REMAINDER'
    myHash['('] = 'LPAREN'
    myHash[')'] = 'RPAREN'
    myHash['='] = 'EQUIV'
    myHash['<'] = 'LT'
    myHash['>'] = 'GT'
    myHash[':='] = 'ASSIGN'
    myHash['>='] = 'GTE'
    myHash['<='] = 'LTE'
    myHash['!='] = 'NOTEQUAL'
    myHash['!'] = 'NOT'
    myHash['true'] = 'TRUE'
    myHash['false'] = 'FALSE'
    myHash['not'] = 'NOT'
    myHash['and'] = 'AND'
    myHash['or'] = 'OR'
    myHash['mod'] = 'MOD'
    myHash['sin'] = 'SIN'
    myHash['cos'] = 'COS'
    myHash['tan'] = 'TAN'
    myHash['if'] = 'IF'
    myHash['while'] = 'WHILE'
    myHash['do'] = 'DO'
    myHash['for'] = 'FOR'
    myHash['then'] = 'THEN'
    myHash['else'] = 'ELSE'
    myHash['let'] = 'LET'
    myHash['stdout'] = 'STDOUT'
    myHash['bool'] = 'BOOL'
    myHash['int'] = 'INT'
    myHash['float'] = 'FLOAT'
    myHash['real'] = 'REAL'
    myHash['string'] = 'STRING'
    
    pass


def tokenizer(tag):
    check = myHash.has_key(tag)
    if(check is True):
        Tokens.append([tag,myHash.get(tag)])
        return 1
    else:
        return 0
    pass

def specialtoken(tag2):
    myHash[tag2] = 'ID'
    Tokens.append([tag2,myHash.get(tag2)])
    pass

def errorOut(invalidTok):
    print invalidTok," on line ",lineNum," is invalid"
    pass
def SyntaxError():
    print "invalid syntax: "
    return "die";
    pass



def scanner(myFile):
    curLine = 1
    count = 1
    stLet = 0
    stNum = 0
    stSym = 0
    word = ''
    idNum = 0
    # num flags
    nDec = 0 #first period for floats
    nEsc = 0 #e for scientific
    nEDec = 0 #period seen after an e
    nNeg  = 0 # for a negative seen immediate after e
    #end num flags
    sString = 0 #string flag
    sSecond = 0 # theres another symbol!
    EOF = 0
    #print "scanning"
    #print "entire file ",myFile
    for ch in myFile:
        
        if count >= len(myFile):
            peek = myFile[count-1]
            EOF = 1
            lineNum + 1
        else:
            peek = myFile[count]
        curLook = ch
        #print curLook == '\n'
        #print curLook
        if stLet is 0 and stNum is 0 and stSym is 0:
            retVal = checknum(curLook)
            if retVal is True:
                stNum = 1
                #print "setting nums"
            else:
                retVal = SymLookup.__contains__(curLook)
                #print retVal
                if retVal is True:
                    stSym = 1
                    #print "setting syms"
                else:
                    if curLook == '\n' or curLook is ' ' or curLook is '\t':
                        pass #print "whitespace"
                    else:
                        stLet = 1
                        #print "setting lets"
        if stLet is 1:
            if word is '_' and (curLook is ' ' or curLook is '\t' or curLook == '\n'):
                errorOut(word)
                pass
            word += curLook
            retVal = checknum(peek)
            if retVal is True:
                pass
            if peek is ' ' or peek is '\t' or peek == '\n' or EOF is 1:
                if EOF is 1:
                    lineNum + 1
                check = tokenizer(word)
                if check is 0:
                    specialtoken(word)
                stLet = 0
                word = ''
            if SymLookup.__contains__(peek) is True:
                if peek is '_': #underscore allowed in id
                    pass
                else:
                    check = tokenizer(word)
                    if check is 0:
                        specialtoken(word)
                    stLet = 0
                    word = ''
        if stNum is 1:
            word += curLook
            #print "im in number printing peek ",peek
            if peek is '.':
                if nDec is 0:
                    nDec = 1
                else:
                    if nEsc is 1 and nEDec is 0:
                        nEDec = 1
                    else:
                        Tokens.append([word,'REAL'])
                        word = ''
                        nDec = 0
                        nEDec = 0
                        nEsc = 0
                        nNeg = 0
                        stNum = 0
            elif peek is 'e' or peek is 'E':
                if nEsc is 0:
                    nEsc = 1
                else:
                    Tokens.append([word,'REAL'])
                    word = ''
                    nEsc = 0
                    nNeg = 0
                    nDec = 0
                    nEDec = 0
                    stNum = 0
            if ch is 'e' or ch is 'E' and peek is '-':
                nNeg = 1
            elif myHash.__contains__(peek) is True:
                if nDec > 0 or nEsc >0:
                    Tokens.append([word,'REAL'])
                else:
                    Tokens.append([word,'NUMBER'])
                word = ''
                nEsc = 0
                nNeg = 0
                nDec = 0
                nEDec = 0
                stNum = 0
            if peek is ' ' or peek is '\t' or peek == '\n' or EOF is 1:
                #print "quick check"
                if EOF is 1:
                    lineNum + 1
                if nDec > 0 or nEsc >0:
                    Tokens.append([word,'REAL'])
                else:
                    Tokens.append([word,'NUMBER'])
                word = ''
                nEsc = 0
                nNeg = 0
                nDec = 0
                nEDec = 0
                stNum = 0
            if peek.isalpha() is True and nEsc is not 1:
                if nDec > 0 or nEsc >0:
                    Tokens.append([word,'REAL'])
                else:
                    Tokens.append([word,'NUMBER'])
                word = ''
                nEsc = 0
                nNeg = 0
                nDec = 0
                nEDec = 0
                stNum = 0
        if stSym is 1:
            word += ch
            if ch is '[' or ch is ']':
                errorOut(ch)
                pass
            if ch == '_':
                stSym = 0
                stLet = 1
            if ch == '\"':
                #print "begin a string"
                if sString is 0:
                    sString = 1
                elif sString is 1:
                    sString = 0
                    Tokens.append([word,'STRING'])
                    stSym = 0
                pass
            elif ch is '>' or ch is '<' or ch is '!' or ch is ':' and sString is 0:
                if peek is '=':
                    sSecond = 1
                    pass #valid
            if sSecond is 1:
                sSecond = 0
            elif sString is not 1 and sSecond is not 1:
                tokenizer(word)
                word = ''
                stSym = 0
        count = count+1
    #print Tokens
            
    

#possible start tokens are Lparen,id,stdout,if,while,for,let,binop,unop,strings
def parser():
    tree = []
    SFlag = 0
    stopParser = ""
    parens = 0
    depth = 0
    bincnt = 0
    binExp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    binTemp = 0
    unExp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    uncnt = 0
    unTemp = 0
    ifCount = 0
    ifTemp = 0
    ifExpr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    letFromIf = 0
    i = 0
    #print Tokens.__len__()," ",Tokens[0]
    for tok in Tokens:
        #print "cur token: ",tok," cur flag: ",SFlag," cur ifTemp: ",ifTemp
        if tok[1] is 'RPAREN':
            depth -= 1
        if SFlag is 0:
            if tok[1] is 'LPAREN':
                parens += 1
                SFlag = 1;
                #depth += 1
                pass
            elif tok[1] is 'STRING' or tok[1] is 'NUMBER' or tok[1] is 'REAL': #consants and numbers/floats
                SFlag = 2
                #depth += 1
                pass
            elif tok[1] is 'ID':
                SFlag = 2
                #depth += 1
                pass
            else:
                #print "invalid Start ",tok
                stopParser = SyntaxError()
                pass
            tree += [tok,depth]
        elif SFlag is 1:  #started with a LParen
            if tok[1] is 'RPAREN':
                parens -= 1
                #depth -= 1
                if parens > 0:
                    SFlag = 1
                else:
                    SFlag = 0
            elif binops.__contains__(tok[0]) is True:
                if bincnt is not 0:
                    binExp[bincnt] = binTemp
                    binTemp = 0
                    pass
                bincnt += 1
                SFlag = 13
            elif unops.__contains__(tok[0]) is True:
                if uncnt is not 0:
                    unExp[uncnt] = unTemp
                    unTemp = 0
                    pass
                uncnt += 1
                SFlag = 14
            elif tok[1] is 'LPAREN':
                parens += 1
                #depth += 1
                SFlag = 1
            elif tok[1] is 'ASSIGN':
                #depth += 1
                SFlag = 3
            elif tok[1] is 'IF':
                if ifCount is not 0:
                    ifExpr[ifCount] = ifTemp
                    ifTemp = 0
                    pass
                ifCount += 1
                SFlag = 11
                pass
            elif tok[1] is 'WHILE':
                SFlag = 1
                pass
            elif tok[1] is 'LET':
                SFlag = 4
                pass
            elif tok[1] is 'STDOUT':
                SFlag = 2
                pass
            elif tok[1] is 'STRING' or tok[1] is 'NUMBER' or tok[1] is 'REAL': #consants and numbers/floats
                SFlag = 2
                #depth += 1
                pass
            elif tok[1] is 'ID':
                SFlag = 2
                #depth += 1
                pass
            tree += [tok,depth]
            pass
        elif SFlag is 2:  #started with a consant or id
            if tok[1] is 'LPAREN':
                parens += 1
                SFlag = 1;
                #depth += 1
                pass
            #elif binops.__contains__(tok[0]) is True or unops.__contains__(tok[0]):
                #SFlag = 2
            elif tok[1] is 'STRING' or tok[1] is 'NUMBER' or tok[1] is 'REAL': #consants and numbers/floats
                SFlag = 1
                #depth += 1
                pass
            elif tok[1] is 'ID':
                SFlag = 2
                #depth += 1
                pass
            elif tok[1] is 'RPAREN':
                parens -= 1
                SFlag = 1
                pass
            else:
                stopParser = SyntaxError()
                pass
            tree += [tok,depth]
            pass
        elif SFlag is 3: #in an assign statment
            if tok[1] is 'ID':
                SFlag = 10
                pass
            else:
                stopParser = SyntaxError(tok)
            tree += [tok,depth]
            pass
        elif SFlag is 4:    #let staments
            if tok[1] is 'LPAREN':
                SFlag = 5
                parens += 1
                #depth += 1
                pass
            else:
                stopParser = SyntaxError()
                pass
            tree += [tok,depth]
            pass
        elif SFlag is 5:
            if tok[1] is 'LPAREN':
                SFlag = 6
                parens += 1
                #depth += 1
                pass
            elif tok[1] is 'ID':
                SFlag = 7
                pass
            else:
                SyntaxError()
                pass
            tree += [tok, depth]
        elif SFlag is 6:
            if tok[1] is 'ID':
                SFlag = 7
                pass
            else:
                stopParser = SyntaxError()
                pass
            tree += [tok, depth]
        elif SFlag is 7:
            if types.__contains__(tok[0]) is True:
                SFlag = 8
                pass
            else:
                stopParser = SyntaxError()
                pass
            tree += [tok, depth]
        elif SFlag is 8:
            if tok[1] is 'RPAREN':
                SFlag = 9
                parens -= 1
                if letFromIf is 1:
                    SFlag = 11
                #depth -= 1
                pass
            else:
                SyntaxError(tok)
                pass
            tree += [tok, depth]
        elif SFlag is 9:
            if tok[1] is 'LPAREN':
                SFlag = 6
                parens += 1
                #depth += 1
                pass
            elif tok[1] is 'RPAREN':
                SFlag = 1
                parens -= 1
                #depth -= 1
            else:
                stopParser = SyntaxError()
                pass
            tree += [tok, depth]
        elif SFlag is 10:  #started with a consant or id
            if tok[1] is 'LPAREN':
                parens += 1
                SFlag = 1;
                #depth += 1
                pass
            elif tok[1] is 'STRING' or tok[1] is 'NUMBER' or tok[1] is 'REAL': #consants and numbers/floats
                SFlag = 12
                #depth += 1
                pass
            elif tok[1] is 'ID':
                SFlag = 2
                #depth += 1
                pass
            else:
                stopParser = SyntaxError()
                pass
            if ifCount is not 0:
                SFlag = 11
            tree += [tok, depth]
        elif SFlag is 11:
            if tok[1] is 'LPAREN' and ifTemp <= 3:
                SFlag = 1
                parens += 1
                ifTemp += 1
                pass
            elif tok[1] is 'ID' and ifTemp <= 3:
                SFlag = 11
                ifTemp += 1
                pass
            elif tok[1] is 'NUMBER'  or tok[1] is 'REAL' and ifTemp <= 3:
                SFlag = 11
                ifTemp += 1
                pass
            elif tok[1] is 'STRING' and ifTemp <= 3:
                SFlag = 11
                ifTemp += 1
                pass
            elif binops.__contains__(tok[0]) is True and parseToken[i-1][0][1] is 'LPAREN':
                SFlag = 13
                if bincnt < 0:
                    bincnt = 0
                if bincnt is not 0:
                    SFlag = 13
                    binExp[bincnt] = binTemp
                    binTemp = 0
                bincnt += 1
            elif unops.__contains__(tok[0]) is True and parseToken[i-1][0][1] is 'LPAREN':
                SFlag = 14
                if uncnt < 0:
                    uncnt = 0
                if uncnt is not 0:
                    SFlag = 14
                    unExp[uncnt] = unTemp
                    unTemp = 0
                uncnt += 1
            elif tok[1] is 'RPAREN' and (ifTemp is 2 or ifTemp is 3):
                ifCount -= 1
                parens -= 1
                if ifCount is not 0:
                    ifTemp = ifExpr[ifCount]
                    SFlag = 11
                else:
                    SFlag = 1
                    ifTemp = 0
            else:
                stopParser = SyntaxError()
            tree += [tok,depth]
        elif SFlag is 12:
            if tok[1] is 'RPAREN':
                SFlag = 1
                parens -= 1
                #depth -= 1
            else:
                stopParser = SyntaxError()
                pass
            tree += [tok, depth]
        elif SFlag is 13:
            if tok[1] is 'LPAREN':
                parens += 1
                SFlag = 11
                binTemp += 1
                pass
            elif tok[1] is 'STRING':
                SFlag = 13
                binTemp += 1
            elif tok[1] == 'NUMBER' or tok[1] is 'REAL':
                SFlag = 13
                binTemp += 1
            elif tok[1] is 'ID':
                SFlag = 13
                binTemp += 1
            elif tok[1] is 'RPAREN' and binTemp is 2:
                SFlag = 1
                parens -= 1
                bincnt -= 1
                if bincnt < 0:
                    bincnt = 0
                if bincnt is not 0:
                    SFlag = 13
                    binTemp = binExp[bincnt]
                elif ifCount is not 0:
                    SFlag = 11
                    binTemp = 0
                else:
                    binTemp = 0
            else:
                if parseToken[i-2][0][0] is '-' and tok[1] is 'RPAREN':
                    binTemp = 0
                    bincnt -= 1
                    parens -= 1
                    if uncnt is not 0:
                        SFlag = 14
                        unTemp = unExp[uncnt]
                    else:
                        unTemp = 0
                        SFlag = 0
                else:
                    stopParser = SyntaxError()
            tree += [tok,depth]
        elif SFlag is 14:
            if tok[1] is 'LPAREN':
                parens += 1
                SFlag = 0
                pass
            elif tok[1] is 'STRING' or tok[1] is 'NUMBER' or tok[1] is 'REAL' or tok[1] is 'ID':
                SFlag = 14
            elif tok[1] is 'RPAREN' and unTemp is 1:
                SFlag = 1
                uncnt -= 1
                parens -= 1
                if uncnt is not 0:
                    SFlag = 14
                    unTemp = unExp[uncnt]
                else:
                    unTemp = 0
            else:
                stopParser = SyntaxError()
            tree += [tok,depth]
            unTemp += 1
        if stopParser is "die":
            break;
        parseToken.append(tree)
        if tok[1] is 'LPAREN':
            depth += 1
        tree = []
        i += 1
    if parens is not 0:
        print "parens: ",parens
        SyntaxError()
    pass

    
    
def printTrees():
    #print "parsetoken ",parseToken 
    for item in parseToken:
        curTabs = ''
        tabs = item[1]
        count = 0
        while count < tabs:
            curTabs += '\t'
            count += 1
            pass
        print curTabs,item[0][0]
    #print Tokens
    pass


def main():
    entireFile = ""
    for line in fileinput.input():
        entireFile += line
    reservedWords()
    scanner(entireFile)
    parser()
    #translator.printTrees(parseToken)
    translator.Translate(parseToken)
    #printTrees()
    pass


entireFile = ""
peek = ''
lookat = ''
myHash = {}
Tokens = []
parseToken = [] #to create trees later
assignTable = [] #give id's there type for lookup
SymLookup = ['-','+','/','*','.','%','<','>','#','$','!','.','/','\\',':',';','\"','=','\'','(',')',']','[','_']
binops = ['-','+','*','/','%','^','=','>',">=",'<',"<=","!=","or","and"]
unops = ["-","not","sin","cos","tan"]
types = ["bool","int","real","string"]
lineNum = 1
if __name__ == '__main__':
    main()
