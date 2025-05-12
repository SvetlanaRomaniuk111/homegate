import requests
from bs4 import BeautifulSoup
from src.database import save_listing

# Change the URL if needed — check it manually in your browser.
URL = "https://www.homegate.ch/rent/real-estate/city-studen-sz/matching-list?be=5000"

def get_listings():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "Accept-Language": "de-CH,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.homegate.ch/"
    })

    response = session.get(URL)
    
    # Debug: Print status code and first 1000 characters of the response
    print(f"HTTP status code: {response.status_code}")
    print(response.text[:1000])
    
    if response.status_code != 200:
        print("Error: Unable to access the website. Check the URL and network connectivity.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    listings = []
    
    for item in soup.find_all("div", class_="ResultList_listItem_j5Td_"):
        price_elem = item.select_one("span.HgListingCard_price_JoPAs")
        rooms_elem = item.select_one("div.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq")
        address_elem = item.select_one("div.HgListingCard_address_JGiFv address")
        title_elem = item.select_one("p.HgListingDescription_title_NAAxy span")
        desc_elem = item.select_one("p.HgListingDescription_medium_NzKMY")

        listing_id = item.select_one("a")["href"].split("/")[-1] if item.select_one("a") else "No ID"

        data = {
            "listing_id": listing_id,
            "title": title_elem.text.strip() if title_elem else "Title missing",
            "price": price_elem.text.strip() if price_elem else "Price missing",
            "rooms": rooms_elem.text.strip() if rooms_elem else "Rooms missing",
            "address": address_elem.text.strip() if address_elem else "Address missing",
            "description": " ".join(desc_elem.text.strip().split()) if desc_elem else "Description missing",
        }

        save_listing(data)  # Save listing to database

    return listings

if __name__ == "__main__":
    get_listings()
    print("✅ Data collection and saving complete!")