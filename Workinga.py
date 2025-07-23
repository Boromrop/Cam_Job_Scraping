import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os
from urllib.parse import urlparse
from selenium.common.exceptions import TimeoutException, WebDriverException

class ScraperConfig:
    CHROME_DRIVER_PATH = r"D:\DSE_Folder\Year_3\Sem_2\Web Scraping\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    OUTPUT_FILENAME = "New_Data_workinga.csv"
    START_ID =  10755
    END_ID = 11683
    BASE_URL = "https://workingna.com/job/{}"
    WAIT_TIMEOUT = 1
    DELAY = 0.1  # seconds between requests
    MAX_RETRIES = 2
    
    COLUMNS = [
        "Job Title", "Company Name", "Salary", "Available", "Office", 
        "Location", "Employment Type", "Closing Date", 
        "Job Responsibilities", "Job Requirements", "Link"
    ]

class JobScraper:
    def __init__(self, config):
        self.config = config
        self.driver = self._init_driver()
        self.scraped_count = 0
        self.skipped_count = 0
        self.error_count = 0
        
    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        service = Service(self.config.CHROME_DRIVER_PATH)
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def clean_text(self, text):
        if not text:
            return ""
        # Remove leading/trailing whitespace and normalize internal spaces
        text = ' '.join(text.strip().split())
        # Remove leading hyphens/dashes if present
        if text.startswith('-') or text.startswith('–'):
            text = text[1:].strip()
        return text
    
    def is_page_not_found(self, soup):
        """Check if the page shows 'not found' or similar error"""
        error_messages = [
            "not found", 
            "404", 
            "page doesn't exist", 
            "job not available",
            "no longer available"
        ]
        page_text = soup.get_text().lower()
        return any(msg in page_text for msg in error_messages)
    
    def is_empty_page(self, job_info):
        """Check if the page has no meaningful data"""
        required_fields = ["Job Title", "Company Name", "Job Responsibilities"]
        return all(job_info.get(field) in [None, "Not specified", ""] for field in required_fields)
    
    def extract_element(self, soup, find_params, next_element=None, attribute=None):
        try:
            element = soup.find(**find_params)
            if not element:
                return None
                
            if next_element:
                element = element.find_next(next_element)
                if not element:
                    return None
                    
            return element.get(attribute) if attribute else element.text
        except:
            return None
    
    def extract_ql_editor_content(self, soup, heading_text):
        """
        Extract content from a div with class="ql-editor" that contains multiple <p> tags
        Returns None if content is just placeholder text
        """
        try:
            # First find the heading
            heading = soup.find(lambda tag: tag.name and heading_text.lower() in tag.get_text().lower())
            if not heading:
                return None
            
            # Find the ql-editor div after the heading
            ql_editor = heading.find_next("div", class_="ql-editor")
            if not ql_editor:
                return None
            
            # Extract all <p> tags within the ql-editor
            paragraphs = ql_editor.find_all("p")
            if not paragraphs:
                return None
            
            # Clean each paragraph and filter out placeholders
            items = []
            for p in paragraphs:
                text = self.clean_text(p.get_text())
                if text and text.lower() not in ["job detail", "not specified"]:
                    items.append(text)
            
            if items:
                return " • ".join(items)
            
            return None
            
        except Exception as e:
            print(f"Error extracting ql-editor content for '{heading_text}': {str(e)}")
            return None
    
    def extract_section_content(self, soup, heading_text):
        """
        Extract content from a section with strict validation against placeholder text
        """
        # First try to get ql-editor content
        ql_content = self.extract_ql_editor_content(soup, heading_text)
        if ql_content:
            return ql_content
            
        # Then try to get multiple paragraphs
        try:
            heading = soup.find(lambda tag: tag.name and heading_text.lower() in tag.get_text().lower())
            if heading:
                paragraphs = []
                next_tag = heading.find_next_sibling()
                
                # Collect all consecutive <p> tags until we hit a different element type
                while next_tag and next_tag.name == 'p':
                    text = self.clean_text(next_tag.get_text())
                    if text and text.lower() not in ["job detail", "not specified"]:
                        paragraphs.append(text)
                    next_tag = next_tag.find_next_sibling()
                
                if paragraphs:
                    return " • ".join(paragraphs)
                
                # Try to find a <ul> list
                list_section = heading.find_next("ul")
                if list_section:
                    items = []
                    for li in list_section.find_all("li", recursive=False):
                        text = self.clean_text(li.text)
                        if text and text.lower() not in ["job detail", "not specified"]:
                            items.append(text)
                    
                    if items:
                        return " • ".join(items)
                
                # Try to find direct <p> tag after heading
                p_tag = heading.find_next("p")
                if p_tag:
                    text = self.clean_text(p_tag.text)
                    if text and text.lower() not in ["job detail", "not specified"]:
                        return text
        except Exception as e:
            print(f"Error extracting section '{heading_text}': {str(e)}")
        
        return "Not specified"
    
    def scrape_job_page(self, job_id):
        url = self.config.BASE_URL.format(job_id)
        
        for attempt in range(self.config.MAX_RETRIES + 1):
            try:
                self.driver.get(url)
                
                # Check for HTTP errors in the URL
                if "404" in self.driver.title or "Not Found" in self.driver.title:
                    return None
                
                # Wait for page to load or detect not found page
                try:
                    WebDriverWait(self.driver, self.config.WAIT_TIMEOUT).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "MuiBox-root"))
                    )
                except TimeoutException:
                    # Check if this is a "not found" page
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    if self.is_page_not_found(soup):
                        return None
                    raise
                
                time.sleep(self.config.DELAY)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                
                # Double check for not found page after load
                if self.is_page_not_found(soup):
                    return None
                
                job_info = {col: None for col in self.config.COLUMNS}
                
                # Extract all fields
                job_info["Job Title"] = self.clean_text(self.extract_element(soup, {"class_": "css-97a38i"}))
                job_info["Company Name"] = self.clean_text(self.extract_element(soup, {"class_": "css-aabkpg"}, "h6"))
                job_info["Office"] = self.clean_text(self.extract_element(soup, {"class_": "css-bnbs76"}, "p"))
                
                label_fields = {
                    "Location": "Location",
                    "Employment Type": "Employment",
                    "Closing Date": "Closing Date"
                }
                
                for field, label in label_fields.items():
                    job_info[field] = self.clean_text(self.extract_element(soup, {"string": label}, "p"))
                
                salary_tag = soup.find("span", class_="css-10bh2m3")
                if salary_tag:
                    job_info["Salary"] = self.clean_text(salary_tag.text)
                    available_text = salary_tag.find_next("span")
                    if available_text:
                        job_info["Available"] = self.clean_text(available_text.text)
                
                # Extract sections with strict validation
                responsibilities = self.extract_section_content(soup, "JOB RESPONSIBILITIES")
                requirements = self.extract_section_content(soup, "JOB REQUIREMENTS")
                
                # Additional validation to ensure we don't get placeholder text
                job_info["Job Responsibilities"] = responsibilities if responsibilities != "Job Detail" else "Not specified"
                job_info["Job Requirements"] = requirements if requirements != "Job Detail" else "Not specified"
                
                job_info["Link"] = url
                
                # Clean None values
                job_info = {k: v if v is not None else "Not specified" for k, v in job_info.items()}
                
                # Check if page has meaningful data
                if self.is_empty_page(job_info):
                    return None
                
                return job_info
                
            except TimeoutException:
                if attempt == self.config.MAX_RETRIES:
                    return None
                continue
                
            except WebDriverException as e:
                if attempt == self.config.MAX_RETRIES:
                    return None
                continue
                
            except Exception as e:
                if attempt == self.config.MAX_RETRIES:
                    return None
                continue
    
    def save_to_csv(self, data):
        file_exists = os.path.exists(self.config.OUTPUT_FILENAME)
        
        with open(self.config.OUTPUT_FILENAME, mode="a", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=self.config.COLUMNS)
            
            if not file_exists:
                writer.writeheader()
                
            writer.writerow(data)
    
    def run(self):
        print(f"🚀 Starting scraping from ID {self.config.START_ID} to {self.config.END_ID}")
        print(f"📁 Output will be saved to {self.config.OUTPUT_FILENAME}")
        print(f"⏳ Timeout set to {self.config.WAIT_TIMEOUT} seconds with {self.config.MAX_RETRIES} retries\n")
        
        for job_id in range(self.config.START_ID, self.config.END_ID + 1):
            print(f"🔍 Processing job ID {job_id}...", end=" ", flush=True)
            
            job_data = self.scrape_job_page(job_id)
            
            if job_data is not None:
                self.scraped_count += 1
                self.save_to_csv(job_data)
                print(f"✅ Success")
                print(f"   Title: {job_data['Job Title']}")
                print(f"   Company: {job_data['Company Name']}")
            else:
                self.skipped_count += 1
                print(f"⏩ Skipped (No data or error)")
            
            print()  # Add empty line between jobs
        
        print("\nScraping complete! Summary:")
        print(f"✅ Successful scrapes: {self.scraped_count}")
        print(f"⏩ Skipped jobs: {self.skipped_count}")
        print(f"💾 Data saved to {self.config.OUTPUT_FILENAME}")
        
        self.driver.quit()

if __name__ == "__main__":
    config = ScraperConfig()
    scraper = JobScraper(config)
    scraper.run()