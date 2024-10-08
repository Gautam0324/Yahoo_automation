import time
import subprocess
import requests
import random 
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


# Function to get the current IP address
def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json().get('ip')
    except requests.RequestException as e:
        print(f"Error fetching current IP: {e}")
        return None
    
# Function to change the IP address by toggling flight mode
def change_ip():
    try:
        print('Enabling flight mode...')
        run_adb_command('adb shell cmd connectivity airplane-mode enable')
        print('Waiting for 10 seconds...')
        time.sleep(10)
        
        print('Disabling flight mode...')
        run_adb_command('adb shell cmd connectivity airplane-mode disable')
        print('Waiting for 20 seconds...')
        time.sleep(20)  # Increase this wait time to allow the network to stabilize
        
        print('Waiting for IP to change...')
        time.sleep(10)

        
        new_ip = get_current_ip()
        
        if new_ip:
            print(f"New IP: {new_ip}")
        else:
            print("New IP not found!")

        return new_ip
    except Exception as error:
        print('Error during IP change:', error)
        return None

def is_ip_used(ip, filename='yahoo.txt'):
    
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            used_ips = file.read().splitlines()
            
            # Loop through each line in the file
            for entry in used_ips:
                # Split the IP and the date (if present) and compare only the IP part
                stored_ip = entry.split(' - ')[0].strip()  # Extract the IP part and remove extra spaces
                if stored_ip == ip:
                    return True  # IP is already used
            return False  # IP not found in the file
    except FileNotFoundError:
        # If the file doesn't exist, consider that no IP has been used yet
        return False
    

# Define the Yahoo credentials
YAHOO_EMAIL = "XXX@yahoo.com"
YAHOO_PASSWORD = "XXX@203916"

# Define the list of recipient email addresses
RECIPIENT_EMAILS = [
    "anur92833@yahoo.com",
    "pasisalive2009@gmail.com",
    "recipient3@example.com",
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

@browser(tiny_profile= True,
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

    # Step 6: Wait
    # for the inbox to load by checking for a unique element
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
    for recipient in RECIPIENT_EMAILS:
        new_ip = change_ip()
        if new_ip and not is_ip_used(new_ip):
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
        else:
            print(f"Recipient {recipient} not found in the contacts list.")

# Execute the login task and send emails
yahoo_login_task(data=None)
