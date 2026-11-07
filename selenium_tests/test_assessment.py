
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 25)

try:
    print("Starting Selenium assessment test...")

    # Open the platform
    driver.get("http://localhost:5173")

    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Enter a test region
    region_input = driver.find_element(
        By.XPATH, "//label[contains(., 'Region')]//input"
    )
    region_input.send_keys("TEST-SELENIUM-KERALA")

    # Select the hazard type
    hazard_select = driver.find_element(
        By.XPATH, "//label[contains(., 'Hazard Type')]//select"
    )
    Select(hazard_select).select_by_visible_text("Cyclone")

    print("Region and hazard selected.")

    # Submit the assessment
    submit_button = driver.find_element(
    By.XPATH, "//form[@class='assessment-form']//button[@type='submit']"
    )    
    submit_button.click()

    # Wait for the new assessment to appear
    wait.until(
        lambda d: "TEST-SELENIUM-KERALA" in
        d.find_element(By.TAG_NAME, "body").text
    )

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert "TEST-SELENIUM-KERALA" in page_text
    assert "Cyclone" in page_text

    print("Assessment submitted successfully!")
    print("New region found on dashboard.")
    print("Hazard type verified: Cyclone")

    # Save screenshot
    driver.save_screenshot(
        "selenium_tests/assessment_result.png"
    )

    print("Screenshot saved: assessment_result.png")
    print("SELENIUM ASSESSMENT TEST PASSED!")

except Exception as e:
    print("TEST FAILED:", e)
    raise

finally:
    driver.quit()
    print("Chrome closed.")
