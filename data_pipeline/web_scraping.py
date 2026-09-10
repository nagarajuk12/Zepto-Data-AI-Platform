"""
Script to scrape books data from books.toscrape.com
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

# Base configuration
BASE_URL = "http://books.toscrape.com/"

def get_categories(soup):
    """Extracts category names and their absolute URLs from the sidebar."""
    categories = []
    sidebar = soup.find("div", class_="side_categories")
    if sidebar:
        data = sidebar.find("ul").find("ul").find_all("a")
        for category in data:
            name = category.text.strip()
            link = urljoin(BASE_URL, category["href"])
            categories.append((name, link))

    if categories:
        return categories[:3]
    else:
        return []

def scrape_books():
    """scrape all books listed across least 3 different book categories"""
    try:
        print("Connecting to books.toscrape.com...")
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raise error for bad status codes
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        categories = get_categories(soup)
        print("Scraping categories...")
        # Select the first 3 categories
        target_categories = categories[:3]
        print(f"Targeting categories: {[c[0] for c in target_categories]}")
        books_data = []
        for cat_name, cat_url in target_categories:
            current_url = cat_url
            print(f"Scraping category: {cat_name}")
            while current_url:
                res = requests.get(current_url)
                if res.status_code != 200:
                    break
                cat_soup = BeautifulSoup(res.text, "html.parser")
                products = cat_soup.find_all("article", class_="product_pod")
                for product in products:
                    # 1. Title
                    title = product.find("h3").find("a")["title"]

                    # 2. Price (GBP)
                    price = product.find("p", class_="price_color").text.strip()
                    price_gbp = price.replace("Â", "")

                    # 3. Star Rating (Extract text like "Three" from class list)
                    star_classes = product.find("p", class_="star-rating")["class"]
                    star_rating = star_classes[1] if len(star_classes) > 1 else "Unknown"

                    # 4. Availability
                    availability = product.find("p", class_="availability").text.strip()
                    in_stock = "In stock" in availability
                    books_data.append({
                        "title": title,
                        "price_gbp": price_gbp,
                        "rating": star_rating,
                        "availability": availability,
                        "category": cat_name,
                        'in_stock': in_stock
                    })

                # Handle pagination within the category
                next_btn = cat_soup.find("li", class_="next")
                if next_btn:
                    next_href = next_btn.find("a")["href"]
                    current_url = urljoin(current_url, next_href)
                else:
                    current_url = None

        return books_data
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except Exception as e:
        print(f"Parsing error: {e}")
        return []


def save_to_csv(data):
    """ Saves books data to a csv file """
    df = pd.DataFrame(data)
    output_file = Path(__file__).parent / "books_dataset.csv"
    df.to_csv(output_file, index=False)
    print(f"Saving data to {output_file}")
    print(f"Total books collected: {len(df)}")


if __name__ == '__main__':
    books = scrape_books()
    if len(books) <= 0:
        pass
    else:
        save_to_csv(books)
    print("Done!")
