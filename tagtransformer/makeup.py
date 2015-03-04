'''
'''
import sys, re
from handlers import *
from util import *
from rules import *

class Parser:
    def __init__(self, handler):
        self.hander = handler
        self.rules = []
        self.filters = []
    
    def addRule(self, rule):
        self.rules.append(rule)
    def addFilter(self, pattern, name):
        def filtermethod(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filtermethod)
    def parse(self, f):
        self.hander.start('document')
        for block in blocks(f):
            for fm in self.filters:
                block = fm(block, self.hander)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.hander)
                    if last: break
        self.hander.end('document')

class BasicTextParser(Parser):
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())
        
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z0-9/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z0-9]+@[\.a-zA-Z0-9]+[a-zA-Z]+)', 'mail')
hanlder = HTMLRender()
parser = BasicTextParser(hanlder)
with open('./test_input.txt') as f:
    parser.parse(f)