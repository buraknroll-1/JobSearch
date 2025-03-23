import requests
from requests.exceptions import RequestException
from playwright.sync_api import sync_playwright
import time
import certifi

URL_FILE = "career_urls.txt"
DEBUG = False  # Set to True for previews, False for clean output

def load_urls():
    try:
        with open(URL_FILE, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_urls(urls):
    with open(URL_FILE, "w") as file:
        for url in urls:
            file.write(url + "\n")

def scrape_for_keyword(url, keyword, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    # Try raw HTML first
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=certifi.where())
            response.raise_for_status()
            page_text = response.text.lower()
            if DEBUG:
                print(f"Raw preview for {url}: {page_text[:min(200, len(page_text))]}...")
            if keyword.lower() in page_text:
                return f"Found '{keyword}' on {url}"
            break
        except RequestException as e:
            print(f"Raw attempt {attempt + 1}/{retries} failed for {url}: {e}")
            if attempt == retries - 1:
                return f"Error fetching {url}: {e}"
        time.sleep(2)

    # Fallback to Playwright rendering
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.set_extra_http_headers(headers)
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            page_text = page.content().lower()
            if DEBUG:
                print(f"Rendered preview for {url}: {page_text[:min(200, len(page_text))]}...")
            if keyword.lower() in page_text:
                return f"Found '{keyword}' on {url}"
            return f"No '{keyword}' found on {url}"
        except Exception as e:
            return f"Error rendering {url}: {e}"
        finally:
            browser.close()

def manage_urls():
    urls = load_urls()
    print("Current URLs:", urls)
    print("1. Add a URL")
    print("2. Remove a URL")
    print("3. Done")
    choice = input("What do you want to do? ")

    if choice == "1":
        new_url = input("Enter the URL to add: ")
        urls.append(new_url)
        save_urls(urls)
        print("URL added!")
    elif choice == "2":
        url_to_remove = input("Enter the URL to remove: ")
        if url_to_remove in urls:
            urls.remove(url_to_remove)
            save_urls(urls)
            print("URL removed!")
        else:
            print("URL not found.")
    elif choice == "3":
        print("Returning to main menu.")
    else:
        print("Invalid choice.")

def main():
    while True:
        print("\n=== URL Keyword Searcher ===")
        print("1. Search URLs for a keyword")
        print("2. Manage URLs")
        print("3. Exit")
        action = input("Choose an option: ")

        if action == "1":
            urls = load_urls()
            if not urls:
                print("No URLs added yet. Add some in 'Manage URLs' first!")
            else:
                keyword = input("Enter keyword to search (e.g., manager): ")
                for url in urls:
                    result = scrape_for_keyword(url, keyword)
                    print(result)
        elif action == "2":
            manage_urls()
        elif action == "3":
            print("Exiting program. Bye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()