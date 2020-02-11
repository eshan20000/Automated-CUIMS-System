from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
from tabulate import tabulate

def screenshot_Attendance(uid, password):
    # create a new Firefox session
    opts = Options()
    opts.add_argument('-headless')
    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(30)
    driver.maximize_window()

    # Navigate to the application home page
    driver.get("https://uims.cuchd.in")
    print("Page Opened")

    # Click the UID Input Field, enter the UID and Submit
    driver.find_element_by_name("txtUserId").send_keys(uid)
    driver.find_element_by_name("btnNext").click()

    # Enter the Password and Submit
    driver.find_element_by_name("txtLoginPassword").send_keys(password)
    driver.find_element_by_name("btnLogin").click()
    print("UID and Password Entered and Submitted")

    # Click the Attendance Button
    attendanceBtn = driver.find_element_by_xpath("/html/body/form/div[4]/div[1]/div/div[1]/ul/li[3]/a")
    driver.execute_script("arguments[0].click();", attendanceBtn)
    print("Attendance Paged Opened")

    # Screenshot the Attendance Page
    time.sleep(5)
    driver.execute_script("document.getElementById('header').style.position = 'relative';")
    driver.find_element_by_xpath("/html/body/form/div[4]/div[3]").screenshot("C:/Users/Development/Desktop/attendance.png")

    # Scraping the Attendance Page
    pageSource = driver.page_source
    soupData = BeautifulSoup(pageSource, "lxml")
    table = soupData.table
    list_of_rows = []
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll(['th', 'td']):
            text = cell.text.strip()
            if text == "View Attendance":
                list_of_cells.append("")
                continue
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)

    print("Page Scraped!")

    with open(r"C:\Users\Development\PycharmProjects\Project(4 Semester)\venv\Selenium Project\output_table.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(list_of_rows)

    # Create and Display the Table
    lenth = len(list_of_rows)
    print(tabulate(list_of_rows[1], headers=list_of_rows[0], tablefmt="grid"))

    # todo : Make the Program run on While Loop

    # close the browser window
    ch = input("Would you like to Quit?")
    if ch == "yes":
        driver.quit()

print("Welcome to CUIMS!")
print("What would you like to do today?")
print("1. Screenshot Attendance")
print("2. Blah Blah Blah")
ch = int(input("Choice: "))
uid = input("Please enter your UID: ")
password = input("Please enter your Password: ")

if(ch == 1):
	screenshot_Attendance(uid, password)
else:
    print("Sorry..... Wrong Input!")