class source_node(object):
    def __init__(self, node_index):
        self.text = ''
        self.has_next = False
        self.align_target_index = -1
        self.shortlist = -1
        self.node_index = node_index
        self.color_index = -1
        
    def set_text(self, text):
        self.text = text
        
    def alter_tag(self):
        self.has_next = True
    
    def set_align_index(self, index):
        self.align_target_index = index
        
    def set_color(self, color_index):
        self.color_index = color_index
        
    def set_shortlist(self, shortlist):
        self.shortlist = shortlist
        
    def print_node(self):
        print('text', self.text, '  tag', self.has_next, ' align_target_index ', self.align_target_index, 'color_index', self.color_index)