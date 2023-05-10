from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select;
from datetime import datetime
from calendar_1 import create_event


def main():
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 60)

    browser.get("https://[hidden].kronos.net/wfc/navigator/logon")

    # Enter username
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'okta-signin-username')))
    username_field.send_keys("[username]")
    username_field.submit()

    # Wait for password input field to be visible and enter password
    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'input75')))
    password_field.send_keys("[password]")
    
    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button-primary')))
    login_button.click()

    # View reports
    myreports = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'My Reports')]")))
    myreports.click()
    
    # Switch to the iframe
    iframe = wait.until(EC.presence_of_element_located((By.ID, "widgetFrame2876")))
    browser.switch_to.frame(iframe)

    # Find the dropdown element
    dropdown_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'timeframesDDL')]")))

    # Interact with the dropdown
    dropdown_element.click()
    select = Select(dropdown_element)
    select.select_by_value("5")

    view_report = browser.find_element(By.ID, 'ViewReportButton')
    view_report.click()

    # Grab schedule table
    schedule = browser.find_element(By.XPATH, "/html/body/table[5]")
    rows = schedule.find_elements(By.TAG_NAME, "tr")

    # Extract Data

    current_day = None
    

# Loop through each row
    for row in rows:
        start_time = None
        end_time = None
        # Find all cells in the row
        cells = row.find_elements(By.TAG_NAME,'td')
        # Check if this row contains the date for a new day
        if len(cells) > 1 and cells[0].get_attribute("class") == "data" and cells[1].get_attribute("class") == "data":
            current_day = cells[0].text.strip()

        # Check if this row contains the start time of a shift
        if len(cells) > 4 and cells[4].text == "Regular":
            # Check if this is the first row of the shift
            if cells[1].get_attribute("class") == "data" and cells[8].text.isspace():
                start_time = cells[1].text.strip()
                print(f"{current_day}: {start_time}")
            # Check if this is the third row of the shift
            elif cells[8].text != "":
                end_time = cells[2].text.strip()
                print(f"{current_day}: {end_time}")

        # transform date data
            dt = datetime.strptime(f"{current_day} {datetime.now().year}", '%a %m/%d %Y')
            formatted_date = dt.isoformat()
        # transform start time data
        if start_time != None:
            shift_start = datetime.strptime(start_time, '%I:%M%p')
            formatted_start = datetime.combine(dt.date(), shift_start.time()).isoformat()
            print(formatted_start)
    # transform end time data
        if end_time != None:
            shift_end = datetime.strptime(end_time, '%I:%M%p')
            formatted_end = datetime.combine(dt.date(), shift_end.time()).isoformat()
            print(formatted_end)
            print('Creating Calendar Event...')
            create_event(formatted_start, formatted_end)
                    


    # Switch back to the default content
    browser.switch_to.default_content()





if __name__ == '__main__':
    main()