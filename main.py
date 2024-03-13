from pathlib import Path
from threading import Thread
from queue import Queue
from typing import Iterable
from modules.content import *

def walk(path: Path) -> Iterable[Path]:
    """Walk through a directory tree and iteratively yield all files"""
    for item in path.iterdir():
        if item.is_dir():
            yield from walk(item)
        else:
            yield item

if __name__ == "__main__":
    test_path = Path("test")
    
    # Main Queue
    queue = [] #Queue()

    #Testing
    for file in walk(test_path):
        
        match file.suffix:
            
            # Text Files
            case ".txt" | ".md" | ".log":
                queue.append(RawText(file))
            
            case ".docx":
            
            # Default
            case _:
                queue.append(UnknownContent(file))

    # Process Queue
    for item in queue:
        print(repr(item))


