import pandas as pd
import os
import re
from pathlib import Path

def clean_text(text):
    if pd.isna(text):
        return ""
    # Remove extra whitespace and clean up text
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = text.replace('|', '')  # Remove any pipe characters
    return text

def create_markdown_file(row, output_dir):
    # Extract job ID from the Job Link
    job_id = row['Job Link'].split('/')[-1] if pd.notna(row['Job Link']) else ''
    job_title = clean_text(row['Job Title'].split('(')[0].strip() if pd.notna(row['Job Title']) else 'Untitled')
    
    # Create a safe filename
    safe_title = re.sub(r'[^\w\s-]', '', job_title).strip().replace(' ', '_')
    filename = f"{safe_title}_{job_id}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Prepare markdown content
    md_content = f"# {job_title}\n\n"
    
    # Add job details
    if job_id:
        md_content += f"## Position ID: {job_id}\n\n"
    
    if pd.notna(row['Job Link']):
        md_content += f"### Job Link\n{row['Job Link']}\n\n"
    
    # Add salary if available
    if pd.notna(row['Salary']) and str(row['Salary']).lower() not in ['n/a', 'negotiable', '']:
        md_content += f"### Salary\n{row['Salary']}\n\n"
    
    # Add job requirements
    if pd.notna(row['Job Requirement']):
        requirements = row['Job Requirement'].split('|')
        md_content += "### Job Requirement\n"
        for req in requirements:
            req = clean_text(req)
            if req:  # Only add non-empty requirements
                md_content += f"- {req}\n"
        md_content += "\n"
    
    # Add required skills if available
    if pd.notna(row['Required Skills']):
        skills = row['Required Skills'].split('|')
        md_content += "### Required Skills\n"
        for skill in skills:
            skill = clean_text(skill)
            if skill:  # Only add non-empty skills
                md_content += f"- {skill}\n"
        md_content += "\n"
    
    # Add additional job details
    details = []
    if pd.notna(row['Job Type']):
        details.append(f"**Job Type:** {row['Job Type']}")
    if pd.notna(row['Job Level']):
        details.append(f"**Level:** {row['Job Level']}")
    if pd.notna(row['Location']):
        location = clean_text(row['Location'])
        details.append(f"**Location:** {location}")
    if pd.notna(row['Years of Experience']):
        details.append(f"**Experience Required:** {row['Years of Experience']}")
    
    if details:
        md_content += "### Job Details\n" + "  \n".join(details) + "\n"
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filename

def main():
    # Create output directory if it doesn't exist
    output_dir = "Jobify_markdowns"
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the CSV file with different encodings
    encodings = ['latin1', 'iso-8859-1', 'cp1252', 'utf-8']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv('Jobify.csv', encoding=encoding, on_bad_lines='skip')
            if not df.empty:
                print(f"Successfully read file with {encoding} encoding")
                break
        except Exception as e:
            print(f"Failed with {encoding}: {str(e)}")
    
    if df is None or df.empty:
        raise ValueError("Could not read the CSV file with any encoding")
    
    # Process each row and create markdown files
    created_files = []
    for _, row in df.iterrows():
        try:
            filename = create_markdown_file(row, output_dir)
            created_files.append(filename)
        except Exception as e:
            print(f"Error processing row {_}: {str(e)}")
    
    print(f"\nSuccessfully created {len(created_files)} markdown files in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
