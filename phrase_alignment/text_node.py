class text_node(object):
    def __init__(self, text, color):
        self.text = text
        self.color = color
        
    def to_text(self):
        return (self.text, self.color)