from scrapy.http import HtmlResponse
import undetected_chromedriver as uc

class SeleniumMiddleware:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # Headless mode
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize the undetected Chrome driver
        self.driver = uc.Chrome(options=options)

    def process_request(self, request, spider):
        if not request.url.startswith('http'):
            return None
        
        self.driver.get(request.url)
        body = self.driver.page_source
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def __del__(self):
        self.driver.quit()
