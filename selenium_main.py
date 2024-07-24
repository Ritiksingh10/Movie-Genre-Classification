
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define your login credentials and URL
url = 'https://cloud.webscraper.io/login'
username = 'riitian10@gmail.com'
password = 'Test@123'

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Open the login page
    driver.get(url)
    
    # Wait for the username field to be present, then enter the username
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    ).send_keys(username)
    
    # Enter the password
    driver.find_element(By.NAME, 'password').send_keys(password)
    
    # Submit the login form
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)


    # Wait for the login process to complete and the dashboard to load
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'small-screen-text'))
        )
        print("Login successful")


        # Find and click on Account info tab
        account_info_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Account Info')]"))
        )
        account_info_tab.click()
        print("Navigated to Account Info tab")

        # Take a screenshot of the Account Info page
        driver.save_screenshot('account_info_screenshot.png')
        print("Screenshot taken for Account Info page")
        
        
        
        # Scrape specific data from the dashboard
        data_element = driver.find_element(By.CSS_SELECTOR, '.table.m-top-10.m-btm-0')
        scraped_data = data_element.text
    

        # Parse the scraped text into a structured format
        data_rows = []
        lines = scraped_data.strip().split('\n')
        for line in lines:
            key, value = map(str.strip, line.split(':', 1))
            data_rows.append([key, value])

        # Write the structured data into a CSV file
        with open('scraped_data.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Attribute', 'Value'])  # Header row
            csvwriter.writerows(data_rows)

        print("Data saved to 'scraped_data.csv'")

        # Print the scraped data
        print('Scraped Data:', scraped_data)
    except TimeoutException:
        try:
            error_message="Authentication failed."
            
            print(f"Login failed: {error_message}")
        except NoSuchElementException:
            print("Login failed: Unknown error occurred")


    
except TimeoutException:
    print("Element not found within the given time frame.")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
finally:
    # Close the WebDriver
    driver.quit()

