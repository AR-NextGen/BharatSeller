from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_reviews_selenium(product_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-headless')  # Run Chrome in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--proxy-server=http://your-proxy-server:port')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(product_url)
    time.sleep(5)  # Debugging delay
    reviews = []

    while True:
        try:
            # Wait for the reviews to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review"]'))
            )
        except Exception as e:
            print(f"Error waiting for reviews to load: {e}")
            break
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_divs = soup.find_all('div', {'data-hook': 'review'})
        print(driver.page_source)  # Add this line for debugging
        print(f"Current URL: {driver.current_url}")  # Add this line for debugging
        print(f"Found {len(review_divs)} review divs")  # Add this line for debugging
        
        for review in review_divs:
            review_body = review.find('span', {'data-hook': 'review-body'})
            if review_body:
                review_text = review_body.text.strip()
                reviews.append({'content': review_text})  # Ensure the review content is correctly formatted
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
            next_button.click()
            print(f"Next button found: {next_button}")  # Add this line for debugging
            driver.execute_script("arguments[0].click();", next_button)
            WebDriverWait(driver, 10).until(
                EC.staleness_of(next_button)
            )
        except Exception as e:
            print(f"Error clicking next button: {e}")
            break
        if "captcha" in driver.page_source.lower():
            input("CAPTCHA detected. Please solve it in the browser window and press Enter to continue...")
            print("CAPTCHA detected!")
    
    driver.quit()
    print(f"Fetched reviews on page: {reviews}")  # Add this line for debugging
    return reviews

def get_all_reviews_selenium(product_url):
    reviews = []
    page = 1
    while True:
        url = f"{product_url}?pageNumber={page}"  # Corrected URL format
        new_reviews = get_reviews_selenium(url)
        if not new_reviews:
            break
        reviews.extend(new_reviews)
        page += 1
    print(f"All fetched reviews: {reviews}")  # Add this line for debugging
    return reviews