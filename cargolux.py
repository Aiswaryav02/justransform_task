from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
# initialize  web driver
driver = webdriver.Chrome()

try:
    # Navigate to the url
    driver.get("https://www.cargolux.com/track-and-Trace")
    time.sleep(3) 

    # accept cookies 
    driver.find_element(By.XPATH, '//button[@id="CybotCookiebotDialogBodyButtonAccept"]').click()
    time.sleep(2)


    # enter AWB reference  number and clicking search
    driver.find_element(By.XPATH, '//div[@class="track-and-trace__awb-label-list"]//input').send_keys("172-91811742")
    driver.find_element(By.XPATH, '//div[@class="track-and-trace__search"]//button[contains(text(),"Search")]').click()
    time.sleep(5)  

    # click button to view shipment tracking details
    driver.find_element(By.XPATH, '//div[@class="track-and-trace__details-trigger"]').click()
    time.sleep(3)


    # extract location names
    keys = []
    key_elements = driver.find_elements(By.XPATH, '//div[@class="track-and-trace__details-row"]//p')

    # Store each location name in the keys list
    for key in key_elements:
        text = key.text.strip()
        if text:
            keys.append(text)


    # Extract the tables containing the tracking details
    tables = driver.find_elements(By.XPATH, '//div[@class="track-and-trace__details-col"]//table')

    output_data = {}
    # iterate through the keys and tables, pairing each key with the corresponding table
    for key, table in zip(keys, tables):
        # extract table headers
        headers = [header.text.strip() for header in table.find_elements(By.XPATH, './/thead//th')]


        table_data = []
        # extract all rows from the table
        rows = table.find_elements(By.XPATH, './/tbody//tr')
        # Iterate through each row, extracting column values
        for row in rows:
            columns = row.find_elements(By.XPATH, './/td')
            if columns:  
                row_data = {headers[i]: columns[i].text.strip() for i in range(len(columns))}
                table_data.append(row_data)

        # Store data under the respective key
        output_data[key] = {"tracking_details": table_data}

    print(output_data)
    # Save the output data to a JSON file
    with open("cargolux_data.json", "w") as file:
        json.dump(output_data, file, indent=4)

    print("data has been saved to cargolux_data.json")
except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
