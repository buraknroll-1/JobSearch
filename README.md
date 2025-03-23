# URL Keyword Searcher

A Python tool to search career websites for specific keywords manually entered by the user (e.g., "manager") without opening a browser. It checks raw HTML first for speed, then uses headless rendering for JavaScript-heavy sites, delivering clean, simple results.

## Features
- **Dual-Mode Scraping**: Uses `requests` for static HTML and Playwright for JS-rendered content.
- **Headless Operation**: No browser windows—just terminal output.
- **Customizable URLs**: Add or remove sites via a text file.
- **Clean Output**: Shows only results (e.g., "Found 'manager' on [URL]") unless debug mode is enabled.
- **Secure**: Handles SSL with `certifi` for safe connections.

## Requirements
- Python 3.13+
- Libraries: `requests`, `playwright`, `certifi`
- Playwright’s Chromium (installed automatically)

## Installation
1. **Clone or Download**:
   - Save `url_searcher.py` and `career_urls.txt` to a folder (e.g., `~/Desktop/JobSearchCode`).

2. **Install Dependencies**:
   ```bash
   pip install requests playwright certifi
   playwright install
   ```

3. **Set Up URLs**:
   - Edit `career_urls.txt` with one URL per line, e.g.:
     ```
     https://www.metacareers.com/jobs/?sort_by_new=true
     ```

4. **(Optional) Fix SSL on macOS**:
   - Run:
     ```bash
     /Applications/Python\ 3.13/Install\ Certificates.command
     ```

## Usage
### Run as a Script
- Navigate to the folder:
  ```bash
  cd ~/Desktop/JobSearchCode
  ```
- Execute:
  ```bash
  python3 url_searcher.py
  ```
- Follow the menu:
  ```
  === URL Keyword Searcher ===
  1. Search URLs for a keyword
  2. Manage URLs
  3. Exit
  Choose an option:
  ```
- Option 1: Enter a keyword (e.g., "manager") to search all URLs.
- Option 2: Add/remove URLs in `career_urls.txt`.

### Compile to Executable
- Install PyInstaller:
  ```bash
  pip install pyinstaller
  ```
- Compile:
  ```bash
  pyinstaller --onefile url_searcher.py
  ```
- Run:
  ```bash
  ./dist/url_searcher
  ```
  - Note: First run may require `chmod +x dist/url_searcher` or right-click > Open.

### Example Output
```
Choose an option: 1
Enter keyword to search (e.g., manager): manager
Found 'manager' on https://www.metacareers.com/jobs/?sort_by_new=true
```

## Configuration
- **Debug Mode**: Edit `DEBUG = False` to `True` in the script to see raw and rendered HTML previews (200 chars each).
- **Timeouts**: Adjust `time.sleep(2)` or `page.wait_for_timeout(5000)` for slower sites.
- **Headers**: Modify `headers` in the script to tweak browser spoofing.

## Troubleshooting
- **SSL Errors**: Rerun the certificate command or check `certifi` installation.
- **Rendering Fails**: Increase `wait_for_timeout` to 10000 or add `page.wait_for_selector("a.p-link")` for Apex-like sites.
- **Large Executable**: Playwright’s Chromium (~150MB) bulks up the binary—normal behavior.

## License
This project is unlicensed—feel free to use, modify, or share it as you see fit!

## Credits
Built with grit, Python, and a dash of caffeine. Questions? Hit me up wherever you found this!

---

### Notes
- **Tone**: Practical and straightforward, with a hint of your clean-output vibe.
- **Structure**: Covers setup, use, and fixes—everything you’d need to pick it up later.
- **Compile Info**: Included since you asked about running it standalone.

Save this as `README.md` in your project folder. Want to tweak anything—like adding a section for your job search use case or changing the tone? Let me know! How’s it look?
