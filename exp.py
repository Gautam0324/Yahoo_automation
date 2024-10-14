import time
import subprocess
import requests
from botasaurus.browser import browser, Driver, Wait
from selenium.webdriver.common.keys import Keys
from playwright.sync_api import sync_playwright
import pyautogui

# Function to run ADB commands
def run_adb_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running ADB command: {e.stderr.decode('utf-8')}")
        return None

# Define the Yahoo credentials
YAHOO_EMAIL = "harishjain8764@yahoo.com"
YAHOO_PASSWORD = "@$%^Harish$$543"

# Define the list of recipient email addresses
RECIPIENT_EMAILS = [
    "sgautamsharma146@gmail.com",
    "sgautamsharma146@gmail.com",
    "sgautamsharma146@gmail.com"
    
]

# Subject
SUBJECT = " What can Robot's do? "

# Message body
BODY = "Essentially, there are as many different types of robots as there are tasks for them to perform. Robots can perform some tasks better than humans, but others are best left to people and not machines. Click this to read more  https://bitshrt.com/4Br"

@browser(tiny_profile=True, profile=YAHOO_EMAIL)
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
    email_input.type(YAHOO_EMAIL)
    driver.select("#login-signin").click()

    # Step 4: Wait for the password field and enter the password
    time.sleep(2)
    password_input = driver.wait_for_element("input[name='password']", wait=Wait.LONG)
    password_input.type(YAHOO_PASSWORD)
    driver.select("#login-signin").click()

    # Step 5: Handle post-login prompts (if any)
    try:
        not_now_button = driver.get_element_with_exact_text("Not now", wait=Wait.LONG)
        not_now_button.click()
    except Exception:
        pass  # If "Not now" doesn't appear, proceed anyway

    # Step 6: Wait for the inbox to load by checking for a unique element
    time.sleep(10)
    try:
        inbox_element = driver.wait_for_element("a[title='Inbox']", wait=Wait.LONG)
        print("Inbox page has loaded.")
        start_composing_emails(driver)  # Now that we're logged in, start composing emails
    except Exception as e:
        print("Inbox did not load properly:", str(e))
        return  # Exit if inbox doesn't load

# Function to compose and send emails
def start_composing_emails(driver: Driver):
    total_sent = 0  # Initialize a counter for sent emails
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
        sender_input.type(recipient)

        # Step 9: Add the subject
        subject_input = driver.wait_for_element("input[data-test-id='compose-subject']", wait=Wait.LONG)
        subject_input.type(SUBJECT)
        pyautogui.hotkey('tab')

        time.sleep(2)
        pyautogui.hotkey('tab')
        time.sleep(2)

        # Step 10: Add the body
        body_input = driver.wait_for_element("div[role='textbox']", wait=Wait.LONG)
        body_input.type(BODY)
        time.sleep(3)

        # Step 11: Click the "Send" button
        try:
            send_button = driver.get_element_with_exact_text("Send", wait=Wait.LONG)
            send_button.click()
            print(f"Email successfully sent to {recipient}.")
            total_sent += 1  # Increment the counter for each successfully sent email
        except Exception as e:
            print(f"Send button not found for {recipient}: {str(e)}")

    print(f"Total emails sent: {total_sent}")  # Print total count of sent emails

# Execute the login task and send emails
yahoo_login_task(data=None)
