# -*- coding: utf-8 -*-
#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.support.ui import Select
import time
from dataclasses import dataclass
import pandas as pd

# TODO: adapt code for other browsers
service = SafariService('/usr/bin/safaridriver')
driver = webdriver.Safari(service=service)

driver.get("https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?dswid=7871&dsrid=370&key=67853")
time.sleep(5)  # wait 5 seconds to let the page load
driver.implicitly_wait(0.5)
# Language of the page is German by default, switch it to English
driver.find_element("id", "language_en").click()
# Wait for the page to reload
time.sleep(3)  # Adjust the sleep time if necessary

#%% modules

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
# Locate the semester select element
semester_select = Select(driver.find_element('name', 'j_id_2i:semesterSelect'))

for semester in semester_select.options:
    # Re-locate the semester select element
    semester_select = Select(driver.find_element('name', 'j_id_2i:semesterSelect'))
    # Select each semester by visible text
    semester_select.select_by_visible_text(semester.text)
    print(f'\n Processing the semester {semester.text} \n')
    time.sleep(3)  # wait 3 seconds to let the page load
    table = driver.find_element(By.ID, "j_id_2i:nodeTable_data")
    rows = table.find_elements(By.TAG_NAME, "tr")

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

    print(f'There were {n_courses} courses found in the curriculum page.')

#%% write the curriculum to a tsv file
curriculum.drop_duplicates().to_csv('curriculum1.tsv', sep='\t', index=False)

