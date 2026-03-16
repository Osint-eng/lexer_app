 class InputBuffer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.buffer_output = []

    def next_char(self):
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.buffer_output.append(ch)   # store char
            self.pos += 1
            return ch
        return None

    def get_buffer(self):
        return self.buffer_output
