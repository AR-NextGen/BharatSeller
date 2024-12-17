from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random

def amazon_login(driver, username, password):
    """
    Automates login to Amazon using provided credentials.
    """
    try:
        print("Starting Amazon login...")

        # Navigate to Amazon's login page
        driver.get("https://www.amazon.in/ap/signin")

        # Enter email/phone number
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_field.send_keys(username)
        driver.find_element(By.ID, "continue").click()

        # Enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_field.send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()

        # Wait until login completes (check for the Amazon logo)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "nav-logo"))
        )
        print("Amazon login successful!")
    except Exception as e:
        print(f"Error during Amazon login: {e}")
        raise

def get_reviews_selenium(product_url, username, password):
    """
    Scrapes reviews from Amazon using Selenium, handling login and pagination.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-headless')  # Ensure visibility
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    reviews = []
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Log in to Amazon
        amazon_login(driver, username, password)

        # Navigate to the product reviews page
        driver.get(product_url)
        time.sleep(random.uniform(2, 5))

        while True:
            try:
                # Wait for reviews to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review"]'))
                )
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Detect CAPTCHA
                if "captcha" in soup.text.lower():
                    print("CAPTCHA detected. Solve it manually in the browser.")
                    break

                # Extract reviews
                review_divs = soup.find_all('div', {'data-hook': 'review'})
                for review in review_divs:
                    review_body = review.find('span', {'data-hook': 'review-body'})
                    if review_body:
                        reviews.append({'content': review_body.text.strip()})

                # Click the "Next" button for pagination
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
                    driver.execute_script("arguments[0].click();", next_button)
                    WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
                except Exception:
                    print("No more pages.")
                    break
            except Exception as e:
                print(f"Error scraping reviews: {e}")
                break
    finally:
        if 'driver' in locals():
            driver.quit()
        return reviews

def get_all_reviews_selenium(product_url, username, password):
    """
    Handles pagination to fetch all reviews from Amazon.
    """
    reviews = []
    page = 1
    print(f"Input URL: {product_url}")

    # Validate and construct the base URL for pagination
    if "product-reviews/" not in product_url:
        print("Invalid product URL format. Ensure it includes 'product-reviews/'.")
        return []

    base_url = product_url.split("&pageNumber=")[0]
    print(f"Base URL: {base_url}")

    while True:
        url = f"{base_url}&pageNumber={page}"
        print(f"Constructed URL for scraping: {url}")

        new_reviews = get_reviews_selenium(url, username, password)
        if not new_reviews:
            print("No new reviews found. Exiting loop.")
            break

        reviews.extend(new_reviews)
        page += 1

    print(f"All fetched reviews: {len(reviews)}")
    return reviews

if __name__ == "__main__":
    product_url = input("Enter the product reviews URL: ")
    username = input("Enter your Amazon email: ")
    password = input("Enter your Amazon password: ")

    all_reviews = get_all_reviews_selenium(product_url, username, password)
    print(f"Fetched {len(all_reviews)} reviews:")
    for review in all_reviews:
        print(review['content'])
