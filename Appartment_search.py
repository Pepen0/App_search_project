from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

# Excel variable
import pandas as pd

Excel_path = "/Users/penoelothibeaud/Desktop/projet/Software engineering/Personal project/Appartment condition check/App_search_project/Appartment_database_template.xlsx"
Criteria_sheet_title = "Criteria"
reading_engine = "openpyxl"
Row_to_skip = 0
Collumn_to_read = "B"


# webdriver variable

Search_Appart_bot = webdriver.Chrome()
listing_counter = 0
max_listing = 0

# criteria

Location = ""
goal = ""
Type = ""
max_price = 0
minimum_bedroom = 0
minimum_bathroom = 0
number_of_listing_goal = 0
Proximity_to = ""


# page research result

Address = ""  # Send this to the google map page to analyse
price = 0
Bedroom = 0
Bathroom = 0
Link = ""
Finder = "Search_bot"
Contact_info = 0
Status = "To be check by human "
Description = ""  # Send this to Chat Gpt Api to analyse


# google map API result

distance_from_uni = 0
Transportation_type = ""
Transportation_line = ""
Transportation_station = ""

# Chat GPT API result

Parking_available = "?"
Parking_spot = 0
Parking_extra_price = 0
Hot_water = "?"
Heating = "?"
Electricity = "?"
Wifi = "?"
A_C = "?"
Appliances = "?"
Gym = "?"
Pool = "?"
Spa = "?"
Elevator = "?"


def extract_criteria_from_excel():
    print(
        "extracting Location,goal,Type,max_price,minimum_bedroom,minimum_bathroom,number_of_listing_goal from the excel file"
    )

    Criteria_list = pd.read_excel(
        Excel_path,
        usecols=Collumn_to_read,
        skiprows=Row_to_skip,
        engine=reading_engine,
        sheet_name=Criteria_sheet_title,
    )

    global Location
    global goal
    global Type
    global max_price
    global minimum_bedroom
    global minimum_bathroom
    global number_of_listing_goal
    global Proximity_to

    Location = Criteria_list.iloc[0, 0]
    goal = Criteria_list.iloc[1, 0]
    Type = Criteria_list.iloc[2, 0]
    max_price = Criteria_list.iloc[3, 0]
    minimum_bedroom = Criteria_list.iloc[4, 0]
    minimum_bathroom = Criteria_list.iloc[5, 0]
    number_of_listing_goal = Criteria_list.iloc[6, 0]
    Proximity_to = Criteria_list.iloc[7, 0]


def fill_search_page():
    print("entering info in page")

    Search_Appart_bot.find_element(
        By.XPATH,
        "//input[@placeholder='Search by City, Neighbourhood, Region, Address or Centris N°']",
    ).send_keys(Location)

    time.sleep(2)

    Search_Appart_bot.find_element(
        By.XPATH,
        "//input[@placeholder='Search by City, Neighbourhood, Region, Address or Centris N°']",
    ).send_keys(Keys.ENTER)

    time.sleep(5)

    # Click on the Select2 dropdown to expand it
    select2_container = Search_Appart_bot.find_element(
        By.CSS_SELECTOR, ".select2-selection.select2-selection--single"
    )
    select2_container.click()

    # Select the "For sale" option
    option = Search_Appart_bot.find_element(By.XPATH, '//option[text()="For rent"]')
    option.click()

    time.sleep(5)


def find_total_page():
    print("finding the number of option that match the search ")
    return


def run_search():
    print("adjusting search in " + Search_Appart_bot.title + " based on criteria")

    max_listing = find_total_page()

    # if max_listing >= number_of_listing_goal:
    #     # run the loop till listing goal
    #     for i in range(number_of_listing_goal):
    #         visit_option(i)

    #     return

    # # else run loop till max listing since we cant reach the listing goal
    # print("Only " + max_listing + " valid option(s) ")

    # for i in range(max_listing):
    #     visit_option(i)


def visit_option(x):
    print("looping trought option number " + x)
    listing_counter = x

    Collect_info()
    proccess_with_GPT()

    transfer_to_excel()


def Collect_info():
    print(
        "openning option " + listing_counter + "option address"
    )  # make it print the proper adress


def proccess_with_GPT():
    print("Sending info to gpt")


def transfer_to_excel():
    print("writing in excel ")


def run_program():
    print("starting the program")

    extract_criteria_from_excel()

    Search_Appart_bot.get("https://www.centris.ca/en")

    time.sleep(3)

    fill_search_page()

    # run_search()

    Search_Appart_bot.quit()


run_program()
