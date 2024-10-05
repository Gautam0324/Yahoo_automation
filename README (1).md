# Selenium Script Usage Instructions

## Prerequisites

- **Python 3.x** installed on your system.
- **Google Chrome** browser installed. (Modify the script if using a different browser)
- **Chrome WebDriver** compatible with your Chrome version.

## Setup Instructions

1. **Clone or download this repository** to your local machine.

2. **Install the required Python packages** using pip:

   ```bash
   pip install -r requirements.txt
   pip install pandas
   ```

3. **Download the appropriate Chrome WebDriver** from:
   [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

   - Ensure the WebDriver version matches your installed Chrome browser version.
   - Place the WebDriver executable in a directory that's in your system's PATH or specify its location in the script.

4. \*\*Download adb driver
   [https://developer.android.com/studio/run/win-usb]
   - Place the adb driver executable in a directory that's in your system's PATH or specify its location in the script.

## Running the Script

1. **Open a terminal/command prompt** in the directory containing the `selenium_script.py`.

2. **Run the script** using Python:
   ```bash
   python selenium_script.py
   ```

## Notes

- Modify the script as needed for different browsers or additional functionality.
- Ensure all XPaths and inputs provided are correct and correspond to elements on the target webpage.
- Handle exceptions and errors as needed for more robust automation.

## References

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Selenium Python Bindings Documentation](https://selenium-python.readthedocs.io/)
- [Requests Library Documentation](https://docs.python-requests.org/en/latest/)



