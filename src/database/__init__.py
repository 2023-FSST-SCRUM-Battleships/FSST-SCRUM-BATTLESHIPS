import os, importlib
from database.DatabaseHelper import *

module_dir = "src/database/entities/"
module_paths = [f"{module_dir}/{f}" for f in os.listdir(module_dir) if f.endswith(".py")]

modules = [importlib.import_module(f"database.entities.{os.path.splitext(f)[0].split('/')[-1]}") for f in module_paths]