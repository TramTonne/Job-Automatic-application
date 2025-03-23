from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ACCOUNT_EMAIL = "tonnuquynhtram2004@gmail.com"
ACCOUNT_PASSWORD = "Tramton123"
PHONE = "8137241905"

def abort_application():
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
        )
        close_button.click()
        time.sleep(2)

        discard_buttons = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
        if len(discard_buttons) > 1:
            discard_buttons[1].click()
    except (NoSuchElementException, TimeoutException):
        print("🔹 No modal to close.")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=4180915206&f_AL=true&geoId=103644278&keywords=software%20engineer%20intern&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true"
)

try:
    time.sleep(2)
    reject_button = driver.find_element(By.CSS_SELECTOR, 'button[action-type="DENY"]')
    reject_button.click()
except NoSuchElementException:
    print("🔹 No cookie rejection button found. Skipping...")

time.sleep(2)

# Wait for and click the "Sign in" button
try:
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
    )
    driver.execute_script("arguments[0].click();", sign_in_button)  # Click using JavaScript
except (NoSuchElementException, TimeoutException):
    print("🔹 Sign in button not found.")
    driver.quit()
    exit()

# Sign in process
time.sleep(5)
email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

# You may be presented with a CAPTCHA
input("Press Enter when you have solved the Captcha")

time.sleep(5)
all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

# Apply for Jobs
for listing in all_listings:
    print("Opening Listing")
    
    # Ensure any pop-ups are closed before clicking
    try:
        WebDriverWait(driver, 3).until(EC.invisibility_of_element((By.CLASS_NAME, "artdeco-modal__content")))
    except TimeoutException:
        print("🔹 No pop-up detected, continuing.")

    try:
        listing.click()
    except ElementClickInterceptedException:
        print("🔹 Element click intercepted, using JavaScript to click.")
        driver.execute_script("arguments[0].click();", listing)

    time.sleep(2)

    time.sleep(2)
    try:
        apply_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button"))
        )
        apply_button.click()

        # Insert Phone Number
        time.sleep(5)
        phone = driver.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
        if phone.text == "":
            phone.send_keys(PHONE)

        # Check the Submit Button
        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()
