import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging

# Configure logging to save logs into a file
logging.basicConfig(
    filename='selenium_page_source.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)

# List of User-Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

class ProductExplorerSpider(scrapy.Spider):
    name = "product_explorer"
    allowed_domains = ["amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=laptops"]

    def __init__(self, *args, **kwargs):
        super(ProductExplorerSpider, self).__init__(*args, **kwargs)

        # Random User-Agent
        user_agent = random.choice(USER_AGENTS)
        self.logger.info(f"Using User-Agent: {user_agent}")

        # Chrome Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-cache')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f"user-agent={user_agent}")

        # Initialize WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        # Remove "navigator.webdriver" property for headless browsers
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def parse(self, response):
        try:
            self.logger.info(f"Navigating to URL: {response.url}")
            self.driver.get(response.url)
            time.sleep(5)  # Allow the page to load completely
            self.logger.info("Page Source fetched by Selenium:\n%s", self.driver.page_source)

            sel = Selector(text=self.driver.page_source)

            # Scrape product details
            for product in sel.css('div.s-result-item'):
                title = product.css('h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span::text').get(default='N/A')
                price = product.css('span.a-price-whole::text').get(default='N/A')
                rating = product.css('i[data-cy="reviews-ratings-slot"] span.a-icon-alt::text').get(default='N/A')
                asin = product.attrib.get('data-asin', '').strip()
                product_link = response.urljoin(product.css('a.a-link-normal::attr(href)').get(default=''))

                self.logger.info(f"Scraped Product: Title={title}, Price={price}, Rating={rating}, ASIN={asin}")
                
                yield {
                    'Product': title.strip() if title else 'N/A',
                    'Price': price.strip() if price else 'N/A',
                    'Rating': rating.strip() if rating else 'N/A',
                    'Monthly Sales': '',  # Placeholder
                    'Monthly Revenue': '',  # Placeholder
                    'Shipping Size Tier': '',  # Placeholder
                    'BSR': '',  # Placeholder
                    'Details': product_link  # Using product link for Details column
                }
        # Check for the "Next" button and follow the link
            next_page = sel.css('a.s-pagination-next::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.logger.info(f"Following pagination to: {next_page_url}")
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                self.logger.info("No more pages to scrape.")
        except Exception as e:
            self.logger.error(f"Error during parsing: {e}")

    def closed(self, reason):
    # Log the reason for spider closure
        self.logger.info(f"Spider closed because: {reason}")
        self.logger.info("Closing Selenium WebDriver.")
        try:
            self.driver.quit()
            # Explicitly delete the temporary directory created by the undetected_chromedriver
            import shutil
            temp_profile_dir = self.driver.capabilities.get('chrome', {}).get('userDataDir')
            if temp_profile_dir:
                shutil.rmtree(temp_profile_dir, ignore_errors=True)
        except Exception as e:
            self.logger.error(f"Error while closing WebDriver: {e}")