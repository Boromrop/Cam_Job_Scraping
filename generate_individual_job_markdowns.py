import csv
import os
import re

# Path to the CSV file
csv_file = 'd:/DSE_Folder/Year_3/Sem_2/Web Scraping/job4.csv'
output_dir = 'd:/DSE_Folder/Year_3/Sem_2/Web Scraping/job_descriptions_individual'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file
jobs = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        jobs.append(row)

# Create a markdown file for each job listing
count = 0
for job in jobs:
    full_title = job['Job Title']
    
    # Extract job ID
    job_id_match = re.search(r'\(JB-(\d+)\)', full_title)
    job_id = job_id_match.group(1) if job_id_match else "Unknown"
    
    # Create a safe filename with job ID to ensure uniqueness
    safe_title = re.sub(r'[^\w\s-]', '', full_title).strip().replace(' ', '_')
    file_path = f"{output_dir}/{safe_title}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        # Write the title
        f.write(f"# {full_title}\n\n")
        
        # Write job details
        for key, value in job.items():
            if key != 'Job Title' and value and value != "N/A":
                f.write(f"## {key}\n")
                f.write(f"{value}\n\n")
    
    count += 1

print(f"Created {count} markdown files in {output_dir}")
