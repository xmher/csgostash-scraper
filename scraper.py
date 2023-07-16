import re
import requests
from bs4 import BeautifulSoup

class ScraperException(Exception):
    """Base exception class for the scraper"""
    pass

class ItemHasNoDescription(ScraperException):
    """Exception that is thrown if the item has no description"""
    pass

class ItemHasNoLore(ScraperException):
    """Exception that is thrown if the item has no lore"""
    pass

class ItemHasNoDateAdded(ScraperException):
    """Exception that is thrown if the item has no date_added"""
    pass

class ItemNoCollection(ScraperException):
    """Exception that is thrown if the item does not belong in a collection"""
    pass

class ItemHasNoWear(ScraperException):
    """Exception that is thrown if the item does have wear"""
    pass

class ItemNoStattrakSouvenir(ScraperException):
    """Exception that is thrown if the item does not come in StatTrak or Souvenir"""
    pass

class PageNoPagination(ScraperException):
    """Exception that is thrown if a page does no have pagination"""
    pass

class PageHandler:
    @staticmethod
    def get_parsed_page(url: str):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    @staticmethod
    def get_item_frames(url: str, filtered_value: str):
        """Retrieves item frame contents"""
        page = PageHandler.get_parsed_page(url)
        item_frames = page.find_all("div", {"class": filtered_value})

        if not item_frames:
            # Try to get the item frames using a different class name
            item_frames = page.find_all("a", {"class": filtered_value})

        for item_frame in item_frames:
            yield item_frame

    @staticmethod
    def get_dropdown_items(filtered_value: str):
        """Retrieves dropdown menu item links that match the filter string"""
        page = PageHandler.get_parsed_page('https://csgostash.com/')
        dropdown_items = page.find_all("li", {"class": "dropdown"})

        for item in dropdown_items:
            if item.a.text == filtered_value:
                for link in item.find_all("a"):
                    if link.get('href') != '#':
                        yield link.get('href')

    @staticmethod
    def get_pagination(url: str):
        """Retrieves the pagination list"""

        def gen_url(url):
            yield url

        def gen_pagination(url):
            page = PageHandler.get_parsed_page(url)
            pagination_ul = page.find_all("ul", {"class": "pagination"})
            _ = []

            for item in pagination_ul:
                for a in item.find_all("a"):
                    href = a['href']
                    if href not in _:
                        yield a['href']
                    _.append(href)
                del _
                break

        yield from gen_url(url)
        yield from gen_pagination(url)

class RetrieveObject:
    """Abstract class for object data scraping"""
    def __init__(self, parsed_page):
        self.parsed_page = parsed_page

class RetrieveWeaponSkin(RetrieveObject):
    """Class for scraping data from weapon skin pages"""
    # This class will contain methods specific to weapon skins
    # ...
    
class RetrieveCollection(RetrieveObject):
    """Class for scraping data from collection pages"""
    # This class will contain methods specific to collections
    # ...

class RetrieveSticker(RetrieveObject):
    """Class for scraping data from sticker pages"""
    def __init__(self, parsed_page):
        super().__init__(parsed_page)

    @classmethod
    def _from_page_url(cls, url: str):
        page = PageHandler.get_parsed_page(url)
        return cls(page)

    @staticmethod
    def get_all_urls(url):
        """Generator that retrieves all sticker page urls"""
        item_frames = PageHandler.get_item_frames(url, 'details-link')

        for frame in item_frames:
            try:
                yield frame.a['href']
            except TypeError:
                continue

    def get_name(self):
        """Returns sticker name as string"""
        # Extract name from page
        name = self.parsed_page.find("h1").text.strip()
        return name

    def get_rarity(self):
        """Returns sticker rarity as string"""
        # Extract rarity from page
        rarity = self.parsed_page.find("div", {"class": "quality"}).text.strip()
        return rarity

    def get_prices(self):
        """Returns sticker prices and trading data as a dictionary"""
        # Extract prices and trading data from page
        prices_table = self.parsed_page.find("table", {"class": "table table-bordered table-condensed"})
        prices = {}
        for row in prices_table.find_all("tr")[1:]:
            data = row.find_all("td")
            key = data[0].text.strip()
            value = data[1].text.strip()
            prices[key] = value
        return prices
class RetrieveWeaponSkin(RetrieveObject):
    """Class for scraping data from weapon skin pages"""
    def __init__(self, parsed_page):
        super().__init__(parsed_page)

    @classmethod
    def _from_page_url(cls, url: str):
        page = PageHandler.get_parsed_page(url)
        return cls(page)

    @staticmethod
    def get_all_urls(url):
        """Generator that retrieves all weapon skin page urls"""
        item_frames = PageHandler.get_item_frames(url, 'details-link')

        for frame in item_frames:
            try:
                yield frame.a['href']
            except TypeError:
                continue

    def get_name(self):
        """Returns weapon skin name as string"""
        # Extract name from page
        name = self.parsed_page.find("h1").text.strip()
        return name

    def get_rarity(self):
        """Returns weapon skin rarity as string"""
        # Extract rarity from page
        rarity = self.parsed_page.find("div", {"class": "quality"}).text.strip()
        return rarity

    def get_prices(self):
        """Returns weapon skin prices and trading data as a dictionary"""
        # Extract prices and trading data from page
        prices_table = self.parsed_page.find("table", {"class": "table table-bordered table-condensed"})
        prices = {}
        for row in prices_table.find_all("tr")[1:]:
            data = row.find_all("td")
            key = data[0].text.strip()
            value = data[1].text.strip()
            prices[key] = value
        return prices


class RetrieveCollection(RetrieveObject):
    """Class for scraping data from collection pages"""
    def __init__(self, parsed_page):
        super().__init__(parsed_page)

    @classmethod
    def _from_page_url(cls, url: str):
        page = PageHandler.get_parsed_page(url)
        return cls(page)

    @staticmethod
    def get_all_urls(url):
        """Generator that retrieves all collection page urls"""
        item_frames = PageHandler.get_item_frames(url, 'details-link')

        for frame in item_frames:
            try:
                yield frame.a['href']
            except TypeError:
                continue

    def get_name(self):
        """Returns collection name as string"""
        # Extract name from page
        name = self.parsed_page.find("h1").text.strip()
        return name

    def get_items(self):
        """Returns items in the collection as a list"""
        # Extract items from page
        items_table = self.parsed_page.find("table", {"class": "table table-bordered table-condensed"})
        items = []
        for row in items_table.find_all("tr")[1:]:
            data = row.find_all("td")
            items.append(data[0].text.strip())
        return items
def scrape_all_data():
    base_url = 'https://csgostash.com/'

    # Get all weapon skin pages
    weapon_skin_urls = RetrieveWeaponSkin.get_all_urls(base_url + 'weapon')
    for url in weapon_skin_urls:
        weapon_skin = RetrieveWeaponSkin._from_page_url(url)
        print("Scraping Weapon Skin:", weapon_skin.get_name())
        print("Rarity:", weapon_skin.get_rarity())
        print("Prices:", weapon_skin.get_prices())
        print('\n' + '-' * 50 + '\n')

    # Get all collection pages
    collection_urls = RetrieveCollection.get_all_urls(base_url + 'collection')
    for url in collection_urls:
        collection = RetrieveCollection._from_page_url(url)
        print("Scraping Collection:", collection.get_name())
        print("Items:", collection.get_items())
        print('\n' + '-' * 50 + '\n')

    # Get all sticker pages
    sticker_urls = RetrieveSticker.get_all_urls(base_url + 'sticker')
    for url in sticker_urls:
        sticker = RetrieveSticker._from_page_url(url)
        print("Scraping Sticker:", sticker.get_name())
        print("Rarity:", sticker.get_rarity())
        print("Prices:", sticker.get_prices())
        print('\n' + '-' * 50 + '\n')

def scrape_souvenir_package(url):
    """Scrapes data from a single souvenir package page"""
    try:
        souvenir_package = RetrieveSouvenirPackage._from_page_url(url)
        print("Scraping Souvenir Package:", souvenir_package.get_title())
        print("Image URL:", souvenir_package.get_image_url())
        print("Collection URL:", souvenir_package.get_collection_url())
        print("Collection Name:", souvenir_package.get_collection_name())
        print("Contents:", souvenir_package.get_souvenir_contents())
        print()
    except Exception as e:
        print(f"Failed to scrape Souvenir Package at URL: {url} due to {str(e)}")   

def scrape_all_souvenir_packages():
    """Scrapes data from all souvenir package pages"""
    souvenir_package_urls = RetrieveSouvenirPackage.get_all_urls()
    for url in souvenir_package_urls:
        print(f'Scraping Souvenir Package at URL: {url}')
        try:
            scrape_souvenir_package(url)
        except Exception as e:
            print(f'Failed to scrape Souvenir Package at URL: {url} due to {e}')

        print('\n' + '-' * 50 + '\n')

def scrape_sticker(url):
    """Scrapes data from a single sticker page"""
    try:
        sticker = RetrieveSticker._from_page_url(url)
        print("Scraping Sticker:", sticker.get_name())
        print("Rarity:", sticker.get_rarity())
        print("Prices:", sticker.get_prices())
        print()
    except Exception as e:
        print(f"Failed to scrape Sticker at URL: {url} due to {str(e)}")   

def scrape_all_stickers():
    """Scrapes data from all sticker pages"""
    sticker_urls = RetrieveSticker.get_all_urls()
    for url in sticker_urls:
        print(f'Scraping Sticker at URL: {url}')
        try:
            scrape_sticker(url)
        except Exception as e:
            print(f'Failed to scrape Sticker at URL: {url} due to {e}')

        print('\n' + '-' * 50 + '\n')

def scrape_all_data():
    """Scrapes data from all pages"""
    print("Starting to scrape all data...")
    scrape_all_weapon_skins()
    scrape_all_collections()
    scrape_all_souvenir_packages()
    scrape_all_stickers()
    print("Finished scraping all data.")

if __name__ == "__main__":
    scrape_all_data()
