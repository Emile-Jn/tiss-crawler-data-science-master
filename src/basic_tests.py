# -*- coding: utf-8 -*-
#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.service import Service as SafariService
import time
from dataclasses import dataclass
import pandas as pd

service = SafariService('/usr/bin/safaridriver')
driver = webdriver.Safari(service=service)
driver.get("https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?dswid=7871&dsrid=370&key=67853")
time.sleep(5)
driver.implicitly_wait(0.5)

test = driver.find_element(By.ID, "j_id_2i:nodeTable_data")

#%%
rows = test.find_elements(By.TAG_NAME, "tr")

#%% modules
"""
@dataclass
class Course:
    title: str
    code: str
    type: str
    semester: str
    credits: int

curriculum = {
    'foundations': [],
    'domain-specific aspects': [],
    'FDS/CO': [],
    'FDS/EX': [],
    'MLS/CO': [],
    'MLS/EX': [],
    'BDHPC/CO': [],
    'BDHPC/EX': [],
    'VAST/CO': [],
    'VAST/EX': [],
    'Thesis': [Course('Diploma thesis', "N/A", "N/A", "N/A", 30)],
}

keys = list(curriculum.keys())
"""
curriculum = pd.DataFrame(columns=['module', 'title', 'code', 'type', 'semester', 'credits'])

section_names = [
    'Prüfungsfach Data Science - Foundations',
    'Prüfungsfach Domain-Specific Aspects of Data Science',
    'Modul FDS/CO - Fundamentals of Data Science - Core',
    'Modul FDS/EX - Fundamentals of Data Science - Extension',
    'Modul MLS/CO - Machine Learning and Statistics - Core',
    'Modul MLS/EX - Machine Learning and Statistics - Extension',
    'Modul BDHPC/CO - Big Data and High Performance Computing - Core',
    'Modul BDHPC/EX - Big Data and High Performance Computing - Extension',
    'Modul VAST/CO - Visual Analytics and Semantic Technologies - Core',
    'Modul VAST/EX - Visual Analytics and Semantic Technologies - Extension',
    'Prüfungsfach Freie Wahlfächer und Transferable Skills'
]


#%%

n_courses = 0
section_number = -1 # start with no section

for i in range(1, len(rows)):  # skip row 0 which just says "Master Data Science"
    if section_number == -1 and  i > 3:
        raise ValueError("Could not find the first section of the curriculum in the first 3 rows.")
    # for each rows, get the 4 grid cells
    cells = rows[i].find_elements(By.TAG_NAME, "td")
    # if the row is a new section of the curriculum, move to that section
    text = cells[0].text.strip()
    print(f'matching {text} with {section_names[section_number+1]}')
    if text == section_names[section_number+1]:
        section_number += 1
        if section_number > len(section_names) - 2:
            break
        continue
    # Check if the row contains a hyperlink
    hyperlinks = rows[i].find_elements(By.TAG_NAME, "a")
    if hyperlinks:  #if there is at least one hyperlink in the row
        # get the course key
        course_key = cells[0].find_element(By.CLASS_NAME, "courseKey").text.strip()
        # get the title of the course
        course_title = cells[0].find_element(By.CLASS_NAME, "courseTitle").text.strip()
        # split the course key into the course code, type, and semester
        course_info = course_key.split(" ")
        # get the number of ECTS credits from the last cell in the row
        ects = int(float(cells[3].text))
        # make a new course object
        # course = Course(course_title, course_info[0], course_info[1], course_info[2], ects)
        # add the course to the curriculum
        # curriculum[keys[section_number]].append(course)
        new_row = pd.DataFrame(
            {'module': [section_names[section_number]],
             'title': [course_title],
             'code': [course_info[0]],
             'type': [course_info[1]],
             'semester': [course_info[2]],
             'credits': [ects]})
        curriculum = pd.concat([curriculum, new_row], ignore_index=True)
        n_courses += 1

print(f'There were {n_courses} found in the curriculum page.')
#%% transform the curriculum into a table of courses

