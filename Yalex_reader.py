from Regex import Regex
from NFA_ import *

class YAlexTokenizer:
    def __init__(self, path_to_file:str) -> None:
        self.path = path_to_file
        self.var_prefixes = ['let', 'var', 'const','global', 'static']
        self.var_def_rules = ['delim', 'ws', 'letter', 'digit', 'digits', 'id', 'number', 'str']
        self.lines = self.returnLines()
        self.delim_val = ''
        self.digit_val = ''
        self.letter_val = ''
        self.tokens = []
        
    def returnLines(self) -> list:
        lines = []
        with open(self.path, "r") as file:
            for line in file:
                line = str(line.rstrip('\r\n'))
                lines.append(line)
        return lines

    def get_non_empty_lines(self) -> list:
        lines = self.lines
        new_lines = []
        for line in lines:
            line.split(' ')
            if line != '':
                new_lines.append(line)
        return new_lines
                            
    def get_tokens(self):
        lines = self.get_non_empty_lines()
        for line in lines:
            line = line.split(' ')
            if line[0] in self.var_prefixes:
                self.check_grammar_vars(line)
                self.default_rules(line)
                
    def default_rules(self, lista) -> None:
        if lista[1] == 'delim':
            self.tokens.append(self.handle_delim(lista))
        elif lista[1] == 'ws':
            self.tokens.append(self.handle_ws(lista))
        elif lista[1] == 'letter':
            self.tokens.append(self.handle_letter(lista))
        elif lista[1] == 'digit':
            self.tokens.append(self.handle_digit(lista))
        elif lista[1] == 'digits':
            self.tokens.append(self.handle_digits(lista))
        elif lista[1] == 'id':
            self.tokens.append(self.handle_id(lista))
        elif lista[1] == 'number':
            self.tokens.append(f'{self.handle_number(lista)}')
        elif lista[1] == 'str':
            self.tokens.append(f'{self.handle_string(lista)}')
        
    def check_grammar_vars(self, line):
        
        if line[0] not in self.var_prefixes:
            raise Exception(f'Syntax Error: variable declaration is incorrect.\nSee element: {line}')
        elif line[1] not in self.var_def_rules:
            raise Exception('Syntax Error: variable declaration is incorrect: ',line[1], 'is not a valid rule.')
        elif line[2] != '=':
            raise Exception('Syntax Error: variable declaration is incorrect: ',line[2], 'not valid.')
    
    def handle_delim(self, line):
        new_token = line[-1].replace('[', '').replace(']','').replace("'",'').replace('"','').replace('\\','')
        new_token =  "$".join(new_token) + "$"
        new_token = new_token[:-1]
        self.delim_val = new_token
        return new_token
    
    def handle_ws(self, line):
        handle = line[-1].replace('[', '').replace(']','').replace("'",'').replace('"','')
        for item in self.var_def_rules:
            if item in handle:
                rule = item
                if rule == 'delim':
                    self.tokens.append(f'{self.delim_val}|{self.delim_val}')
                elif rule == 'ws':
                    raise Exception('Syntax Error: variable declaration is incorrect: ',item, 'is not a valid rule.')
                elif rule == 'digit':
                    self.tokens.append()
                elif rule == 'digits':
                    self.tokens.append(f'{self.handle_digits(line)}|{self.handle_digits(line)}')
                elif rule == 'id':
                    self.tokens.append(f'{self.handle_id(line)}|{self.handle_id(line)}')
                elif rule == 'number':
                    self.tokens.append(f'{self.handle_number(line)}|{self.handle_number(line)}')  
            
    def handle_letter(self, line):
        new_token = line[-1].replace('[', '').replace(']','').replace("'",'').replace('"','')
        self.letter_val = self.get_alphas(new_token)
        return self.get_alphas(new_token)
    
    def handle_digit(self, line):
        new_token = line[-1].replace('[', '').replace(']','').replace("'",'').replace('"','')
        self.digit_val = new_token
        return self.get_digits(new_token)
    
    def handle_digits(self, line):
        new_token = line[-1].replace('[', '').replace(']','').replace("'",'').replace('"','').replace('+', '')
        if new_token == 'digit':
            return f'{self.get_digits(self.digit_val)}|{self.get_digits(self.digit_val)}' 
    
    def handle_id(self, line):
        new_token = line[-1].replace('[', '').replace(']','').replace("'",'').replace('"','')
        if new_token == 'letter(letter|digit)*':
            return f'({self.letter_val}|{self.get_digits(self.digit_val)})*'
    
    def handle_number(self, line):
        return '(a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z$A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z|0$1$2$3$4$5$6$7$8$9$A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z)*'
    
    def handle_string(self, line):
        return f'_|_'
    
    def get_alphas(self, string):
        
        if string == 'A-Za-z':
            return 'a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z$A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z'
        elif string == 'a-z':
            return 'a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z'
        elif string == 'A-Z':
            return 'A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z'
        elif string == 'a-zA-Z':
            return 'A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z$a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z'
        
        else:
            raise Exception('Syntax Error: variable declaration is incorrect: ',string, 'is not a valid rule.')
    
    def get_digits(self,string):
        if string == '':
            return ''
        elif string == '0-9' or '0123456789':
            return '0$1$2$3$4$5$6$7$8$9'
        elif string == '0-8':
            return '0$1$2$3$4$5$6$7$8'
        elif string == '0-7':
            return '0$1$2$3$4$5$6$7'
        elif string == '0-6':
            return '0$1$2$3$4$5$6'
        elif string == '0-5':
            return '0$1$2$3$4$5'
        elif string == '0-4':
            return '0$1$2$3$4'
        elif string == '0-3':
            return '0$1$2$3'
        elif string == '0-2':
            return '0$1$2'
        elif string == '0-1':
            return '0$1'
        elif len(string) == 1:
            return string
        else:
            raise Exception('Syntax Error: variable declaration is incorrect: ',string, 'is not a valid rule.')
    

def clean_tokens(tokens:list):
    return [x for x in tokens if x is not None]


# slr-1.yal.txt
# slr-2.yal.txt
# slr-3.yal.txt
# slr-4.yal.txt

file_number = input('Enter file number: ')
yal = YAlexTokenizer(f'slr-{file_number}.yal.txt')
yal.get_tokens()
tokens = clean_tokens(yal.tokens)

counter = 0
while counter < len(tokens):
    expression = tokens[counter]
    postfix = Regex(expression).postfix
    print(f'Infix: {expression}\nPostfix: {postfix}\n')
    nfa = NFA_(postfix)
    print('NFA:')
    nfa.showNFA(nfa.result[0])
    new_nfa = nfa.to_dict()
    graph = nfa.visualize_nfa()
    graph.render()

    next = input('press any key for next token: ')
    if next == '':
        counter += 1
        
    






