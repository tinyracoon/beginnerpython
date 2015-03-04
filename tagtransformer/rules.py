'''
'''

class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ":"

class TitleRule(Rule):
    type = 'title'
    title = True
    def condition(self, block):
        if not self.title: return False
        self.title = False
        return HeadingRule().condition(block)

class ListItemRule(Rule):
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True
class ListRule(Rule):
    type = 'list'
    inside = False
    def condition(self, block):
        True
    def action(self, block, handler):
        if not self.inside and ListItemRule().condition(block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule().condition(block):
            handler.end(self.type)
            self.inside = False
        return False
class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self, block):
        return True
            
            