class YAlexTokenizer:
    def __init__(self, path_to_file:str) -> None:
        self.path = path_to_file
        self.var_prefixes = ['let', 'var', 'const','global', 'static']
        self.var_def_rules = ['delim', 'ws', 'letter', 'digit', 'digits', 'id', 'number']
        self.lines = self.returnLines()
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
                
    def default_rules(self, lista) -> None:
        if lista[1] == 'delim':
            pass
        elif lista[1] == 'ws':
            pass
        elif lista[1] == 'letter':
            pass
        elif lista[1] == 'digit':
            pass
        elif lista[1] == 'digits':
            pass
        elif lista[1] == 'id':
            pass
        elif lista[1] == 'number':
            pass
        
    def check_grammar_vars(self, line):
        
        if line[0] not in self.var_prefixes:
            raise Exception(f'Syntax Error: variable declaration is incorrect.\nSee element: {line}')
        elif line[1] not in self.var_def_rules:
            raise Exception('Syntax Error: variable declaration is incorrect: ',line[1], 'is not a valid rule.')
        elif line[2] != '=':
            raise Exception('Syntax Error: variable declaration is incorrect: ',line[2], 'not valid.')
        
yal = YAlexTokenizer('myYALex.txt')
yal.get_tokens()


