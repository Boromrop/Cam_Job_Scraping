from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Path to your Chrome WebDriver (update as needed)
chrome_driver_path = r"D:\DSE_Folder\Year_3\Sem_2\Web Scraping\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Ensure the path is correct

# Configure Selenium WebDriver
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)

# Open a CSV file to store the scraped data
with open("job4.csv", "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Job Link", "Salary", "Job Type", "Job Level", "Gender", "Age",
                     "Years of Experience", "Language", "Category", "Industry", "Location", "Qualification",
                     "Available Position", "Required Skills", "Job Requirement"])

    # Open browser once
    driver = webdriver.Chrome(service=service, options=options)

    # Loop through job IDs from 1031 to 889
    for job_id in range(1086, 500, -1):  # Corrected range
        url = f"https://jobify.works/jobs/{job_id}"
        print(f"Fetching {url}...")

        try:
            driver.get(url)

            # Wait for job title to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-title"))
            )

            # Extract job title
            try:
                title = driver.find_element(By.CLASS_NAME, "job-title").text.strip()
            except Exception as e:
                title = "N/A"
                print(f"❌ Error extracting title for {url}: {e}")

            # Extract job details using labels
            def get_job_detail(label):
                try:
                    element = driver.find_element(By.XPATH, f"//strong[text()='{label}']")
                    return element.find_element(By.XPATH, "./following-sibling::text()").strip()
                except Exception as e:
                    print(f"❌ Error extracting {label} for {url}: {e}")
                    return "N/A"

            salary = get_job_detail("Salary:")
            job_type = get_job_detail("Job Type:")
            job_level = get_job_detail("Job Level:")
            gender = get_job_detail("Gender:")
            age = get_job_detail("Age:")
            experience = get_job_detail("Years of Experience:")  # Corrected label
            language = get_job_detail("Language:")
            category = get_job_detail("Category:")
            industry = get_job_detail("Industry:")
            location = get_job_detail("Location:")
            qualification = get_job_detail("Qualification:")
            available_position = get_job_detail("Available Position:")
            required_skills = get_job_detail("Required Skills:")

            # ✅ Extract Job Requirement (Now Works with JavaScript!)
            job_requirement = "N/A"
            try:
                job_req_section = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h5[text()='Job Requirement']/following-sibling::div"))
                )
                ul_elements = job_req_section.find_elements(By.TAG_NAME, "ul")
                li_elements = [li.text.strip() for ul in ul_elements for li in ul.find_elements(By.TAG_NAME, "li") if li.text.strip()]
                job_requirement = " | ".join(li_elements) if li_elements else "N/A"
            except Exception as e:
                print(f"❌ Job Requirement not found for {url}: {e}")

            print(f"Title: {title}, Job Requirement: {job_requirement}")

            # Write to CSV
            writer.writerow([title, url, salary, job_type, job_level, gender, age, experience, language,
                             category, industry, location, qualification, available_position, required_skills,
                             job_requirement])


        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")

    driver.quit()  # Close browser
