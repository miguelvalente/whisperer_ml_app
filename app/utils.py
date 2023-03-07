from pathlib import Path
def is_plural(size):
    return "s" if size > 1 else ""

def get_files_ignore_hidden(path):
    return [x for x in path.iterdir() if not x.name.startswith(".")]