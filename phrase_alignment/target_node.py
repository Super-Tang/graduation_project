class target_node(object):
    def __init__(self, node_index):
        self.text = ''
        self.has_next = False
        self.align_source_index = -1
        self.shortlist = -1
        self.node_index = node_index
        self.color_index = -1
        self.is_pun = False
        
    def set_text(self, text):
        self.text = text
        
    def alter_tag(self):
        self.has_next = True
        
    def set_align_index(self, index):
        self.align_source_index = index
        
    def set_shortlist(self, shortlist):
        self.shortlist = shortlist
        
    def set_color(self, color):
        self.color_index = color

    def alter_pun(self):
        self.is_pun = True
        
    def print_node(self):
        print('text', self.text, '  tag', self.has_next, ' align_source_index ', self.align_source_index, ' color', self.color_index)