from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

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


def find_total_page():
    print("finding the number of option that match the search ")
    return


def run_search():
    print("adjusting search based on criteria")
    max_listing = find_total_page()

    if max_listing >= number_of_listing_goal:
        # run the loop till listing goal
        for i in range(number_of_listing_goal):
            visit_option(i)

        return

    # else run loop till max listing since we cant reach the listing goal
    print("Only " + max_listing + " valid option(s) ")

    for i in range(max_listing):
        visit_option(i)


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

    # run_search()


run_program()
