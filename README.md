# 🚀 Job Market Scraping & RAG Data Pipeline

A comprehensive web scraping project for collecting and processing job data from multiple Cambodian job portals (CamHR, Jobify, and Workinga) with automated markdown generation for Retrieval-Augmented Generation (RAG) systems.

## 📁 Project Structure

```
Web Scraping/
│
├── 📓 Jupyter Notebooks (Main Scrapers)
│   ├── CamHR_Scraper.ipynb          # CamHR.com job scraper
│   ├── Jobify_Scraper.ipynb         # Jobify.works job scraper
│   └── Workinga_Scraper.ipynb       # Workinga.com job scraper
│
├── 🐍 Original Python Scripts
│   ├── camhr.py                     # Original CamHR scraper
│   ├── Jobify.py                    # Original Jobify scraper
│   └── Workinga.py                  # Original Workinga scraper
│
├── 🔄 Markdown Generation Scripts
│   ├── convert_camhr_to_md.py       # CamHR data → Markdown (IT focus)
│   ├── convert_jobify_to_md.py      # Jobify data → Markdown
│   └── generate_individual_job_markdowns.py  # Individual job files
│
├── 📊 Data Files
│   ├── CamHr.csv                    # CamHR scraped data
│   ├── Jobify.csv                   # Jobify scraped data
│   ├── job4.csv                     # Additional job data
│   └── Workinga.csv                 # Workinga scraped data
│
└── 📝 Generated Markdown Directories
    ├── CamHr_IT_Jobs/               # IT-focused CamHR jobs
    ├── Jobify_markdowns/            # Jobify job descriptions
    ├── Jobify_descriptions/         # Alternative Jobify format
    ├── Workina_descriptions/        # Workinga job descriptions
    └── job_descriptions_individual/ # Individual job files
```

## 🎯 Purpose & Use Cases

This project is designed for:
- **Job Market Analysis**: Understanding employment trends in Cambodia
- **RAG System Training**: Generating structured markdown data for AI systems
- **Career Research**: Comprehensive job requirement analysis
- **Educational Research**: Labor market studies and analysis

## 🔧 Technical Stack

- **Python 3.x**
- **Selenium WebDriver** - Dynamic content scraping
- **BeautifulSoup4** - HTML parsing
- **Pandas** - Data manipulation and analysis
- **CSV/Excel/JSON** - Multiple export formats
- **Markdown** - RAG-ready documentation format

## 📓 Jupyter Notebooks Overview

### 1. CamHR_Scraper.ipynb
**Source**: CamHR.com (Cambodia Human Resources)

**Features**:
- 18 data fields extraction
- Company and job classification
- Salary and requirement analysis
- Real-time progress tracking
- Multiple export formats

**Data Fields**:
```
Job Title, Company Name, Level, Year of Exp., Hiring, Salary, 
Sex, Age, Term, Function, Industry, Qualification, Language, 
Location, Job Requirements, Publish Date, Closing Date, Link URL
```

### 2. Jobify_Scraper.ipynb
**Source**: Jobify.works

**Features**:
- 16 comprehensive job attributes
- Advanced error handling
- Background processing
- Job requirement extraction
- Market trend analysis

**Data Fields**:
```
Job Title, Job Link, Salary, Job Type, Job Level, Gender, Age,
Years of Experience, Language, Category, Industry, Location,
Qualification, Available Position, Required Skills, Job Requirement
```

### 3. Workinga_Scraper.ipynb
**Source**: Workinga.com

**Features**:
- 11 essential job fields
- Robust data validation
- Error recovery mechanisms
- Progress monitoring
- Quality assessment

**Data Fields**:
```
Job Title, Company Name, Salary, Available, Office, Location,
Employment Type, Closing Date, Job Responsibilities, 
Job Requirements, Link
```

## 🔄 Markdown Generation Pipeline

### For RAG System Preparation

#### 1. convert_camhr_to_md.py
- **Purpose**: Converts CamHR CSV data to structured markdown
- **Specialization**: IT job filtering and categorization
- **Output**: Individual markdown files for each IT position
- **Features**:
  - IT keyword detection and filtering
  - Clean text processing
  - Structured markdown formatting
  - Metadata preservation

#### 2. convert_jobify_to_md.py
- **Purpose**: Transforms Jobify data into markdown format
- **Output**: Comprehensive job description files
- **Features**:
  - Job ID extraction and filename safety
  - Detailed job information structuring
  - Clean data formatting
  - Cross-platform compatibility

#### 3. generate_individual_job_markdowns.py
- **Purpose**: Creates individual markdown files for each job listing
- **Source**: job4.csv (general job data)
- **Features**:
  - Unique filename generation
  - Job ID extraction from titles
  - Safe character handling
  - Comprehensive job detail formatting

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
pip install selenium beautifulsoup4 pandas openpyxl
```

### 2. WebDriver Configuration
- Download Chrome WebDriver
- Update paths in configuration classes:
```python
CHROME_DRIVER_PATH = r"path\to\chromedriver.exe"
```

### 3. Running the Scrapers
Open any notebook and:
1. Run cells sequentially
2. Modify configuration parameters
3. Uncomment execution lines
4. Monitor progress in real-time

### 4. Generate RAG-Ready Markdown
```bash
python convert_camhr_to_md.py      # For IT-focused jobs
python convert_jobify_to_md.py     # For Jobify data
python generate_individual_job_markdowns.py  # For individual files
```

## 📊 Data Output Formats

### Primary Formats
- **CSV**: Raw structured data
- **Excel**: Formatted spreadsheets with summaries
- **JSON**: API-friendly format
- **Markdown**: RAG-ready documentation

### Markdown Structure Example
```markdown
# Software Developer (JB-12345)

## Company Name
TechCorp Cambodia

## Job Level
Senior Level

## Salary
$1000 - $1500

## Job Requirements
- Bachelor's degree in Computer Science
- 3+ years Python experience
- Knowledge of web frameworks
```

## 🔍 Key Features

### Advanced Scraping Capabilities
- **Headless Operation**: Background processing
- **Error Recovery**: Robust error handling
- **Rate Limiting**: Respectful server interaction
- **Progress Tracking**: Real-time updates
- **Data Validation**: Quality assurance

### Analytics & Insights
- **Market Trends**: Industry and location analysis
- **Salary Insights**: Compensation trends
- **Skill Requirements**: Most demanded skills
- **Company Analysis**: Top hiring organizations

### RAG Optimization
- **Structured Format**: Consistent markdown structure
- **Metadata Rich**: Comprehensive job information
- **Clean Text**: Processed and formatted content
- **Searchable**: Optimized for retrieval systems

## 🎯 RAG System Integration

The generated markdown files are optimized for RAG systems with:

### Structured Content
- Clear headings and sections
- Consistent formatting
- Metadata preservation
- Clean text processing

### Search Optimization
- Keyword-rich content
- Standardized terminology
- Categorical organization
- Cross-reference capabilities

### Example RAG Query Results
```
Query: "What are the requirements for senior developer positions?"
Result: Aggregated requirements from multiple job postings with 
        salary ranges, skill requirements, and company information
```

## 📈 Performance Metrics

### Scraping Efficiency
- **CamHR**: ~2-3 seconds per job
- **Jobify**: ~1-2 seconds per job  
- **Workinga**: ~1-2 seconds per job

### Data Quality
- **Completeness**: 85-95% field completion
- **Accuracy**: Validated extraction methods
- **Consistency**: Standardized formatting

## ⚖️ Ethical Considerations

### Responsible Scraping
- ✅ Rate limiting and delays
- ✅ Respectful server interaction
- ✅ Error handling for server protection
- ✅ Terms of service compliance

### Data Usage
- 🎓 Educational and research purposes
- 📊 Market analysis and insights
- 🤖 AI/ML model training data
- 📈 Career guidance and planning

## 🔧 Configuration Options

### Scraping Parameters
```python
# Example configuration
START_ID = 10000
END_ID = 15000
WAIT_TIMEOUT = 5
DELAY = 0.5
OUTPUT_FORMAT = ['csv', 'excel', 'json']
```

### Markdown Generation
```python
# Customization options
OUTPUT_DIR = 'path/to/markdown/files'
IT_KEYWORDS = ['python', 'java', 'developer', ...]
INCLUDE_METADATA = True
CLEAN_TEXT = True
```

## 📚 Documentation & Support

### Notebook Documentation
Each notebook contains:
- Comprehensive markdown explanations
- Step-by-step instructions
- Code comments and docstrings
- Usage examples and best practices

### Error Handling
- Detailed error messages
- Troubleshooting guides
- Recovery mechanisms
- Performance optimization tips

## 🔮 Future Enhancements

### Planned Features
- [ ] Automated scheduling and monitoring
- [ ] Additional job portal integration
- [ ] Enhanced RAG optimization
- [ ] Real-time dashboard creation
- [ ] API endpoint development
- [ ] Machine learning integration

### RAG System Improvements
- [ ] Vector embedding optimization
- [ ] Query enhancement algorithms
- [ ] Response ranking systems
- [ ] Multi-language support

## 📞 Support & Contributing

For questions, issues, or contributions:
- Review the comprehensive notebook documentation
- Check configuration settings
- Verify WebDriver setup
- Ensure CSV files are properly formatted

## 📄 License & Usage

This project is designed for educational and research purposes. Please ensure compliance with respective websites' terms of service and use responsibly.

---

**Happy Job Market Analysis & RAG Development! 🚀**

*Last Updated: July 2025*
