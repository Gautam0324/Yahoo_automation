import time
import random 
from botasaurus.browser import browser, Driver, Wait
from selenium.webdriver.common.keys import Keys
from playwright.sync_api import sync_playwright
import pyautogui

# Define the Yahoo credentials
YAHOO_EMAIL = "XXXX@yahoo.com"
YAHOO_PASSWORD = "XYXYX@203916"

# Define the list of recipient email addresses
RECIPIENT_EMAILS = [
    "XXXX@yahoo.com",
    "XXXXe2009@gmail.com",
    "XXXX3@example.com",
    # Add more recipient email addresses as needed
]

# Subject
SUBJECT = "Yahoo Mail Automation Done"

# Message body
BODY = ""

# Proxy Settings
# proxy_settings = "http://62.171.141.103:6781"

# Function to simulate typing with a delay
def type_with_delay(element, text):
    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.01, 0.03))  # Adjust typing delay as needed

@browser(tiny_profile=True, 
  profile=YAHOO_EMAIL)  # Add proxy usage here
def yahoo_login_task(driver: Driver, data):
    # Step 1: Navigate to Yahoo Mail
    driver.get("https://mail.yahoo.com/d/onboarding")

    # Step 2: Check if the user is already logged in
    try:
        compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.SHORT)
        if compose_button:
            print("User is already logged in. Skipping login process and starting email composition.")
            start_composing_emails(driver)  # If logged in, start composing
            return
    except Exception:
        print("User is not logged in. Proceeding with login process...")

    # Step 3: Enter the email
    email_input = driver.wait_for_element("input[name='username']", wait=Wait.LONG)
    type_with_delay(email_input, YAHOO_EMAIL)
    driver.select("#login-signin").click()

    # Step 4: Wait for the password field and enter the password
    time.sleep(2)
    password_input = driver.wait_for_element("input[name='password']", wait=Wait.LONG)
    type_with_delay(password_input, YAHOO_PASSWORD)
    driver.select("#login-signin").click()

    # Step 5: Handle post-login prompts (if any)
    try:
        not_now_button = driver.get_element_with_exact_text("Not now", wait=Wait.LONG)
        not_now_button.click()
    except Exception:
        pass  # If "Not now" doesn't appear, proceed anyway

    # Step 6: Wait for the inbox to load by checking for a unique element
    try:
        inbox_element = driver.wait_for_element("a[title='Inbox']", wait=Wait.LONG)
        print("Inbox page has loaded.")
        start_composing_emails(driver)  # Now that we're logged in, start composing emails
    except Exception as e:
        print("Inbox did not load properly:", str(e))
        return  # Exit if inbox doesn't load

# Function to compose and send emails
def start_composing_emails(driver: Driver):
    for recipient in RECIPIENT_EMAILS:
        time.sleep(2)  # Ensure that the inbox is fully loaded
        
        # Step 7: Click the "Compose" button
        try:
            compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.LONG)
            compose_button.click()
        except Exception as e:
            print(f"Compose button not found for {recipient}: {str(e)}")
            continue  # Skip to the next recipient if the compose button is not found

        # Step 8: Add recipient email
        sender_input = driver.wait_for_element("input[id='message-to-field']", wait=Wait.LONG)
        type_with_delay(sender_input, recipient)

        # Step 9: Add the subject
        subject_input = driver.wait_for_element("input[data-test-id='compose-subject']", wait=Wait.LONG)
        type_with_delay(subject_input, SUBJECT)
        pyautogui.hotkey('tab')
        
        # Open a new tab using the Ctrl + T shortcut
        pyautogui.hotkey('ctrl', 't')
    
        # Navigate to the specific link
        pyautogui.typewrite('https://m.phx.co.in/a/mailer.html')
        pyautogui.press('enter')
        time.sleep(5)
        # Select all content on the page using Ctrl + A
        pyautogui.hotkey('ctrl', 'a')

        # Copy the selected content using Ctrl + C
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('ctrl', 'w')
        
        time.sleep(2)
        # Switch back to the original tab
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(2)
        pyautogui.hotkey('tab')
        time.sleep(2)
        # Step 10: Add the body
        # body_input = driver.wait_for_element("div[role='textbox']", wait=Wait.LONG)
        # type_with_delay(body_input, BODY)
        pyautogui.hotkey('ctrl',  'v')
        time.sleep(3)
        # Step 11: Click the "Send" button
        try:
                send_button = driver.get_element_with_exact_text("Send", wait=Wait.LONG)
                send_button.click()
                print(f"Email successfully sent to {recipient}.")
        except Exception as e:
                print(f"Send button not found for {recipient}: {str(e)}")

        # Optional: Delay between sending emails
        time.sleep(2)

# Execute the login task and send emails
yahoo_login_task(data=None)
