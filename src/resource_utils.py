"""
Resource path utilities for PyInstaller compatibility.
"""
import os
import sys


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    Works both in development and when bundled with PyInstaller.
    
    Args:
        relative_path: Path relative to the project root
        
    Returns:
        Absolute path to the resource
    """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running as normal Python script
        # Go up from src/ to project root
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)
