import chardet

def open_with_auto_encoding(file, mode="r"):
    """Open a file with the correct encoding"""
    with open(file, mode) as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)["encoding"]
        return open(file, mode, encoding=encoding)
