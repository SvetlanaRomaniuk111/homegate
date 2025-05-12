from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

URL = "https://www.homegate.ch/rent/real-estate/city-studen-sz/matching-list?be=5000"

def get_listings_with_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Используем webdriver-manager для автоматической настройки chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(URL)
    
    driver.implicitly_wait(10)
    
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, "html.parser")
    
    listings = soup.find_all("div", class_="HgListingCard_info_RKrwz")
    for item in listings:
        title_elem = item.select_one("p.HgListingDescription_title_NAAxy")
        price_elem = item.select_one("span.HgListingCard_price_JoPAs")
        
        title = title_elem.text.strip() if title_elem else "Title missing"
        price = price_elem.text.strip() if price_elem else "Price missing"
        
        print(f"Title: {title}\nPrice: {price}\n")
    
if __name__ == "__main__":
    get_listings_with_selenium()