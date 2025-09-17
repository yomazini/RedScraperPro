# RedScraperPro Debugging Summary

This document outlines the problems encountered, the fixes applied, and the correct way to run and use the RedScraperPro application.

## 1. The Problem

The primary issue was a `ModuleNotFoundError` which prevented the application from starting. This was caused by a combination of factors:

*   **Incorrect Imports:** The Python source code used relative imports (e.g., `from utils.config import Config`). When a project is structured as an installable package (using `setup.py` and a `src` layout), all internal imports must be absolute from the package's root (e.g., `from redscraperpro.utils.config import Config`).
*   **Incorrect Execution Method:** The application was being run as a simple script. A packaged application must be run via its registered "entry points" to ensure the Python path is set up correctly.
*   **Secondary Errors:** While fixing the imports, a Python `IndentationError` was accidentally introduced, which also caused the application to crash.

## 2. The Fixes

A series of steps were taken to resolve all the issues:

1.  **Installed the Package:** The project was correctly installed as a Python package in "editable" mode. This registers the command-line entry points (`rsp` and `redscraperpro`) and makes the package available throughout the environment.
2.  **Corrected All Imports:** A project-wide search was conducted to find and fix all incorrect relative imports. All imports were updated to be absolute, referencing the `redscraperpro` package name. This was done in the following files:
    *   `src/redscraperpro/cli/interface.py`
    *   `src/redscraperpro/main.py`
    *   `src/redscraperpro/scraper/reddit_scraper.py`
3.  **Added Missing Imports:** Necessary imports for `PostScraper`, `CommentScraper`, and `UserScraper` were added to `src/redscraperpro/scraper/reddit_scraper.py`.
4.  **Fixed Indentation:** The `IndentationError` was corrected in `src/redscraperpro/cli/interface.py`.

## 3. How to Run the Application

Follow these steps to run the application correctly.

### Step 1: Installation
Ensure your Python virtual environment is activated. From the project root directory, run the installation command:

```bash
pip install -e .
```

This only needs to be done once.

### Step 2: First-Time Configuration
The first time you run the application, it will launch a configuration wizard to help you set up your Reddit API credentials.

Run the application with either of the following commands:

```bash
rsp
```

or

```bash
redscraperpro
```

Follow the on-screen instructions to enter your Client ID, Client Secret, and other details.

### Step 3: Normal Use
Once configured, you can run the application in two ways:

**A) Interactive Mode**
For a user-friendly, menu-driven experience, simply run the command without any arguments:

```bash
rsp
```

**B) Command-Line Mode**
For direct scraping, you can provide arguments to the command.

## 4. How to Use It (Command-Line Examples)

Here are a few examples of how to use the tool directly from the command line:

*   **Run the configuration wizard again:**
    ```bash
    rsp --setup
    ```

*   **Scrape posts by a keyword:**
    ```bash
    rsp --mode keyword --query "data science" --limit 50
    ```

*   **Scrape a specific subreddit and export to XLSX:**
    ```bash
    rsp --mode subreddit --target "learnpython" --limit 100 --export xlsx
    ```

*   **Scrape a user's profile:**
    ```bash
    rsp --mode user --target "some_username"
    ```

## 5. Additional Fixes

After the initial debugging, two more issues were identified and resolved.

*   **Progress Bar Crash:**
    *   **Problem:** The application would crash when starting a scrape, showing a `TypeError` related to an unexpected argument `spinner_style`.
    *   **Fix:** This was a dependency issue. The `rich` library had been updated and renamed the parameter. The fix was to change `spinner_style` to `style` in `src/redscraperpro/utils/progress.py`.

*   **Empty CSV and XLSX Exports:**
    *   **Problem:** The CSV and XLSX files were created, but the data sheets were empty. The CSV had the correct number of rows, but no data, and the XLSX was missing all post and comment data.
    *   **Fix:** The logic used to "flatten" the scraped data for the export was buggy. The recursive function was not correctly returning the data. This was fixed by correcting the logic in the `_flatten_data` and `_flatten_dict` functions inside both `src/redscraperpro/exporters/csv_exporter.py` and `src/redscraperpro/exporters/xlsx_exporter.py`.