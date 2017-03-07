from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json


# css selector for sider to get side effects and indications
TABLE_SELECTOR = '#drugInfoTable'
TERM_SELECOTR = "table tr td a[href^='/se']"


def get_med_names():
    """
    read the 100 medicine names from file
    """
    names = list()
    with open('med_names.txt', 'r') as f:
        for line in f:
            names.append(line.strip().lower())
    return names


def get_terms(table):
    """
    extract side effects terms and indication terms from the table element
    """
    terms = list()
    for term in table.find_elements_by_css_selector(TERM_SELECOTR):
        terms.append(term.text)
    return terms


med_names = get_med_names()
driver = webdriver.Chrome()
final_results = {}

# search every medicine name as keyword
for name in med_names:
    driver.get("http://sideeffects.embl.de/")
    # locate to the search box
    elem = driver.find_element_by_name("q")
    elem.clear()
    # put the medicine name in the search box
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)  # wait until the site is fully rendered
    # there are two tables, one for side effects and one for indications
    se_tables = driver.find_elements_by_css_selector(TABLE_SELECTOR)
    if se_tables:
        side_effects = get_terms(se_tables[0])
        indications = get_terms(se_tables[1])
        final_results[name] = {
            'side effects': side_effects, 'indications': indications}

driver.close()

# write result into json file
with open('sider.json', 'w') as f:
    json.dump(final_results, f, indent=2)
