from collections import deque
from collections import OrderedDict
from pprint import pprint
import firstfollow
from firstfollow import production_list, nt_list as ntl, t_list as tl
nt_list, t_list=[], []

import string

class Scanner:
    def __init__(self,text):
        self.key_words = ["if", "while", "do", "else"]
        self.operator  = ["{", "}", ";", "+", "-", "/", "*", ">", "<", "!"]
        self.digits = list(string.digits)
        self.letters = list(string.ascii_letters)
        self.withe_space = list(string.whitespace)
        self.state = 0
        self.index = -1
        self.line = 1
        self.temp =""
        self.code = text
        self.tokens_list=[]
    def tokenizer(self):
        while True:
            if True:
                if self.state ==  0:
                    self.index += 1
                    if self.index > len(self.code)-1:
                        break
                    ch = self.code[self.index]
                    if ch in self.withe_space:
                        if ch == "\n":
                            self.line += 1
                        self.state = 0
                    elif ch == "{":
                        self.tokens_list.append("({,{)")
                        self.state = 0
                    elif ch == "(":
                        self.tokens_list.append("((,()")
                        self.state = 0
                    elif ch == ")":
                        self.tokens_list.append("(),))")
                        self.state = 0
                    elif ch == "}":
                        self.tokens_list.append("(},})")
                        self.state = 0
                    elif ch == "+":
                        self.tokens_list.append("(OP,+)")
                        self.state = 0
                    elif ch == "-":
                        self.tokens_list.append("(OP,-)")
                        self.state = 0
                    elif ch == "/":
                        self.tokens_list.append("(OP,/)")
                        self.state = 0
                    elif ch == "*":
                        self.tokens_list.append("(OP,*)")
                        self.state = 0
                    elif ch == "<":
                        self.state = 1
                    elif ch == ">":
                        self.state = 1
                    elif ch == "=":
                        self.state = 4
                    elif ch == ";":
                        self.tokens_list.append("(;,;)")
                        self.state = 0
                    elif ch == "!":
                        self.state = 2
                    elif ch == "$":
                        self.state = 3
                    elif ch in self.digits :
                        self.state = 5
                    elif ch in self.letters:
                        self.state = 6
                    else:
                        self.state = 9
                
                if self.state ==  1:
                    prev = ch
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "=":
                        self.tokens_list.append(f"(OP,{prev}=)")
                        self.state = 0
                        continue
                    if prev in ["<",">"]:
                        self.tokens_list.append(f"(R_OP,{prev})")
                        self.state = 0
                        self.index -= 1
                    else:
                        self.tokens_list.append(f"(OP,{prev})")
                        self.index -= 1
                        self.state = 0

                if self.state ==  2:
                    prev = ch
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "=":
                        self.tokens_list.append(f"(OP,{prev}=)")
                        self.state = 0
                        continue
                    if ch in ["<",">"]:
                        self.tokens_list.append(f"(R_OP,{prev}=)")
                        self.state = 0
                        continue
                    self.tokens_list.append(f"(ERROR,{prev},line{self.line})")
                    self.index -= 1
                    self.state = 0

                if self.state ==  3:
                    if self.index == len(self.code)-1:
                        break
                    self.index += 1
                    if self.code[self.index] in self.withe_space:
                        self.tokens_list.append(f"(ERROR,$,line{self.line})")
                        self.state = 0
                    else:
                        self.index -= 1
                        self.state = 9

                if self.state ==  4:
                    prev = ch
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "=":
                        self.tokens_list.append("(R_OP,==)")
                        self.state = 0
                        continue
                    self.tokens_list.append("(ASSIGN_OP,=)")
                    self.index -= 1
                    self.state = 0

                if self.state ==  5:
                    num = ch
                    self.index += 1
                    ch = self.code[self.index]
                    while ch in self.digits :
                        num += ch
                        self.index += 1
                        if self.index > len(self.code)-1:
                            break
                        ch = self.code[self.index]
                    if ch == ".":
                        self.state = 7
                        num += ch
                    elif ch == "E":
                        self.state = 8
                        num += ch
                    else:
                        if num[-1] in self.operator:
                            self.tokens_list.append(f"(ERROR,{num},line{self.line})")
                            self.state =0
                        self.tokens_list.append(f"(NUM,{num})")
                        num = ""
                        self.index -= 1
                        self.state = 0

                if self.state ==  6:
                    if not self.temp:
                        self.temp = ch
                    self.index += 1
                    ch = self.code[self.index]
                    while ch in self.digits  or ch in self.letters:
                        self.temp += ch
                        self.index += 1
                        if self.index > len(self.code)-1:
                            break
                        ch = self.code[self.index]
                    if self.temp in self.key_words:
                        self.tokens_list.append(f"(KEY,{self.temp})")
                        self.temp = ""
                        self.index -= 1
                        self.state = 0
                    else:
                        self.tokens_list.append(f"(ID,{self.temp})")
                        self.temp = ""
                        self.index -= 1
                        self.state = 0

                if self.state ==  7:
                    self.index += 1
                    ch = self.code[self.index]
                    if ch not in self.digits :
                        self.tokens_list.append(f"(ERROR,{num},line{self.line})")
                        num = ""
                        self.state = 0
                        self.index -= 1
                        continue
                    while ch in self.digits :
                        num += ch
                        self.index += 1
                        ch = self.code[self.index]
                    if ch == "E":
                        self.state = 8
                        num += ch
                    else:
                        if num[-1] in self.operator:
                            self.tokens_list.append(f"(ERROR,{num},line{self.line})")
                            self.state =0

                        self.tokens_list.append(f"(NUM,{num})")
                        num = ""
                        self.index -= 1
                        self.state = 0
                
                if self.state ==  8:
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "+" or ch == "-":
                        num += ch
                        self.index += 1
                        ch = self.code[self.index]
                    elif ch not in self.digits :
                        self.tokens_list.append(f"(ERROR,{num},line{self.line})")
                        num = ""
                        self.state = 0
                        self.index -= 1
                        continue
                    while ch in self.digits :
                        num += ch
                        self.index += 1
                        if self.index > len(self.code)-1:
                            break
                        ch = self.code[self.index]
                    if num[-1] in self.operator:
                            self.tokens_list.append(f"(ERROR,{num},line{self.line})")
                            self.state =0
                            self.index -= 1

                    else:
                        self.tokens_list.append(f"(NUM,{num})")
                        num = ""
                        self.state = 0
                        self.index -= 1

                if self.state ==  9:
                    self.temp_error = ch
                    self.index += 1
                    if self.index > len(self.code)-1:
                        break
                    ch = self.code[self.index]
                    if ch in self.withe_space:
                        self.tokens_list.append(f"(ERROR,{self.temp_error},line{self.line})")
                        self.temp_error = ""
                        self.index -= 1
                        self.state = 0
                        continue
                    while ch not in self.digits  and ch not in self.letters and ch not in self.operator and ch not in self.withe_space:
                        self.temp_error += ch
                        self.index += 1
                        if self.index > len(self.code)-1:
                            self.tokens_list.append(f"(ERROR,{self.temp_error},line{self.line})")
                            break
                        ch = self.code[self.index]
                    self.tokens_list.append(f"(ERROR,{self.temp_error},line{self.line})")
                    self.temp_error = ""
                    self.index -= 1
                    self.state = 0

        return self.tokens_list

def read_file():
    tokens_list = ""

    while True:
        i = input("")
        if i=="$":
            break
        tokens_list+=i+"\n"
    return tokens_list



class State:

    _id=0
    def __init__(self, closure):
        self.closure=closure
        self.no=State._id
        State._id+=1

class Item(str):
    def __new__(cls, item, lookahead=list()):
        self=str.__new__(cls, item)
        self.lookahead=lookahead
        return self

    def __str__(self):
        return super(Item, self).__str__()+", "+'|'.join(self.lookahead)
        

def closure(items):

    def exists(newitem, items):

        for i in items:
            if i==newitem and sorted(set(i.lookahead))==sorted(set(newitem.lookahead)):
                return True
        return False


    global production_list

    while True:
        flag=0
        for i in items: 
            
            if i.index('.')==len(i)-1: continue

            Y=i.split('->')[1].split('.')[1][0]

            if i.index('.')+1<len(i)-1:
                lastr=list(firstfollow.compute_first(i[i.index('.')+2])-set(chr(1013)))
                
            else:
                lastr=i.lookahead
            
            for prod in production_list:
                head, body=prod.split('->')
                
                if head!=Y: continue
                
                newitem=Item(Y+'->.'+body, lastr)

                if not exists(newitem, items):
                    items.append(newitem)
                    flag=1
        if flag==0: break

    return items

def goto(items, symbol):

    global production_list
    initial=[]

    for i in items:
        if i.index('.')==len(i)-1: continue

        head, body=i.split('->')
        seen, unseen=body.split('.')


        if unseen[0]==symbol and len(unseen) >= 1:
            initial.append(Item(head+'->'+seen+unseen[0]+'.'+unseen[1:], i.lookahead))

    return closure(initial)


def calc_states():

    def contains(states, t):

        for s in states:
            if len(s) != len(t): continue

            if sorted(s)==sorted(t):
                for i in range(len(s)):
                        if s[i].lookahead!=t[i].lookahead: break
                else: return True

        return False

    global production_list, nt_list, t_list

    head, body=production_list[0].split('->')


    states=[closure([Item(head+'->.'+body, ['$'])])]
    
    while True:
        flag=0
        for s in states:

            for e in nt_list+t_list:
                
                t=goto(s, e)
                if t == [] or contains(states, t): continue

                states.append(t)
                flag=1

        if not flag: break
    
    return states 


def make_table(states):

    global nt_list, t_list

    def getstateno(t):

        for s in states:
            if len(s.closure) != len(t): continue

            if sorted(s.closure)==sorted(t):
                for i in range(len(s.closure)):
                        if s.closure[i].lookahead!=t[i].lookahead: break
                else: return s.no

        return -1

    def getprodno(closure):

        closure=''.join(closure).replace('.', '')
        return production_list.index(closure)

    SLR_Table=OrderedDict()
    
    for i in range(len(states)):
        states[i]=State(states[i])

    for s in states:
        SLR_Table[s.no]=OrderedDict()

        for item in s.closure:
            head, body=item.split('->')
            if body=='.': 
                for term in item.lookahead: 
                    if term not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][term]={'r'+str(getprodno(item))}
                    else: SLR_Table[s.no][term] |= {'r'+str(getprodno(item))}
                continue

            nextsym=body.split('.')[1]
            if nextsym=='':
                if getprodno(item)==0:
                    SLR_Table[s.no]['$']='accept'
                else:
                    for term in item.lookahead: 
                        if term not in SLR_Table[s.no].keys():
                            SLR_Table[s.no][term]={'r'+str(getprodno(item))}
                        else: SLR_Table[s.no][term] |= {'r'+str(getprodno(item))}
                continue

            nextsym=nextsym[0]
            t=goto(s.closure, nextsym)
            if t != []: 
                if nextsym in t_list:
                    if nextsym not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][nextsym]={'s'+str(getstateno(t))}
                    else: SLR_Table[s.no][nextsym] |= {'s'+str(getstateno(t))}

                else: SLR_Table[s.no][nextsym] = str(getstateno(t))

    return SLR_Table

def augment_grammar():

    for i in range(ord('Z'), ord('A')-1, -1):
        if chr(i) not in nt_list:
            start_prod=production_list[0]
            production_list.insert(0, chr(i)+'->'+start_prod.split('->')[0]) 
            return

def read_file():
    tokens_list = ""

    while True:
        i = input("")
        if i=="$":
            tokens_list+=i
            break
        tokens_list+=i+""
    return tokens_list

def convert_data(input):
        temp = []
        for item in input:
            i = item.replace("(","").replace(")","").split(",")
            if i[0] in ["R_OP","OP","KEY","ASSIGN_OP"]:
                temp.append(str(i[1]))
            else:
                temp.append(str(i[0]).lower())
        # #print("data",temp)
        # temp.append("$")
        temp2=[]
        convertor = {"if":"i","id":"d","while":"w","do":"o","num":"n","==":"q","!=":"t","else":"e","<=":"y",">=":"p"}
        # print(temp)
        for i in temp:
            if i in convertor:
                temp2.append(convertor[i])
            else:
                temp2.append(i)
        
        return temp2

def main(tokens):

    global production_list, ntl, nt_list, tl, t_list    

    firstfollow.main()
    for nt in ntl:
        firstfollow.compute_first(nt)
        firstfollow.compute_follow(nt)
        print(nt)
        print("\tFirst:\t", firstfollow.get_first(nt))
        print("\tFollow:\t", firstfollow.get_follow(nt), "\n")  
    

    augment_grammar()
    nt_list=list(ntl.keys())
    t_list=list(tl.keys()) + ['$']

    print(nt_list)
    print(t_list)

    j=calc_states()

    ctr=0
    for s in j:
        print("Item{}:".format(ctr))
        for i in s:
            pass
            print("\t", i)
        ctr+=1

    table=make_table(j)
    print('_____________________________________________________________________')
    print("\n\tCLR(1) TABLE\n")
    sym_list = nt_list + t_list
    sr, rr=0, 0
    print('_____________________________________________________________________')
    print('\t|  ','\t|  '.join(sym_list),'\t\t|')
    print('_____________________________________________________________________')
    for i, j in table.items():
        print(i, "\t|  ", '\t|  '.join(list(j.get(sym,' ') if type(j.get(sym))in (str , None) else next(iter(j.get(sym,' ')))  for sym in sym_list)),'\t\t|')
        s, r=0, 0

        for p in j.values():
            if p!='accept' and len(p)>1:
                p=list(p)
                if('r' in p[0]): r+=1
                else: s+=1
                if('r' in p[1]): r+=1
                else: s+=1      
        if r>0 and s>0: sr+=1
        elif r>0: rr+=1
    print('_____________________________________________________________________')
    print("\n", sr, "s/r conflicts |", rr, "r/r conflicts")
    print('_____________________________________________________________________')
    # print("Enter the string to be parsed")
    Input= tokens
    try:
        stack=['0']
        a=list(table.items())
        print("productions\t:",production_list)
        print('stack',"\t \t\t \t",'Input')
        print(*stack,"\t \t\t \t",*Input,sep="")
        while(len(Input)!=0):
            b=list(a[int(stack[-1])][1][Input[0]])
            if(b[0][0]=="s" ):
                s=Input[0]+b[0][1:]
                stack.append(Input[0])
                stack.append(b[0][1:])
                Input=Input[1:]
                print(*stack,"\t \t\t \t",*Input,sep="")
            elif(b[0][0]=="r" ):
                s=int(b[0][1:])
                print(len(production_list),s)
                l=len(production_list[s])-3
                print(l)
                prod=production_list[s]
                l*=2
                l=len(stack)-l
                stack=stack[:l]
                s=a[int(stack[-1])][1][prod[0]]
                print(s,b)
                stack+=list(prod[0])
                stack.append(s)
                print(*stack,"\t \t\t \t",*Input,sep="")
            elif(b[0][0]=="a"):
                print("successful")
                break
    except:
        print('ERROR')
    return 

if __name__=="__main__":
    raw_data =read_file()
    # print(raw_data.replace("\n",""))
    sc = Scanner(raw_data)
    tokens = sc.tokenizer()
    print("".join(convert_data(tokens)))
    # main("".join(convert_data(tokens)))
    main("idqdd=d+n;wdo{id>nd=n;e{d=n;}d=d-n;$")
    




