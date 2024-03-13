from functools import wraps
from contextlib import contextmanager
from pathlib import Path
import tempfile
import shutil

@contextmanager
def _temporary_copy(path):
    """Context manager for handling temporary copies of files"""
    original_path = Path(path)
    with tempfile.NamedTemporaryFile(delete=False, dir=tempfile.gettempdir(), prefix=original_path.name) as temp_file:
        shutil.copy(original_path, temp_file.name)
        yield Path(temp_file.name)  # Yield temporary path for use in with block
    Path(temp_file.name).unlink()  # Ensure the temporary file is deleted

def with_temporary_copy(method):
    """Decorator to create a temporary copy of a file and pass it to a function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with _temporary_copy(self.path) as temp_path:
            original_path = self.path  # Save original path
            self.path = temp_path  # Set path to temporary path
            try:
                result = method(self, *args, **kwargs)  # Call the method
            finally:
                self.path = original_path  # Restore original path
            return result
    return wrapper