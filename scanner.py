import string

class Scanner:
    def __init__(self,text):
        self.key_words = ["if", "while", "do", "else"]
        self.operator  = ["{", "}", ";", "+", "-", "/", "*", ">", "<", "!"]
        self.digits = list(string.digits)
        self.letters = list(string.ascii_letters)
        self.withe_space = string.whitespace
        self.state = 0
        self.index = -1
        self.line = 1
        self.temp =""
        self.code = text

    def tokenizer(self):
        while True:
            match self.state:
                case 0:
                    self.index += 1
                    if self.index > len(self.code)-1:
                        break
                    ch = self.code[self.index]
                    if ch in self.withe_space:
                        if ch == "\n":
                            self.line += 1
                        self.state = 0
                    elif ch == "{":
                        print("( { , { )")
                        self.state = 0
                    elif ch == "(":
                        print("( (, ( )")
                        self.state = 0
                    elif ch == ")":
                        print("( ) , ) )")
                        self.state = 0
                    elif ch == "}":
                        print("( } , } )")
                        self.state = 0
                    elif ch == "+":
                        print("(op , +)")
                        self.state = 0
                    elif ch == "-":
                        print("(op , -)")
                        self.state = 0
                    elif ch == "/":
                        print("(op , /)")
                        self.state = 0
                    elif ch == "*":
                        print("(op , *)")
                        self.state = 0
                    elif ch == "<":
                        self.state = 1
                    elif ch == ">":
                        self.state = 1
                    elif ch == "=":
                        self.state = 4
                    elif ch == ";":
                        print("( ; , ;)")
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
                
                case 1:
                    prev = ch
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "=":
                        print(f"(op, {prev}=)")
                        self.state = 0
                        continue
                    print(f"(op, {prev})")
                    self.index -= 1
                    self.state = 0

                case 2:
                    prev = ch
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "=":
                        print(f"(op, {prev}=)")
                        self.state = 0
                        continue
                    print(f"(error, {prev} , line{self.line})")
                    self.index -= 1
                    self.state = 0

                case 3:
                    if self.index == len(self.code)-1:
                        break
                    self.index += 1
                    if self.code[self.index] in self.withe_space:
                        print(f"(error, $ , line{self.line})")
                        self.state = 0
                    else:
                        self.index -= 1
                        self.state = 9

                case 4:
                    prev = ch
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "=":
                        print("(op, ==)")
                        self.state = 0
                        continue
                    print("(assign_op , = )")
                    self.index -= 1
                    self.state = 0

                case 5:
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
                        print(f"(num , {num})")
                        num = ""
                        self.index -= 1
                        self.state = 0

                case 6:
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
                        print(f"(keyword , {self.temp})")
                        self.temp = ""
                        self.index -= 1
                        self.state = 0
                    else:
                        print(f"(id , {self.temp})")
                        self.temp = ""
                        self.index -= 1
                        self.state = 0

                case 7:
                    self.index += 1
                    ch = self.code[self.index]
                    if ch not in self.digits :
                        print(f"(error, {num} , line{self.line})")
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
                        print(f"(num , {num})")
                        num = ""
                        self.index -= 1
                        self.state = 0
                
                case 8:
                    self.index += 1
                    ch = self.code[self.index]
                    if ch == "+" or ch == "-":
                        num += ch
                        self.index += 1
                        ch = self.code[self.index]
                    elif ch not in self.digits :
                        print(f"(error, {num} , line{self.line})")
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
                    print(f"(num , {num})")
                    num = ""
                    self.state = 0
                    self.index -= 1

                case 9:
                    self.temp_error = ch
                    self.index += 1
                    if self.index > len(self.code)-1:
                        break
                    ch = self.code[self.index]
                    if ch in self.withe_space:
                        print(f"(error, {self.temp_error} , line{self.line})")
                        self.temp_error = ""
                        self.index -= 1
                        self.state = 0
                        continue
                    while ch not in self.digits  and ch not in self.letters and ch not in self.operator and ch not in self.withe_space:
                        self.temp_error += ch
                        self.index += 1
                        if self.index > len(self.code)-1:
                            print(f"(error, {self.temp_error} , line{self.line})")
                            break
                        ch = self.code[self.index]
                    print(f"(error, {self.temp_error} , line{self.line})")
                    self.temp_error = ""
                    self.index -= 1
                    self.state = 0

