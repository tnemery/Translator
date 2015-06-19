import lexer

gforthtoken = []
#newPT = []
sentence = []
operations = ['+','-','*','/','**','sin','cos','tan','<','<=','>','>=','=','<>']
dotOps = ['<','<=','>','>=','=','!=']
newPT = []
typeFlag = 0
count = 0
numInts = 0;
opSave = ''
realSet = 0
strSet = 0;


def breakToken(gforthtoken, newPT):
    #print "we go here? ",gforthtoken
    count = 0
    for i in gforthtoken:
        count += 1
        #print i
        if i == 'break' or len(gforthtoken) == count:
            #print newPT
            newPT = reversed(newPT)
            scopeLate(newPT)
            newPT = []
        else:
            newPT.append(i)
    pass

def Translate(parseToken):
    newCode = ""
    gforthtoken = checkScoping(parseToken)
    
    #print(gforthtoken)
    breakToken(gforthtoken, newPT)
    
    #printTrees(gforthtoken)
    #print gforthtoken
    
    
    sendGforth()
    pass

def scopeLate(newPT):
    typeFlag = 0
    count = 0
    numInts = 0;
    opSave = ''
    realSet = 0
    strSet = 0;
    for item in newPT:
        #print item
        if item[0][0] is not '(' and item[0][0] is not ')':
            #print item[0][1]
            if item[0][1] is 'NUMBER':
                typeFlag = 0
            if item[0][1] is 'REAL':
                realSet = 1
                typeFlag = 1
            if item[0][1] is 'STRING':
                typeFlag = 2
                sentence.append("s\" ")
            if typeFlag is 0:
                numInts += 1
                if item[0][0] is '^':
                    sentence.append("** ")
                    #newCode += ("** ")
                elif item[0][0] == '!=':
                    sentence.append("<> ")
                    #newCode += ("<> ")
                elif count is 1 and item[0][0] is '-':
                    sentence.append("negate ")
                    #newCode += "negate "
                elif item[0][0] == 'not':
                    sentence.append("invert ")
                    #newCode += "invert "
                elif item[0][0] == 'stdout':
                    sentence.append("type \n");
                else:
                    if realSet is 1 and operations.__contains__(item[0][0]) is True:
                        sentence.append("f"+item[0][0]+" ")
                        #newCode += ("f"+item[0][0]+" ")
                        numInts -= 1
                    elif realSet is 1 and operations.__contains__(item[0][0]) is False:
                        sentence.append(item[0][0]+" ")
                        #newCode += (item[0][0]+" ")
                        numInts -= 1
                    else:
                        sentence.append(item[0][0]+" ")
                        #newCode += (item[0][0]+" ")
                if realSet is 1 and operations.__contains__(item[0][0]) is False:
                    sentence.append("s>f ")
            elif typeFlag is 1:
                if count is 1 and item[0][0] is '-':
                    sentence.append("fnegate ")
                    #newCode += "fnegate "
                elif operations.__contains__(item[0][0]) is True:
                    sentence.append("f"+item[0][0]+" ")
                    #newCode += ("f"+item[0][0]+" ")
                    if dotOps.__contains__(item[0][0]) is True:
                        opSave = item[0][0]
                elif item[0][0] is '^':
                    sentence.append("f** ")
                    #newCode += ("f** ")
                elif item[0][0] == '!=':
                    sentence.append("f<> ")
                    #newCode += ("f<> ")
                elif item[0][0] is '%':
                    sentence.append("% ")
                    #newCode += "% "
                elif item[0][0] == 'stdout':
                    sentence.append("type \n");
                else:
                    sentence.append(item[0][0]+"e ")
                    #newCode += (item[0][0]+"e ")
                if numInts is not 0:
                    sentence.append("s>f fswap ")
                    numInts -= 1
            elif typeFlag is 2:
                if item[0][0] == '+':
                    sentence.append("s"+item[0][0]+" ")
                elif item[0][0] == 'stdout':
                    sentence.append("type \n");
                else:
                    sentence.append(item[0][0][1:]+" ")
                #newCode += (item[0][0][1:-1]+" ")
            count += 1
            pass
        pass
    newPT = []
    if typeFlag is 0 and realSet is not 1:
        sentence.append(". CR \n")
        #newCode += ". CR"
    elif realSet is 1:
        if dotOps.__contains__(opSave) is True:
            sentence.append(". CR \n")
            #newCode += ". CR"
        else:
            sentence.append("f. CR \n")
            #newCode += "f. CR"
    elif typeFlag is 2:
        sentence.append("CR \n")
        #newCode = ".\" "+newCode[:-2]+ "\" CR"    
    #print "check: ",sentence
    pass

def checkScoping(tokens):
    defs = []
    defining = 0
    curvar = ""
    typevar = 0
    assigning = 0
    charcheck = 0
    a = 1
    assignee = ""
    for i in tokens:
        if i[0][0] is not '(' and i[0][0] is not ')':
            if a is 0:
                if i[0][0] == 'let':
                    defining = 1
                    a = 1
                elif i[0][0] == ':=':
                    a = 1
                    defining = 1
                elif i[0][0] == 'while' or i[0][0] == 'if':
                    defs.append("break")
                defs.append(i)
            elif i[0][0] == 'let':
                defining = 1
            elif defining is 1:
                curvar = i[0][0]
                defining = 0
            elif i[0][0] == 'int':
                typevar = 0
            elif i[0][0] == 'real':
                typevar = 1
            elif i[0][0] == 'string':
                typevar = 2
            elif i[0][0] == 'bool':
                typevar = 3
            elif i[0][0] == ':=':
                assigning = 1
            elif assigning is 1 and i[0][0] == curvar:
                charcheck = 1
            elif assigning is 1 and charcheck is 1:
                assignee = i[0][0]
                assigning = 0
                charcheck = 0
                a = 0
            else:
                defs.append(i)
                a = 0
    if typevar is 1 or 3 or 4:
        sentence.append(assignee+" Constant "+curvar+" \n")
    else:
        sentence.append(assignee+" fconstant "+curvar+" \n")
    return defs
    pass


def sendGforth():
    gforthcode = ""
    #print "lllll: ",sentence
    for i in sentence:
        gforthcode += i
    print gforthcode
    #print code
    pass
