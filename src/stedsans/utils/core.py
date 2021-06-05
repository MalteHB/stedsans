"""Core utilities for stedsans
"""
import pathlib
import io


def read_file(file, encoding="utf-8"):
    """
    Check if the input is a file or not.

    Args:
        file ([str, io.IOBase or pathlib.PurePath], optional): file object. Defaults to None.

    Raises:
        AttributeError: If wrong type is passed raise error.
            
    Returns:
        text [str]: text from file
    """
    
    if isinstance(file, str):
        
        text = file
    
    elif isinstance(file, pathlib.PurePath):
                
        text = file.read_text(encoding=encoding)
                
    elif isinstance(file, io.IOBase):
            
        text = file.read(encoding=encoding)
        
        

    else:
        
        raise AttributeError(f"{file} is neither of type string, io.IOBase or pathlib.PurePath.")
    
    return text
