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
class T_If:
    def __init__(self, value):
        self.value = value
class T_LeftBrace:
    def __init__(self, value):
        self.value = value
class T_RightBrace:
    def __init__(self, value):
        self.value = value
class T_Define:
    def __init__(self, value):
        self.value = value
class T_Else:
    def __init__(self, value):
        self.value = value
class T_Comma:
    def __init__(self, value):
        self.value = value
class T_Return:
    def __init__(self, value):
        self.value = value
class T_Plus:
    def __init__(self, value):
        self.value = value
class T_Minus:
    def __init__(self, value):
        self.value = value
class T_Star:
    def __init__(self, value):
        self.value = value
class T_Slash:
    def __init__(self, value):
        self.value = value
class T_For:
    def __init__(self, value):
        self.value = value
class T_DoubleEquals:
    def __init__(self, value):
        self.value = value
class T_Less:
    def __init__(self, value):
        self.value = value
class T_Greater:
    def __init__(self, value):
        self.value = value
class T_LessEquals:
    def __init__(self, value):
        self.value = value
class T_GreaterEquals:
    def __init__(self, value):
        self.value = value
class T_While:
    def __init__(self, value):
        self.value = value
class T_Break:
    def __init__(self, value):
        self.value = value
class T_Continue:
    def __init__(self, value):
        self.value = value
class T_PlusEquals:
    def __init__(self, value):
        self.value = value
class T_MinusEquals:
    def __init__(self, value):
        self.value = value
class T_StarEquals:
    def __init__(self, value):
        self.value = value
class T_SlashEquals:
    def __init__(self, value):
        self.value = value
class T_DoublePlus:
    def __init__(self, value):
        self.value = value
class T_DoubleMinus:
    def __init__(self, value):
        self.value = value

class Tokeniser:
    def __init__(self):
        self.contents = ""
        self.currentToken = ""
        self.tokens = []
        self.index = 0

    def getType(self, value):
        if len(value) == 0:
            return None
        elif value[0] == "'":
            return T_String
        elif value == "END":
            return T_End
        elif value == "(":
            return T_LeftParen
        elif value == ")":
            return T_RightParen
        elif value == "=":
            return T_SingleEquals
        elif value == "if":
            return T_If
        elif value == "{":
            return T_LeftBrace
        elif value == "}":
            return T_RightBrace
        elif value == "define":
            return T_Define
        elif value == "else":
            return T_Else
        elif value == ",":
            return T_Comma
        elif value == "return":   # if value is return, return t_return
            return T_Return
        elif value == "+":
            return T_Plus
        elif value == "-":
            return T_Minus
        elif value == "*":
            return T_Star
        elif value == "/":
            return T_Slash
        elif value == "for":
            return T_For
        elif value == "==":
            return T_DoubleEquals
        elif value == "<":
            return T_Less
        elif value == ">":
            return T_Greater
        elif value == "<=":
            return T_LessEquals
        elif value == ">=":
            return T_GreaterEquals
        elif value == "while":
            return T_While
        elif value == "break":
            return T_Break
        elif value == "continue":
            return T_Continue
        elif value == "+=":
            return T_PlusEquals
        elif value == "-=":
            return T_MinusEquals
        elif value == "*=":
            return T_StarEquals
        elif value == "/=":
            return T_SlashEquals
        elif value == "++":
            return T_DoublePlus
        elif value == "--":
            return T_DoubleMinus
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
        t_type = self.getType(self.currentToken)
        if t_type != None:
            self.tokens.append(self.createToken(t_type, self.currentToken))

    def appendTokens(self, extra):
        self.appendCurrentToken()
        self.tokens.append(self.createToken(self.getType(extra), extra))
        self.currentToken = ""

    def isCurrentToken(self, check):
        char = self.contents[self.index]

        if not char == check[0]:
            return False
        
        next = check[1:]
        for index in range(len(next)):
            amount = index + 1

            if not self.peek(amount) == next[index]:
                return False
        
        return True

    def tokenise(self, content):
        self.contents = content
        inComment = False
        inMLComment = False
        inString = False
        escaping = False
        garbageEscapingTimes = 0
        parenLayer = 0
        braceLayer = 0
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
                elif self.peek() == "=":
                    self.appendTokens("/=")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens("/")
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
            elif garbageEscapingTimes > 0:
                garbageEscapingTimes -= 1
                continue
            elif (char == "'" or char == '"') and not inString:
                self.currentToken = "'"
                inString = True
                stringChars = char
            elif char == stringChars and inString:
                inString = False
            elif char == "(" and not inString:
                self.appendTokens("(")
                parenLayer += 1
            elif char == ")" and not inString:
                self.appendTokens(")")
                parenLayer -= 1
                if parenLayer < 0:
                    print("No '(' to close")
                    exit(1)
            elif char == "=" and not inString:
                if self.peek() == "=":
                    self.appendTokens("==")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens("=")
            elif self.isCurrentToken("if") and not inString:
                self.appendTokens("if")
                garbageEscapingTimes += len("if") - 1
            
            elif char == "{" and not inString:
                self.appendTokens("{")
                braceLayer += 1
            elif char == "}" and not inString:
                self.appendTokens("}")
                braceLayer -= 1
                if braceLayer < 0:
                    print("No '{' to close")
                    exit(1)
            elif char == "," and not inString:
                self.appendTokens(",")
            elif self.isCurrentToken("define") and not inString:
                self.appendTokens("define")
                garbageEscapingTimes += len("define") - 1
            elif self.isCurrentToken("else") and not inString:
                self.appendTokens("else")
                garbageEscapingTimes += len("else") - 1
            elif self.isCurrentToken("return") and not inString:
                self.appendTokens("return")
                garbageEscapingTimes += len("return") - 1
            elif char == "+" and not inString:
                if self.peek() == "=":
                    self.appendTokens("+=")
                    garbageEscapingTimes += 1
                elif self.peek() == "+":
                    self.appendTokens("++")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens("+")
            elif char == "-" and not inString:
                if self.peek() == "=":
                    self.appendTokens("-=")
                    garbageEscapingTimes += 1
                elif self.peek() == "-":
                    self.appendTokens("--")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens("-")
            elif char == "*" and not inString:
                if self.peek() == "=":
                    self.appendTokens("*=")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens("*")
            elif self.isCurrentToken("for") and not inString:
                self.appendTokens("for")
                garbageEscapingTimes += len("for") - 1
            elif char == "<" and not inString:
                if self.peek() == "=":
                    self.appendTokens("<=")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens("<")
            elif char == ">" and not inString:
                if self.peek() == "=":
                    self.appendTokens(">=")
                    garbageEscapingTimes += 1
                else:
                    self.appendTokens(">")
            elif self.isCurrentToken("while") and not inString:
                self.appendTokens("while")
                garbageEscapingTimes += len("while") - 1
            elif self.isCurrentToken("break") and not inString:
                self.appendTokens("break")
                garbageEscapingTimes += len("break") - 1
            elif self.isCurrentToken("continue") and not inString:
                self.appendTokens("continue")
                garbageEscapingTimes += len("continue") - 1
            else:
                self.currentToken += char
        
        if self.currentToken != "":
            self.tokens.append(self.currentToken)
        
        self.tokens.append(T_End("END"))

        if inString:
            print("Unterminated string")
            exit(1)
        
        if parenLayer > 0:
            print("Missing ')'")
            exit(1)
        
        if braceLayer > 0:
            print("Missing '}'")
            exit(1)
        
        return self.tokens