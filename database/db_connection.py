import os
import sqlite3
import sys

try:
    from config import DATABASE_NAME
except ModuleNotFoundError:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from config import DATABASE_NAME


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection