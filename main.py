import sqlite3
from pathlib import Path
from typing import Iterable
from multiprocessing import Queue, Process, Pool
from modules.content import FileRecord, RawText, StructuredText, Document, Image, UnknownContent

# Database Connection
conn = sqlite3.connect('content.db')
cursor = conn.cursor()

# Create File Contents Table
cursor.execute('''CREATE TABLE IF NOT EXISTS FileContents (
                id INTEGER PRIMARY KEY
                path TEXT,
                content TEXT,
                name TEXT,
                type TEXT,
                size INTEGER,
                date_created TEXT,
                date_modified TEXT
                )''')

def process_file(file: FileRecord, db_cursor) -> None:
    content = file.get_content()
    db_cursor.execute('''INSERT INTO FileContents (path, content, name, type, size, date_created, date_modified)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (file.path, content, file.name, file.type, file.size, file.date_created, file.date_modified))

def worker(queue: Queue, db_cursor) -> None:
    while True:
        file = queue.get()
        process_file(file, db_cursor)
        queue.task_done()

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
    num_threads = 4
    processes = []
    
    for _ in range(num_threads):
        p = Process(target=worker, args=(queue, cursor))
        p.start()
        processes.append(p)
    
    # Wait for all threads to finish
    queue.join()
    
    # Stop database insertion process
    for _ in range(num_threads):
        queue.put(None) 
    for p in processes:
        p.join()
    
    # Commit and close database
    conn.commit()
    conn.close()
