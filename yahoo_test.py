import time
import subprocess
import random
from datetime import datetime, timedelta
from botasaurus.browser import browser, Driver, Wait
import pyautogui
import os

# Define the Yahoo credentials
YAHOO_EMAIL = "harishjain8764@yahoo.com"
YAHOO_PASSWORD = "@$%^Harish$$543"

# Define the list of recipient email addresses
RECIPIENT_EMAILS = [
    "paisalive2009@gmail.com",
    "gautamsharma@phx.co.in",
    "sgautamsharma146@gmail.com",
    "harishjain8764@yahoo.com",
    "ankitasha98@gmail.com"
    # Add your other email addresses here...
]

# Subject
SUBJECT = "What can Robot's do?"

# Message body
BODY = "Essentially, there are as many different types of robots as there are tasks for them to perform. Robots can perform some tasks better than humans, but others are best left to people and not machines. Click this to read more  https://bitshrt.com/4Br"

# File to save sent email addresses
SENT_EMAILS_FILE = "sent_emails.txt"
# File to store the last reset time
LAST_RESET_FILE = "last_reset.txt"


# Function to run ADB commands
def run_adb_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running ADB command: {e.stderr.decode('utf-8')}")
        return None


def load_sent_emails():
    """Load sent emails from a file."""
    try:
        with open(SENT_EMAILS_FILE, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()


def load_last_reset_time():
    """Load the last reset time from a file."""
    try:
        with open(LAST_RESET_FILE, "r") as file:
            last_reset_str = file.read().strip()
            return datetime.strptime(last_reset_str, "%Y-%m-%d %H:%M:%S")
    except (FileNotFoundError, ValueError):
        return None


def save_last_reset_time():
    """Save the current time as the last reset time."""
    with open(LAST_RESET_FILE, "w") as file:
        file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def reset_sent_emails_if_needed():
    """Reset the sent_emails.txt file if 24 hours have passed since the last reset."""
    last_reset_time = load_last_reset_time()
    now = datetime.now()

    if last_reset_time is None or now - last_reset_time >= timedelta(hours=24):
        # If 24 hours have passed or it's the first run, clear the file and save the current time
        with open(SENT_EMAILS_FILE, "w") as file:
            file.write("")  # Clear the file
        print("24 hours have passed. sent_emails.txt has been reset.")
        save_last_reset_time()
    else:
        print("Less than 24 hours since the last reset. No reset needed.")


@browser(tiny_profile=True, profile=YAHOO_EMAIL)
def yahoo_login_task(driver: Driver, data):
    # Step 1: Navigate to Yahoo Mail
    driver.get("https://mail.yahoo.com/d/onboarding")

    # Step 2: Check if the user is already logged in
    try:
        compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.SHORT)
        if compose_button:
            print("User is already logged in. Skipping login process and starting email composition.")
            start_composing_emails(driver)
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
        start_composing_emails(driver)
    except Exception as e:
        print("Inbox did not load properly:", str(e))
        return


# Function to compose and send emails
def start_composing_emails(driver: Driver):
    sent_emails = load_sent_emails()  # Load already sent emails
    total_recipients = len(RECIPIENT_EMAILS)
    current_index = 0
    limit = 4  # Set limit for emails to be sent in one run
    sent_count = 0  # Counter for sent emails

    while current_index < total_recipients and sent_count < limit:
        recipient = RECIPIENT_EMAILS[current_index]

        if recipient in sent_emails:  # Skip already sent emails
            current_index += 1
            continue

        time.sleep(2)

        # Step 7: Click the "Compose" button
        try:
            compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.LONG)
            compose_button.click()
        except Exception as e:
            print(f"Compose button not found for {recipient}: {str(e)}")
            current_index += 1
            continue

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
            sending_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Email successfully sent to {recipient} at {sending_time}.")
            sent_emails.add(recipient)  # Add to the set of sent emails
            sent_count += 1  # Increment the sent counter

            # Append the recipient email to the file
            with open(SENT_EMAILS_FILE, "a") as file:
                file.write(f"{recipient}\n")

            current_index += 1
        except Exception as e:
            print(f"Send button not found for {recipient}: {str(e)}")

        # Add random delay between 30 and 90 seconds before sending the next email
        random_delay = random.randint(30, 90)
        countdown_timer(random_delay)  # Call the countdown timer
        time.sleep(random_delay)

    # Step 12: Logout process (if required)
    try:
        profile_icon = driver.get_element_with_exact_text("Account", wait=Wait.LONG)
        profile_icon.click()
        time.sleep(1)
        sign_out_button = driver.get_element_with_exact_text("Sign out", wait=Wait.LONG)
        sign_out_button.click()
        print("Logged out successfully.")
    except Exception as e:
        print("Error logging out:", str(e))


# Countdown Timer Function
def countdown_timer(seconds):
    """Display a countdown in seconds before sending the next email."""
    while seconds:
        mins, secs = divmod(seconds, 60)
        time_format = f'{mins:02}:{secs:02}'
        print(f"Next email in: {time_format}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("\nTime to send the next email!")


# Main program execution
if __name__ == "__main__":
    reset_sent_emails_if_needed()  # Reset the sent_emails.txt if necessary before starting
    while True:
        yahoo_login_task(data=None)
        print("Waiting for 2 minutes before repeating the process...")
        time.sleep(120)  # Wait for 2 minutes before starting again
