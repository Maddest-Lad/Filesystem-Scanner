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
    queue = Queue()

    #Testing
    for file in walk(test_path):
        
        match file.suffix:
            
            # Text Files
            case ".txt" | ".md" | ".log":
                queue.put(RawText(file))
            
            # Structured Text
            case ".json" | ".xml" | ".csv" | ".tsv":
                queue.put(StructuredText(file))
            
            # Documents
            case ".docx" | ".doc" | ".pptx" | ".ppt":
                queue.put(Document(file))
            
            # Images
            case ".png" | ".jpg" | ".jpeg" | ".gif" | ".bmp" | ".tiff" | ".webp":
                queue.put(Image(file))
            
            # Default
            case _:
                queue.put(UnknownContent(file))

    # Thread Pool
    # TODO Implement Threadpool to Dequeue and Process Files
    # TODO Implement Results Aggregator
    # TODO Vector Database to Store Results?
    num_threads = 4
    
    
        


