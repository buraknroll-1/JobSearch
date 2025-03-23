import requests
from requests.exceptions import RequestException
from playwright.sync_api import sync_playwright
import time
import certifi
import re

URL_FILE = "career_urls.txt"
HTML_FILE = "search_results.html"

# ANSI color codes for terminal
WHITE = "\033[97m"
GREEN = "\033[32m"
RED = "\033[31m"
GRAY = "\033[90m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

def load_urls():
    try:
        with open(URL_FILE, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
            return [(line.split(":", 1)[0], line.split(":", 1)[1]) for line in lines]
    except FileNotFoundError:
        return []

def save_urls(url_pairs):
    with open(URL_FILE, "w") as file:
        for company, url in url_pairs:
            file.write(f"{company}:{url}\n")

def scrape_for_keyword(company, url, keyword, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=certifi.where())
            response.raise_for_status()
            page_text = response.text.lower()
            if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", page_text):
                terminal_result = f"{WHITE}{company}{RESET} - {GREEN}{keyword} found{RESET}: {GRAY}{UNDERLINE}{url}{RESET}"
                html_result = f'<li><span style="color: white">{company}</span> - <span style="color: green">{keyword} found</span>: <a href="{url}" style="color: gray">{url}</a></li>'
                return terminal_result, html_result
            break
        except RequestException:
            if attempt == retries - 1:
                pass
        time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.set_extra_http_headers(headers)
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(10000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page_text = page.content().lower()
            if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", page_text):
                terminal_result = f"{WHITE}{company}{RESET} - {GREEN}{keyword} found{RESET}: {GRAY}{UNDERLINE}{url}{RESET}"
                html_result = f'<li><span style="color: white">{company}</span> - <span style="color: green">{keyword} found</span>: <a href="{url}" style="color: gray">{url}</a></li>'
            else:
                terminal_result = f"{WHITE}{company}{RESET} - {RED}{keyword} not found{RESET}: {GRAY}{UNDERLINE}{url}{RESET}"
                html_result = f'<li><span style="color: white">{company}</span> - <span style="color: red">{keyword} not found</span>: <a href="{url}" style="color: gray">{url}</a></li>'
            return terminal_result, html_result
        except Exception as e:
            terminal_result = f"{WHITE}{company}{RESET} - error fetching: {GRAY}{UNDERLINE}{url}{RESET} ({e})"
            html_result = f'<li><span style="color: white">{company}</span> - error fetching: <a href="{url}" style="color: gray">{url}</a> ({e})</li>'
            return terminal_result, html_result
        finally:
            browser.close()

def manage_urls():
    url_pairs = load_urls()
    print("Current URLs:")
    for company, url in url_pairs:
        print(f"{company}: {url}")
    print("1. Add a URL")
    print("2. Remove a URL")
    print("3. Done")
    choice = input("What do you want to do? ")

    if choice == "1":
        company = input("Enter the company name: ")
        url = input("Enter the URL: ")
        url_pairs.append((company, url))
        save_urls(url_pairs)
        print("URL added!")
    elif choice == "2":
        company_to_remove = input("Enter the company name to remove: ")
        url_to_remove = input("Enter the URL to remove: ")
        pair_to_remove = (company_to_remove, url_to_remove)
        if pair_to_remove in url_pairs:
            url_pairs.remove(pair_to_remove)
            save_urls(url_pairs)
            print("URL removed!")
        else:
            print("Company-URL pair not found.")
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
            url_pairs = load_urls()
            if not url_pairs:
                print("No URLs added yet. Add some in 'Manage URLs' first!")
            else:
                keyword = input("Enter keyword to search (e.g., manager): ")
                html_lines = [
                    "<html><body style='background: #1e1e1e; color: #ccc;'>",
                    "<h1>Search Results</h1><ul>"
                ]
                for company, url in url_pairs:
                    terminal_result, html_result = scrape_for_keyword(company, url, keyword)
                    print(terminal_result)
                    html_lines.append(html_result)
                html_lines.append("</ul></body></html>")
                with open(HTML_FILE, "w") as f:
                    f.write("\n".join(html_lines))
                print(f"Results saved to {HTML_FILE}")
        elif action == "2":
            manage_urls()
        elif action == "3":
            print("Exiting program. Bye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
