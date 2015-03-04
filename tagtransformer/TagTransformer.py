'''
'''
import re
import util

class TagTransformer:
    HREF_RE = r'(http://[^\\(\\)]+)'
    
    def generatehtml(self, inputfile, outputfile_path):
        title = True
        result = '<html><header><title>...</title></header><body>'
        for block in util.blocks(inputfile):
            block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
            if title:
                result += '<h1>' + block + '</h1>'
                title = False
            else:
                block = self.handle_subtitle(block)
                block = self.handle_href(block)
                result += '<p>' + block + '</p>'
        result += '</body></html>'
        with open(outputfile_path, 'w') as f:
            f.write(result)
            f.flush()
    def handle_href(self, block):
        return re.sub(self.HREF_RE, '<a href="\1">\1</a>', block)
        
    def handle_subtitle(self, block):
        if self.issubtitle(block):
            return '<h2>' + block + '</h2>'
        return block
    
    def issubtitle(self, block):
        '''
            only one word
        '''
        if block and len(block.split(' ')) == 1:
            return True
        return False


if __name__ == '__main__':
    tt = TagTransformer()
    input_path = './test_input.txt'
    output_path = './test_output.html'
    print 'start to transforming input text file...'
    with open(input_path) as inputf:
        tt.generatehtml(inputf, output_path)
    print 'done!'