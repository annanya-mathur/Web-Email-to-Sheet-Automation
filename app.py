from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a GUI window)
driver = webdriver.Chrome('path_to_chrome_webdriver', options=chrome_options)

# Read the list of websites from a file or any data source
websites = ['https://example1.com', 'https://example2.com', 'https://example3.com']

# Initialize a list to store the extracted email IDs
email_ids = []

# Loop through each website
for website in websites:
    # Navigate to the website
    driver.get(website)

    # Retrieve the page source
    page_source = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find email IDs using appropriate HTML tags and attributes
    # Adjust this code to match the specific structure of the target website
    email_elements = soup.find_all('a', href=lambda href: href and 'mailto:' in href)
    for element in email_elements:
        email_ids.append(element['href'].split(':')[1])

# Authenticate with Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('path_to_json_key_file', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet and select the worksheet
sheet = client.open('your_sheet_name').sheet1

# Write the email IDs to the Google Sheet
for i, email in enumerate(email_ids, start=2):  # Assuming headers are in the first row
    sheet.update_cell(i, 1, email)

# Close the browser
driver.quit()
