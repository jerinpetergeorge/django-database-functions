class Format(dict):
    def __missing__(self, key):
        return '%(' + key + ')s'