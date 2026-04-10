class T_Ident:
    def __init__(self, value):
        self.value = value
class T_String:
    def __init__(self, value):
        self.value = value[1:]
class T_Number:
    def __init__(self, value):
        self.value = float(value)
        if self.value == int(value):
            self.value = int(value)
class T_Boolean:
    def __init__(self, value):
        self.value = value
class T_LeftParen:
    def __init__(self, value):
        self.value = value
class T_RightParen:
    def __init__(self, value):
        self.value = value
class T_End:
    def __init__(self, value):
        self.value = value
class T_SingleEquals:
    def __init__(self, value):
        self.value = value

class Tokeniser:
    def __init__(self):
        self.contents = ""
        self.currentToken = ""
        self.tokens = []
        self.index = 0

    def getType(self, value):
        if value[0] == "'":
            return T_String
        elif value == "true" or value == "false":
            return T_Boolean
        elif value == "END":
            return T_End
        elif value == "(":
            return T_LeftParen
        elif value == ")":
            return T_RightParen
        elif value == "=":
            return T_SingleEquals
        else:
            try:
                x = int(value)
                return T_Number
            except:
                return T_Ident

    def createToken(self, t_type, value):
        return t_type(value)

    def peek(self, amount = 1):
        if self.index + amount < len(self.contents):
            return self.contents[self.index + amount]
        else:
            return ""
    
    def appendCurrentToken(self):
        self.tokens.append(self.createToken(self.getType(self.currentToken), self.currentToken))

    def appendTokens(self, extra):
        self.appendCurrentToken()
        self.tokens.append(self.createToken(self.getType(extra), extra))
        self.currentToken = ""

    def tokenise(self, content):
        self.contents = content
        inComment = False
        inMLComment = False
        inString = False
        escaping = False
        stringChars = ""
        
        for index in range(len(content)):
            self.index = index
            char = content[index]

            if char == "\n":
                inComment = False
                if self.currentToken != "":
                    self.appendCurrentToken()
                    self.currentToken = ""
                continue
            elif char == " " and not inString:
                continue
            elif char == "/" and not inComment and not inMLComment and not inString and not self.peek() == "*":
                if self.peek() == "/":
                    inComment = True
                    continue
            elif char == "/" and not inComment and not inMLComment and not inString:
                if self.peek() == "*":
                    inMLComment = True
                    continue
            elif char == "*" and not inComment and inMLComment and not inString and not self.peek(-1) == "/":
                if self.peek() == "/":
                    inMLComment = False
                    continue
            elif inComment or inMLComment:
                continue
            elif char == "\\" and inString:
                escaping = True
                continue
            elif escaping and inString:
                escaping = False
                self.currentToken += char
                continue
            elif (char == "'" or char == '"') and not inString:
                self.currentToken = "'"
                inString = True
                stringChars = char
            elif char == stringChars and inString:
                inString = False
            elif char == "(":
                self.appendTokens("(")
            elif char == ")":
                self.appendTokens(")")
            elif char == "=":
                self.appendTokens("=")
            else:
                self.currentToken += char
        
        if self.currentToken != "":
            self.tokens.append(self.currentToken)
        
        self.tokens.append(T_End("END"))
        
        return self.tokens