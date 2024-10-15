import time
import subprocess
import random
import requests
from datetime import datetime, timedelta
import json
import os
from botasaurus.browser import browser, Driver, Wait
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

# Function to check if session data exists for the given email
def is_session_saved(email):
    profile_dir = get_profile_directory(email)
    session_file = os.path.join(profile_dir, "session.json")  # Adjust this based on your session file location
    return os.path.exists(session_file)

# Function to create a unique tiny profile directory for each email account
def get_profile_directory(email):
    profile_dir = f"tiny_profiles/{email.replace('@', '_at_').replace('.', '_dot_')}"
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    return profile_dir

# Function to load Yahoo accounts from a JSON file
def load_yahoo_accounts(filename="email_accounts.json"):
    try:
        with open(filename, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print("Email accounts file not found. Please create 'email_accounts.json' with your accounts.")
        return []

# Main function to perform the Yahoo login and email sending task using tiny profiles
@browser(tiny_profile=True, profile= "email_accounts.json")     
def yahoo_login_task(driver: Driver, email, password):
    profile_dir = get_profile_directory(email)
    driver.set_profile_directory(profile_dir)  # Set the browser to use a specific tiny profile

    if is_session_saved(email):
        print(f"Session already exists for {email}. Skipping login process and using saved session.")
        driver.get("https://mail.yahoo.com/d/onboarding")
        time.sleep(10)
        start_composing_emails(driver)
        return

    # Proceed with login if session is not found
    driver.get("https://mail.yahoo.com/d/onboarding")
    time.sleep(10)

    try:
        compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.SHORT)
        if compose_button:
            print(f"User {email} is already logged in. Skipping login process and starting email composition.")
            start_composing_emails(driver)
            return
    except Exception:
        print(f"User {email} is not logged in. Proceeding with login process...")

    email_input = driver.wait_for_element("input[name='username']", wait=Wait.LONG)
    email_input.type(email)
    driver.select("#login-signin").click()

    time.sleep(10)
    password_input = driver.wait_for_element("input[name='password']", wait=Wait.LONG)
    password_input.type(password)
    driver.select("#login-signin").click()

    try:
        not_now_button = driver.get_element_with_exact_text("Not now", wait=Wait.LONG)
        not_now_button.click()
    except Exception:
        pass

    try:
        time.sleep(10)
        inbox_element = driver.wait_for_element("a[title='Inbox']", wait=Wait.LONG)
        print("Inbox page has loaded.")
        start_composing_emails(driver)
    except Exception as e:
        print("Inbox did not load properly:", str(e))

# Function to compose and send emails (placeholder function)
def start_composing_emails(driver: Driver):
    print("Composing and sending emails...")  # Your email sending logic goes here

# Load all Yahoo accounts from the JSON file
yahoo_accounts = load_yahoo_accounts()

# Loop through each account and perform login and email sending tasks
for account in yahoo_accounts:
    email = account['email']
    password = account['password']
    print(f"Starting email session for {email}...")

    # Call the yahoo_login_task function with the current email and password
    yahoo_login_task(driver=None, email=email, password=password)

    print("Waiting for 5 minutes before logging in to the next account...")
    time.sleep(300)
