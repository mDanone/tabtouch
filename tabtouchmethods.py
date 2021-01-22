import csv
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delay():
    return time.sleep(random.randint(2, 3))


def getHorseRaceInfo(driver):
    result = {}

    # main block with players
    try:
        block_players = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flat-runners-list"))
        )
    except:
        driver.quit()

    # List of blocks with information about players
    list_of_players = block_players.find_elements_by_tag_name('li')

    for player in list_of_players:
        keys = []
        values = []
        ul_elements = []
        li_elements = []
        clicker = player.find_element_by_class_name("selection-form-table")
        clicker.click()
        delay()
        name = player.find_element_by_class_name("selection-name").text

        # Defining tables
        try:
            tables = player.find_elements(By.XPATH, "//*[contains(@class,'formlist')]")
        except:
            driver.quit()
            print("no information about players")

        # Going deep into blocks of information to find text
        for table in tables:
            ul_elements.extend([el for el in table.find_elements_by_tag_name("ul")])
        for ul in ul_elements:
            li_elements.extend([li for li in ul.find_elements_by_tag_name("li")])

        # Defining each key and value of information about player
        keys = [li.text.split('\n')[0] for li in li_elements]
        values = [
            li.text.split('\n')[1] if len(li.text.split('\n')) >= 2 else 'Null' for li in li_elements
        ]

        result |= {name: {keys[i]: values[i] for i in range(len(keys))}}

        clicker.click()
        delay()

    return result


def getDogRaceInfo(driver):
    result = {}
    keys = []
    values = []

    # num_of_formlists needs to count blocks of player`s information
    num_of_formlists = 1

    try:
        players = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "selection-info"))
        )
    except:
        driver.quit()

    for player in players:
        player.click()
        delay()
        name = player.find_element_by_class_name("selection-name").text

        # gettin information block
        try:
            formlist = player.find_element_by_xpath(
                "//*[@id='winplace']/div/starters-list/ul/li[" + str(num_of_formlists) + 
                "]/dog-starter/form-info/div/div/div[2]/div/div/dog-formdata/div[1]"
            )
        except:
            driver.quit()
            print("No Information to parse")

        # Getting player`s information from tables
        try:
            tables = formlist.find_elements_by_tag_name("ul")[:2]
        except:
            driver.quit()
            print("No Information")
        for i in range(len(tables)):
            keys.extend([
                i.text.split("\n")[0] for i in tables[i].find_elements_by_tag_name("li")
            ])
            values.extend([
                i.text.split("\n")[1] for i in tables[i].find_elements_by_tag_name("li")
            ])
        result |= {name: {keys[i]: values[i] for i in range(len(keys))}}

        # transition to the next player`s page
        player.click()
        delay()

        # counting number of player
        num_of_formlists += 1

    return result


def getRacePage(driver, name, code):
    # getting the main page with list of races
    driver.get('https://www.tabtouch.mobi/#')
    driver.find_element_by_xpath('//*[@id="redirect-mobile"]').click()
    delay()
    driver.find_element_by_xpath('//*[@id="content"]/div[5]/a').click()
    delay()

    # Here we are searching for race we need
    races = driver.find_elements_by_class_name("css-lwgudr")
    for race in races:
        if name.upper() == race.text.split('\n')[1] and code == race.text.split('\n')[2].split(' ')[0]:
            try:
                type_of_race = race.find_element_by_class_name(
                    "css-1fpbujr").get_attribute('data-tid-icon-type'
                                                 )
                delay()
                race.click()
                break
            except:
                driver.quit()
                print('No results')

    # return type of race we need (races, dog)
    return type_of_race


def SaveResult(result, name, code):
    # Saving results
    with open("{} {}.csv".format(name, code), 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ')
        for key, values in result.items():
            csvwriter.writerow([key + "\n"])
            for key, value in values.items():
                csvwriter.writerow([key, ":", value])


def RunScript(driver, name, code):
    # Starting script
    type_of_race = getRacePage(driver, name, code)
    if type_of_race == "races":
        result = getHorseRaceInfo(driver)
    else:
        result = getDogRaceInfo(driver)
    SaveResult(result, name, code)
