
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Open Chrome
driver = webdriver.Chrome()

try:
    print("Starting Selenium dashboard test...")

    # Open the application
    driver.get("http://localhost:5173")

    # Wait for the page to load
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    # Check that the page body is visible
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed(), "Dashboard body is not visible"

    # Check that the page contains content
    page_text = body.text
    assert page_text.strip(), "Dashboard is empty"

    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)
    print("Dashboard content loaded successfully!")

    # Capture screenshot
    driver.save_screenshot(
        "selenium_tests/dashboard_initial.png"
    )
    print("Screenshot saved successfully!")

except Exception as e:
    print("TEST FAILED:", e)
    raise

finally:
    driver.quit()
    print("Chrome closed.")
