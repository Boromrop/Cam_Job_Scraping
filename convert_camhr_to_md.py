import os
import re
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def is_it_job(row):
    it_keywords = [
        'it', 'software', 'developer', 'programmer', 'engineer', 
        'system', 'network', 'devops', 'data', 'cyber', 'security',
        'technical', 'support', 'cloud', 'web', 'mobile', 'application',
        'programming', 'coding', 'ai', 'artificial intelligence', 
        'machine learning', 'ml', 'database', 'it support', 'network',
        'infrastructure', 'it infrastructure', 'it specialist', 'it officer',
        'it executive', 'it manager', 'it administrator', 'it consultant', 
        'it analyst', 'it project', 'it security', 'it technician',
        'computer', 'technology', 'information technology', 'tech', 'developer',
        'programmer', 'systems', 'network', 'server', 'database', 'frontend',
        'backend', 'fullstack', 'full-stack', 'full stack', 'ui/ux', 'ui-ux',
        'devops', 'cloud', 'aws', 'azure', 'google cloud', 'gcp', 'cybersecurity',
        'information security', 'infosec', 'web', 'mobile', 'ios', 'android',
        'blockchain', 'ai', 'artificial intelligence', 'machine learning',
        'data science', 'data analyst', 'data engineer', 'big data', 'etl',
        'qa', 'quality assurance', 'tester', 'testing', 'automation',
        'devops', 'sre', 'site reliability', 'sysadmin', 'system administrator',
        'network engineer', 'security engineer', 'cloud engineer', 'solutions architect',
        'technical lead', 'cto', 'cio', 'it director', 'it manager'
    ]
    
    title = str(row.get('Job Title', '')).lower()
    function = str(row.get('Function', '')).lower()
    industry = str(row.get('Industry', '')).lower()
    requirements = str(row.get('Job Requirements', '')).lower()
    
    # Check if any IT keyword is in title, function, industry, or requirements
    for keyword in it_keywords:
        if (keyword in title) or (keyword in function) or (keyword in industry) or (keyword in requirements):
            return True
    return False

def create_markdown_file(row, output_dir):
    # Safely get values with default empty string if key doesn't exist
    job_title = clean_text(row.get('Job Title', 'Untitled Position'))
    company = clean_text(row.get('Company Name', 'Not Specified'))
    location = clean_text(row.get('Location', 'Not Specified'))
    salary = clean_text(row.get('Salary', 'Negotiable'))
    job_level = clean_text(row.get('Level', 'Not Specified'))
    experience = clean_text(row.get('Years of Exp.', 'Not Specified'))
    job_type = clean_text(row.get('Term', 'Full Time'))
    requirements = clean_text(row.get('Job Requirements', 'Not Specified'))
    publish_date = clean_text(row.get('Publish Date', ''))
    closing_date = clean_text(row.get('Closing Date', ''))
    job_url = clean_text(row.get('Link URL', ''))
    
    safe_title = re.sub(r'[^\w\s-]', '', job_title).strip().replace(' ', '_')
    filename = f"{safe_title}.md"
    filepath = os.path.join(output_dir, filename)
    
    md_content = f"# {job_title}\n\n"
    md_content += f"## Company\n{company}\n\n"
    md_content += f"## Location\n{location}\n\n"
    
    # Add salary if available
    if salary and salary.lower() not in ['negotiable', 'not specified', 'n/a', '']:
        md_content += f"## Salary\n{salary}\n\n"
    
    # Add job metadata
    md_content += f"## Job Level\n{job_level}\n\n"
    md_content += f"## Experience Required\n{experience}\n\n"
    md_content += f"## Job Type\n{job_type}\n\n"
    
    # Add dates if available
    if publish_date and 'not found' not in publish_date.lower():
        md_content += f"## Published Date\n{publish_date}\n\n"
    if closing_date and 'not found' not in closing_date.lower():
        md_content += f"## Closing Date\n{closing_date}\n\n"
    
    # Add job requirements
    if requirements and requirements.lower() not in ['not found', 'not specified', 'n/a', '']:
        md_content += "## Job Requirements\n"
        # Split by bullet points or newlines
        req_list = [r.strip() for r in re.split(r'•|\n', requirements) if r.strip()]
        if req_list:
            for req in req_list:
                if req.strip():
                    md_content += f"- {req.strip()}\n"
            md_content += "\n"
    
    # Add application link if available
    if job_url and job_url.lower() not in ['not found', 'not specified', 'n/a', '']:
        md_content += f"## Apply Here\n{job_url}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filename

def read_csv_file(file_path):
    """Read CSV file with robust handling of various formats"""
    data = []
    
    try:
        # First, try to detect the file encoding
        import chardet
        
        # Read a sample of the file to detect encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB to guess encoding
            
        # Detect encoding
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Detected encoding: {encoding} with confidence {result['confidence']}")
        
        # Read the entire file with detected encoding
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            # Read all lines and clean them
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        if not lines:
            print("File is empty")
            return None, None
            
        # The first line is the header - clean it up
        header_line = lines[0].strip('\ufeff')  # Remove BOM if present
        header = [h.strip().strip('"') for h in header_line.split(',')]
        print(f"Found columns: {header}")
        
        # Process each line as a separate record
        for i, line in enumerate(lines[1:], 1):  # Skip header
            try:
                # Clean the line and split by comma, handling quoted fields
                line = line.strip()
                if not line:
                    continue
                    
                # Use csv module to parse the line
                import io
                import csv
                
                # Create a file-like object from the line
                line_io = io.StringIO(line)
                reader = csv.reader(line_io, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
                
                try:
                    values = next(reader)
                except Exception as e:
                    print(f"Error parsing line {i}: {str(e)}")
                    print(f"Problematic line: {line}")
                    continue
                
                # Create a dictionary with column names and values
                row = {}
                for j, col in enumerate(header):
                    if j < len(values):
                        row[col] = values[j].strip('"\'').strip()
                    else:
                        row[col] = ''
                
                # Special handling for job title and company which might be combined
                if 'Job Title' in row and ('Company Name' not in row or not row['Company Name']) and ',' in row['Job Title']:
                    parts = row['Job Title'].split(',')
                    if len(parts) > 1:
                        row['Job Title'] = parts[0].strip()
                        row['Company Name'] = parts[1].strip()
                
                # Only add non-empty rows
                if any(v for v in row.values() if v):
                    data.append(row)
                
            except Exception as e:
                print(f"Error processing line {i+1}: {str(e)}")
                print(f"Problematic line: {line}")
                continue
        
        print(f"Successfully processed {len(data)} job listings")
        return data, header
        
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

def clean_text(text):
    if not text or text.lower() in ['nan', 'na', 'n/a', 'none', 'null']:
        return ''
    if not isinstance(text, str):
        text = str(text)
    return text.strip()

def is_it_job(row):
    it_keywords = [
        'it', 'software', 'developer', 'programmer', 'engineer', 
        'system', 'network', 'devops', 'data', 'cyber', 'security',
        'technical', 'support', 'cloud', 'web', 'mobile', 'application',
        'programming', 'coding', 'ai', 'artificial intelligence', 
        'machine learning', 'ml', 'database', 'it support', 'network',
        'infrastructure', 'it infrastructure', 'it specialist', 'it officer',
        'it executive', 'it manager', 'it administrator', 'it consultant', 
        'it analyst', 'it project', 'it security', 'it technician',
        'computer', 'technology', 'information technology', 'tech', 'developer',
        'programmer', 'systems', 'network', 'server', 'database', 'frontend',
        'backend', 'fullstack', 'full-stack', 'full stack', 'ui/ux', 'ui-ux',
        'devops', 'cloud', 'aws', 'azure', 'google cloud', 'gcp', 'cybersecurity',
        'information security', 'infosec', 'web', 'mobile', 'ios', 'android',
        'blockchain', 'ai', 'artificial intelligence', 'machine learning',
        'data science', 'data analyst', 'data engineer', 'big data', 'etl',
        'qa', 'quality assurance', 'tester', 'testing', 'automation',
        'devops', 'sre', 'site reliability', 'sysadmin', 'system administrator',
        'network engineer', 'security engineer', 'cloud engineer', 'solutions architect',
        'technical lead', 'cto', 'cio', 'it director', 'it manager',
        'developer', 'programmer', 'coder', 'software', 'hardware', 'network',
        'system admin', 'system administrator', 'tech support', 'helpdesk',
        'desktop support', 'it helpdesk', 'it support', 'network admin',
        'network administrator', 'system engineer', 'systems engineer',
        'devops engineer', 'cloud architect', 'cloud engineer', 'aws engineer',
        'azure engineer', 'gcp engineer', 'cloud administrator', 'cloud architect',
        'cloud consultant', 'cloud developer', 'cloud devops engineer',
        'cloud infrastructure engineer', 'cloud network engineer',
        'cloud security engineer', 'cloud solutions architect', 'cloud system administrator',
        'cloud systems engineer', 'senior cloud engineer', 'aws cloud engineer',
        'azure cloud engineer', 'gcp cloud engineer', 'cloud support engineer',
        'cloud operations engineer', 'cloud platform engineer', 'cloud software engineer',
        'cloud systems administrator', 'cloud infrastructure architect',
        'cloud security architect', 'cloud network architect', 'cloud solutions engineer'
    ]
    
    # Get all text fields from the row
    text_to_check = ''
    for key, value in row.items():
        if isinstance(value, str):
            text_to_check += ' ' + value.lower()
    
    # Check if any IT keyword is in the combined text
    for keyword in it_keywords:
        if keyword.lower() in text_to_check:
            return True
    
    return False

def create_markdown_file(row, output_dir):
    """Create a markdown file for a job listing"""
    # Get job details with defaults for missing fields
    job_title = clean_text(row.get('Job Title', 'Untitled Position'))
    
    # If job title is still 'Untitled Position', try to find a better title
    if job_title == 'Untitled Position' and 'Job Requirements' in row:
        # Try to extract a title from the requirements
        requirements = row['Job Requirements']
        if isinstance(requirements, str):
            # Look for patterns like "Position: [Title]" or "Title: [Title]"
            title_match = re.search(r'(?:Position|Title)[:\s]+([^\n\r\t]+)', requirements, re.IGNORECASE)
            if title_match:
                job_title = clean_text(title_match.group(1))
    
    company = clean_text(row.get('Company Name', 'Not Specified'))
    location = clean_text(row.get('Location', 'Not Specified'))
    salary = clean_text(row.get('Salary', 'Negotiable'))
    job_level = clean_text(row.get('Level', 'Not Specified'))
    experience = clean_text(row.get('Year of Exp.', row.get('Years of Exp.', 'Not Specified')))
    job_type = clean_text(row.get('Term', 'Full Time'))
    requirements = clean_text(row.get('Job Requirements', 'Not Specified'))
    publish_date = clean_text(row.get('Publish Date', ''))
    closing_date = clean_text(row.get('Closing Date', ''))
    job_url = clean_text(row.get('Link URL', row.get('URL', '')))
    
    # If we still don't have a good title, use the first line of requirements
    if job_title == 'Untitled Position' and requirements and requirements != 'Not Specified':
        first_line = requirements.split('\n')[0].strip()
        if first_line and len(first_line) < 100:  # Only use if it's a reasonable length
            job_title = first_line
    
    # Create a safe filename based on job title
    safe_title_base = re.sub(r'[^\w\s-]', '', job_title).strip().replace(' ', '_')
    
    # If the job title is empty or results in an empty string after sanitization, use a unique fallback
    if not safe_title_base:
        safe_title_base = f"Untitled_Job_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}"

    filename_candidate = f"{safe_title_base}.md"
    filepath = os.path.join(output_dir, filename_candidate)
    
    # Handle potential filename collisions by appending a counter
    counter = 1
    while os.path.exists(filepath):
        filename_candidate = f"{safe_title_base}_{counter}.md"
        filepath = os.path.join(output_dir, filename_candidate)
        counter += 1
    
    filename = filename_candidate # Final unique filename
    
    # Prepare markdown content
    md_content = f"# {job_title}\n\n"
    md_content += f"## Company\n{company}\n\n"
    md_content += f"## Location\n{location}\n\n"
    
    # Add salary if available
    if salary and salary.lower() not in ['negotiable', 'not specified', 'n/a', '']:
        md_content += f"## Salary\n{salary}\n\n"
    
    # Add job metadata
    md_content += f"## Job Level\n{job_level}\n\n"
    md_content += f"## Experience Required\n{experience}\n\n"
    md_content += f"## Job Type\n{job_type}\n\n"
    
    # Add dates if available
    if publish_date and 'not found' not in publish_date.lower():
        md_content += f"## Published Date\n{publish_date}\n\n"
    if closing_date and 'not found' not in closing_date.lower():
        md_content += f"## Closing Date\n{closing_date}\n\n"
    
    # Add job requirements
    if requirements and requirements.lower() not in ['not found', 'not specified', 'n/a', '']:
        md_content += "## Job Requirements\n"
        # Split by bullet points or newlines
        req_list = [r.strip() for r in re.split(r'•|\n', requirements) if r.strip()]
        if req_list:
            for req in req_list:
                if req.strip():
                    md_content += f"- {req.strip()}\n"
            md_content += "\n"
    
    # Add application link if available
    if job_url and job_url.lower() not in ['not found', 'not specified', 'n/a', '']:
        md_content += f"## Apply Here\n{job_url}\n"
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return filename
    except Exception as e:
        print(f"Error writing file {filename}: {str(e)}")
        return None

def main():
    # Create output directory if it doesn't exist
    output_dir = "CamHr_IT_Jobs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the CSV file
    print("Reading CSV file...")
    data, headers = read_csv_file('CamHr.csv')
    
    if not data or not headers:
        raise ValueError("Could not read the CSV file with any encoding")
    
    print(f"\nFound {len(data)} job listings")
    print(f"Columns: {headers}")
    
    # Filter IT jobs
    print("\nFiltering IT jobs...")
    it_jobs = [job for job in data if is_it_job(job)]
    
    if not it_jobs:
        print("No IT jobs found in the CSV file.")
        return
    
    print(f"Found {len(it_jobs)} IT-related jobs.")
    
    # Create markdown files for IT jobs
    created_files = 0
    skipped_files = 0
    
    for job in it_jobs:
        try:
            job_title = job.get('Job Title', 'Untitled').strip()
            company = job.get('Company Name', '').strip()
            
            if not job_title or job_title.lower() == 'nan':
                print("Skipping job with no title")
                skipped_files += 1
                continue
                
            print(f"Processing: {job_title} at {company}")
            
            filename = create_markdown_file(job, output_dir)
            if filename:
                created_files += 1
            else:
                skipped_files += 1
                
        except Exception as e:
            print(f"Error processing job: {str(e)}")
            skipped_files += 1
    
    print(f"\nSuccessfully created {created_files} IT job markdown files in the '{output_dir}' directory.")
    if skipped_files > 0:
        print(f"Skipped {skipped_files} jobs due to errors.")

if __name__ == "__main__":
    main()
