import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json


def init_driver():
    """
    Initialize the Selenium WebDriver using Selenium Manager for automatic ChromeDriver management.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Required for Linux environments
    options.add_argument("--window-size=1920,1080")  # Set window size

    return webdriver.Chrome(service=Service(), options=options)


def scrape_reddit(driver, query, pages=1):
    """
    Scrape Reddit for posts related to a specific query.

    Args:
        driver: Selenium WebDriver instance.
        query: Search term (e.g., "GOKU").
        pages: Number of pages to scrape.

    Returns:
        List of dictionaries containing scraped data.
    """
    base_url = "https://www.reddit.com/search/?q="
    driver.get(base_url + query)
    time.sleep(3)  # Wait for the page to load

    scraped_data = []

    for page in range(pages):
        # Scroll down to load more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for more content to load

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        posts = soup.find_all("div", {"data-testid": "post-container"})

        for post in posts:
            title_elem = post.find("h3")
            if title_elem:
                title = title_elem.get_text()
                if "goku" in title.lower():  # Check for "goku" in any case
                    link_elem = post.find("a", href=True)
                    link = link_elem["href"] if link_elem else "No link"
                    scraped_data.append(
                        {"title": title, "link": f"https://www.reddit.com{link}"}
                    )

    return scraped_data


def save_to_file(data, filename="output/reddit_posts.json"):
    """
    Save scraped data to a JSON file.

    Args:
        data: List of dictionaries containing scraped data.
        filename: Path to the output file.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    # Initialize the driver
    print("Initializing driver...")
    driver = init_driver()

    try:
        # Scrape Reddit for posts mentioning "GOKU"
        print("Scraping Reddit...")
        results = scrape_reddit(driver, query="ru", pages=2)

        # Save results to a file
        save_to_file(results)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Quit the driver
        driver.quit()
