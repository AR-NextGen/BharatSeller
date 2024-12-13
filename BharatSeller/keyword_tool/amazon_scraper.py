from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_reviews_selenium(product_url):
    # Configure Selenium WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-headless')  # Ensure visibility
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    print(f"URL being scraped: {product_url}")  # Debugging output
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(product_url)
        time.sleep(5)  # Allow page to load
        reviews = []

        while True:
            try:
                # Wait for the reviews to load
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review"]'))
                )
            except Exception as e:
                print(f"Error waiting for reviews to load: {e}")
                break
            
            # Parse reviews using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Detect CAPTCHA
            if "captcha" in soup.text.lower():
                print("CAPTCHA detected. Solve it manually in the browser.")
                break

            review_divs = soup.find_all('div', {'data-hook': 'review'})
            print(f"Current URL: {driver.current_url}")  # Debugging output
            print(f"Found {len(review_divs)} review divs")  # Debugging output
            
            # Extract review content
            for review in review_divs:
                try:
                    review_body = review.find('span', {'data-hook': 'review-body'})
                    if review_body:
                        review_text = review_body.text.strip()
                        reviews.append({'content': review_text})
                except Exception as e:
                    print(f"Error extracting review: {e}")
            
            # Attempt to click the "Next" button for pagination
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
                print(f"Found next button: {next_button}")  # Debugging output
                driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
            except Exception as e:
                print(f"Error clicking next button: {e}")
                break
    except Exception as e:
        print(f"Error initializing browser: {e}")
    finally:
        driver.quit()
        print(f"Fetched reviews on page: {reviews}")  # Debugging output
        return reviews

def get_all_reviews_selenium(product_url):
    reviews = []
    page = 1
    print(f"Input URL: {product_url}")  # Debugging output

    # Ensure URL is valid and does not duplicate "product-reviews"
    if "product-reviews/" not in product_url:
        print("Invalid product URL format. Ensure it includes 'product-reviews/'.")
        return []
    
    # Handle pagination without duplicating "pageNumber"
    base_url = product_url.split("&pageNumber=")[0]  # Remove existing pageNumber if any
    print(f"Base URL: {base_url}")  # Debugging output

    while True:
        url = f"{base_url}&pageNumber={page}"  # Append pagination parameter
        print(f"Constructed URL for scraping: {url}")

        new_reviews = get_reviews_selenium(url)
        if not new_reviews:
            break  # Stop if no reviews found
        reviews.extend(new_reviews)
        page += 1

    print(f"All fetched reviews: {len(reviews)}")
    return reviews