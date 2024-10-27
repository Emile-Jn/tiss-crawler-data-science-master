# -*- coding: utf-8 -*-
#!/usr/bin/python3

from pathlib import Path
import os
import sys

"""
# Check if __file__ is defined
if '__file__' in globals():
    script_dir = Path(__file__).resolve().parent
else:
    # Fallback: manually set the script directory
    script_dir = Path(sys.argv[0]).resolve().parent

# Change the current working directory to the script's directory
os.chdir(script_dir)

# Add the script's directory to the Python path
sys.path.insert(0, str(script_dir))
"""

# beginning of section copied from src/extract_process_study_programs.py
# - - -
try:
    import crawl
except ModuleNotFoundError:
    import src.crawl as crawl
from config import *

# TODO: set language (subsemester) to english (DB!)

# initiate driver (instance)
crawl_delay = 10
driver_instance = crawl.crawler(False, 800, 600, crawl_delay)
driver = driver_instance.init_driver()

# - - -
# end of section copied from src/extract_process_study_programs.py

urls_in_range = driver_instance.extract_fundamentals(driver, "https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?dswid=7871&dsrid=370&key=67853")
