import time
import subprocess
import random
import requests
from datetime import datetime, timedelta
from botasaurus.browser import browser, Driver, Wait
import pyautogui
import os
import json

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
        time.sleep(20)
        
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
            for entry in used_ips:
                stored_ip = entry.split(' - ')[0].strip()
                if stored_ip == ip:
                    return True
            return False
    except FileNotFoundError:
        return False

# Save Yahoo credentials in a JSON file
def save_yahoo_credentials(email, password, filename="yahoo_account_details.json"):
    yahoo_account = {
        "email": email,
        "password": password
    }
    with open(filename, "w") as json_file:
        json.dump(yahoo_account, json_file, indent=4)
    print(f"Yahoo account details saved in {filename}")

# Save recipient emails in a JSON file
def save_recipient_emails(recipients, filename="recipient_emails.json"):
    data = {
        "recipients": recipients
    }
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Recipient emails saved in {filename}")

# Define the Yahoo credentials
YAHOO_EMAIL = "ojhanaman78911@yahoo.com"
YAHOO_PASSWORD = "@$%Naman667$543"

# Define the list of recipient email addresses
RECIPIENT_EMAILS = [
    "paisalive2009@gmail.com",
    "gautamsharma@phx.co.in",
    "sgautamsharma146@gmail.com",
    "harishjain8764@yahoo.com",
    "ankitasha98@gmail.com",
    "dubbabatliwala@gmail.com",
    "internalwarmup7@gmail.com",
    "jaadhavravi76@gmail.com",
    "jaanibuk1305@gmail.com",
    "jagdishraje89@gmail.com",
    "jaleela287@gmail.com",
    "janardanbuk1305@gmail.com",
]

# Subject
SUBJECT = "What can Robot's do?"

# Message body
BODY = "Essentially, there are as many different types of robots as there are tasks for them to perform. Robots can perform some tasks better than humans, but others are best left to people and not machines. Click this to read more  https://bitshrt.com/4Br"

# File to save sent email addresses
SENT_EMAILS_FILE = "sent_emails.txt"
# File to store the last reset time
LAST_RESET_FILE = "last_reset.txt"

# Function to load sent emails
def load_sent_emails():
    try:
        with open(SENT_EMAILS_FILE, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

# Function to load the last reset time
def load_last_reset_time():
    try:
        with open(LAST_RESET_FILE, "r") as file:
            last_reset_str = file.read().strip()
            return datetime.strptime(last_reset_str, "%Y-%m-%d %H:%M:%S")
    except (FileNotFoundError, ValueError):
        return None

# Function to save the last reset time
def save_last_reset_time():
    with open(LAST_RESET_FILE, "w") as file:
        file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Reset sent emails if needed
def reset_sent_emails_if_needed():
    last_reset_time = load_last_reset_time()
    now = datetime.now()

    if last_reset_time is None or now - last_reset_time >= timedelta(hours=24):
        with open(SENT_EMAILS_FILE, "w") as file:
            file.write("")
        print("24 hours have passed. sent_emails.txt has been reset.")
        save_last_reset_time()
    else:
        print("Less than 24 hours since the last reset. No reset needed.")

@browser(tiny_profile=True, profile=YAHOO_EMAIL)
def yahoo_login_task(driver: Driver, data):
    driver.get("https://mail.yahoo.com/d/onboarding")

    time.sleep(40)
    try:
        compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.SHORT)
        if compose_button:
            print("User is already logged in. Skipping login process and starting email composition.")
            start_composing_emails(driver)
            return
    except Exception:
        print("User is not logged in. Proceeding with login process...")

    new_ip = change_ip()
    if new_ip and not is_ip_used(new_ip):
        email_input = driver.wait_for_element("input[name='username']", wait=Wait.LONG)
        email_input.type(YAHOO_EMAIL)
        driver.select("#login-signin").click()

        time.sleep(10)
        password_input = driver.wait_for_element("input[name='password']", wait=Wait.LONG)
        password_input.type(YAHOO_PASSWORD)
        driver.select("#login-signin").click()

    try:
        not_now_button = driver.get_element_with_exact_text("Not now", wait=Wait.LONG)
        not_now_button.click()
    except Exception:
        pass

    try:
        time.sleep(40)
        inbox_element = driver.wait_for_element("a[title='Inbox']", wait=Wait.LONG)
        print("Inbox page has loaded.")
        start_composing_emails(driver)
    except Exception as e:
        print("Inbox did not load properly:", str(e))
        return

# Function to compose and send emails
def start_composing_emails(driver: Driver):
    sent_emails = load_sent_emails()
    total_recipients = len(RECIPIENT_EMAILS)
    current_index = 0
    limit = random.randint(3, 4)
    sent_count = 0

    while current_index < total_recipients and sent_count < limit:
        recipient = RECIPIENT_EMAILS[current_index]

        if recipient in sent_emails:
            current_index += 1
            continue

        time.sleep(2)
        try:
            compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.LONG)
            compose_button.click()
        except Exception as e:
            print(f"Compose button not found for {recipient}: {str(e)}")
            current_index += 1
            continue

        sender_input = driver.wait_for_element("input[id='message-to-field']", wait=Wait.LONG)
        sender_input.type(recipient)

        subject_input = driver.wait_for_element("input[data-test-id='compose-subject']", wait=Wait.LONG)
        subject_input.type(SUBJECT)
        pyautogui.hotkey('tab')

        time.sleep(2)
        pyautogui.hotkey('tab')
        time.sleep(2)

        body_input = driver.wait_for_element("div[role='textbox']", wait=Wait.LONG)
        body_input.type(BODY)
        time.sleep(3)

        try:
            send_button = driver.get_element_with_exact_text("Send", wait=Wait.LONG)
            send_button.click()
            time.sleep(10)
            sending_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Email successfully sent to {recipient} at {sending_time}.")
            sent_emails.add(recipient)
            sent_count += 1

            with open(SENT_EMAILS_FILE, "a") as file:
                file.write(f"{recipient}\n")

            current_index += 1
        except Exception as e:
            print(f"Send button not found for {recipient}: {str(e)}")

        random_delay = random.randint(30, 40)
        countdown_timer(random_delay)
        time.sleep(random_delay)

    try:
        profile_icon = driver.get_element_with_exact_text("Account", wait=Wait.LONG)
        profile_icon.click()
        time.sleep(1)
        sign_out_button = driver.get_element_with_exact_text("Sign out", wait=Wait.LONG)
        sign_out_button.click()
        print("Logged out successfully.")
    except Exception as e:
        print("Logout failed:", str(e))

def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"{remaining} seconds remaining...", end="\r")
        time.sleep(1)

# Reset the sent_emails.txt if more than 24 hours have passed
reset_sent_emails_if_needed()

while True:
    yahoo_login_task(data=None)
    print("Waiting for 5 minutes before repeating the process...")
    countdown_timer(300)

# Example usage to save credentials and recipient emails in JSON
save_yahoo_credentials(YAHOO_EMAIL, YAHOO_PASSWORD)
save_recipient_emails(RECIPIENT_EMAILS)
