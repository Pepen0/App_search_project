from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

# Excel variable
import pandas as pd

Excel_path = "/Users/penoelothibeaud/Desktop/projet/Software engineering/Personal project/Appartment condition check/App_search_project/Appartment_database_template.xlsx"
Criteria_sheet_title = "Criteria"
reading_engine = "openpyxl"
Row_to_skip = 0
Collumn_to_read = "B"


# webdriver variable

Search_Appart_bot = webdriver.Firefox()
listing_counter = 0
max_listing = 0
price_slider = []

# criteria

Location = ""
goal = ""
Type = ""
max_price = 0
min_price = 0
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

    print(len(Criteria_list))

    global Location
    global goal
    global Type
    global max_price
    global min_price
    global minimum_bedroom
    global minimum_bathroom
    global number_of_listing_goal
    global Proximity_to

    Location = Criteria_list.iloc[0, 0]
    goal = Criteria_list.iloc[1, 0]
    Type = Criteria_list.iloc[2, 0]
    max_price = Criteria_list.iloc[3, 0]
    min_price = Criteria_list.iloc[4, 0]
    minimum_bedroom = Criteria_list.iloc[5, 0]
    minimum_bathroom = Criteria_list.iloc[6, 0]
    number_of_listing_goal = Criteria_list.iloc[7, 0]
    Proximity_to = Criteria_list.iloc[8, 0]


def fill_search_page():
    global price_slider
    global min_price
    global max_price
    global minimum_bedroom
    global minimum_bathroom

    print("entering info in page")

    # change the location

    Search_Appart_bot.find_element(
        By.XPATH,
        "//input[@placeholder='Search by City, Neighbourhood, Region, Address or Centris N°']",
    ).send_keys(Location)

    time.sleep(1)

    Search_Appart_bot.find_element(
        By.XPATH,
        "//input[@placeholder='Search by City, Neighbourhood, Region, Address or Centris N°']",
    ).send_keys(Keys.ENTER)

    time.sleep(1)

    # change the type

    Type_select = Search_Appart_bot.find_element(
        By.CSS_SELECTOR, ".select2-selection.select2-selection--single"
    )
    Type_select.click()

    time.sleep(1)

    Type_option = Search_Appart_bot.find_element(
        By.XPATH, '//option[text()="' + Type + '"]'
    )
    Type_option.click()

    time.sleep(1)

    # Find where to slide

    price_elements = Search_Appart_bot.find_elements(
        By.XPATH, '//div[@id="RentPrice-slider-values"]/price'
    )

    for el in price_elements:
        price_value = int(el.get_attribute("data-field-value-id"))
        price_slider.append(price_value)

    # select the price range

    if (
        min_price >= max_price
    ):  # check that the min price is smaller then the max and fix it
        min_price = max_price - 500

    Price_select = Search_Appart_bot.find_element(
        By.XPATH, "//button[@id='RentPrice-button']//span[contains(text(),'Price')]"
    )
    Price_select.click()

    upper_bound_slide = Search_Appart_bot.find_element(
        By.XPATH,
        "//div[@class='primary-search-form search-section js-primary-form-other-field show-primary-filter']//div[6]",
    )
    lower_bound_slide = Search_Appart_bot.find_element(
        By.XPATH,
        "//div[@class='primary-search-form search-section js-primary-form-other-field show-primary-filter']//div[5]",
    )
    action_to_do = ActionChains(Search_Appart_bot)

    time.sleep(1)

    # apply minimum
    Min_price_option = Search_Appart_bot.find_element(
        By.XPATH,
        "//div[@class='collapse-body']//input[@class='RentPrice-slider-min']",
    )

    closest_min_price = min(price_slider, key=lambda x: abs(x - min_price))

    time.sleep(1)

    # apply maximum
    Max_price_option = Search_Appart_bot.find_element(
        By.XPATH,
        "//div[@class='collapse-body']//input[@class='RentPrice-slider-max']",
    )

    closest_max_price = min(price_slider, key=lambda x: abs(x - max_price))

    time.sleep(2)

    lower_bound = int(
        Min_price_option.get_attribute("value").replace("$", "").replace(",", "")
    )
    upper_bound = int(
        Max_price_option.get_attribute("value")
        .replace("$", "")
        .replace(",", "")
        .replace("+", "")
    )

    timer = time.time()

    while (lower_bound < closest_min_price) or (upper_bound > closest_max_price):
        lower_bound = int(
            Min_price_option.get_attribute("value").replace("$", "").replace(",", "")
        )
        upper_bound = int(
            Max_price_option.get_attribute("value")
            .replace("$", "")
            .replace(",", "")
            .replace("+", "")
        )

        time.sleep(0.001)

        upper_bound_slide = Search_Appart_bot.find_element(
            By.XPATH,
            '//*[@id="RentPrice"]/div[1]/div[1]/div[6]',
        )
        lower_bound_slide = Search_Appart_bot.find_element(
            By.XPATH,
            '//*[@id="RentPrice"]/div[1]/div[1]/div[5]',
        )

        if int(lower_bound) < closest_min_price:
            action_to_do.click_and_hold(lower_bound_slide).move_by_offset(
                5, 0
            ).release().perform()
            print(">")

        if int(upper_bound) > closest_max_price:
            action_to_do.click_and_hold(upper_bound_slide).move_by_offset(
                -5, 0
            ).release().perform()
            print("<")

        # print(
        #     str(closest_min_price)
        #     + " "
        #     + str(closest_max_price)
        #     + " "
        #     + str(price_slider[0])
        #     + " "
        #     + str(price_slider[48])
        #     + " "
        #     + str(lower_bound)
        #     + " "
        #     + str(upper_bound)
        # )

    print("good selection")

    # will apply the price restiction

    apply_price = Search_Appart_bot.find_element(
        By.XPATH, '//*[@id="RentPrice-collapse"]/div[2]/div/div/button[2]'
    )
    apply_price.click()

    time.sleep(1)

    open_filter = Search_Appart_bot.find_element(
        By.XPATH, "//span[normalize-space()='Filters']"
    )
    open_filter.click()

    time.sleep(1)

    feature_select = Search_Appart_bot.find_element(
        By.XPATH, '//*[@id="FeaturesSection-heading-filters"]/h2/button'
    )
    feature_select.click()

    time.sleep(1)

    Bedroom_select = Search_Appart_bot.find_element(
        By.XPATH, '//*[@id="Rooms"]/span/span[1]'
    )
    Bedroom_select.click()

    time.sleep(1)

    if minimum_bedroom == 1:
        minimum_bedroom_select = Search_Appart_bot.find_element(
            By.XPATH,
            '//option[text()="' + str(minimum_bedroom) + ' bedrooms or +"]',
        )

    if minimum_bedroom >= 5:
        minimum_bedroom = 5
        minimum_bedroom_select = Search_Appart_bot.find_element(
            By.XPATH,
            '//option[text()="' + str(minimum_bedroom) + ' bedrooms or +"]',
        )

    if minimum_bedroom != 1 or minimum_bedroom != 5 or minimum_bedroom != 0:
        minimum_bedroom_select = Search_Appart_bot.find_element(
            By.XPATH,
            '//option[text()="' + str(minimum_bedroom) + ' bedrooms or +"]',
        )

    minimum_bedroom_select.click()

    time.sleep(1)

    Bathroom_select = Search_Appart_bot.find_element(
        By.XPATH, '//*[@id="BathPowderRooms"]/span/span[1]'
    )
    Bathroom_select.click()

    time.sleep(1)

    if minimum_bathroom == 1:
        minimum_bathroom_select = Search_Appart_bot.find_element(
            By.XPATH,
            '//option[text()="' + str(minimum_bathroom) + ' bath/powder rooms or +"]',
        )

    if minimum_bathroom >= 5:
        minimum_bedroom = 5
        minimum_bathroom_select = Search_Appart_bot.find_element(
            By.XPATH,
            '//option[text()="' + str(minimum_bathroom) + ' bath/powder rooms or +"]',
        )

    if minimum_bathroom != 1 or minimum_bathroom != 5 or minimum_bathroom != 0:
        minimum_bathroom_select = Search_Appart_bot.find_element(
            By.XPATH,
            '//option[text()="' + str(minimum_bathroom) + ' bath/powder rooms or +"]',
        )

    minimum_bathroom_select.click()

    time.sleep(1)

    launch_search = Search_Appart_bot.find_element(
        By.ID, "js-home-button-search-container"
    )
    launch_search.click()

    time.sleep(2)


def run_search():
    global max_listing

    print(
        "looking at the search result in "
        + Search_Appart_bot.title
        + " based on criteria"
    )
    time.sleep(5)
    max_listing_finder = Search_Appart_bot.find_element(
        By.XPATH, "(//span[@class='resultCount'])[1]"
    )

    max_listing = int(max_listing_finder.get_attribute("textContent"))

    print("Total listing :" + str(max_listing))

    time.sleep(5)

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
    print("looping trought option number " + str(x))
    listing_counter = x
    # create and open excel file copy and save the links in there


def Collect_info():
    print(
        "openning option " + str(listing_counter) + "option address"
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

    run_search()

    Collect_info()
    proccess_with_GPT()

    transfer_to_excel()

    Search_Appart_bot.quit()


run_program()
