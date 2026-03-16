class InputBuffer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def next_char(self):
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.pos += 1
            return ch
        return None