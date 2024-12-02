# Influencer Selection System - End-to-End Deep Learning Project

# Main analysis and results
## You can view the analysis of the data directly over here and worry about the boring part later:

https://influencer-impact-results.onrender.com/

## Table of Contents
- [Influencer Selection System - End-to-End Deep Learning Project](#influencer-selection-system---end-to-end-deep-learning-project)
- [Main analysis and results](#main-analysis-and-results)
  - [You can view the analysis of the data directly over here and worry about the boring part later:](#you-can-view-the-analysis-of-the-data-directly-over-here-and-worry-about-the-boring-part-later)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Problem Statement](#problem-statement)
    - [Objectives:](#objectives)
  - [Project Workflow](#project-workflow)
  - [Pipeline Components](#pipeline-components)
    - [Stage 1: Data Cleaning](#stage-1-data-cleaning)
    - [Stage 2: Gathering Results](#stage-2-gathering-results)
    - [Stage 3: Result Transformation](#stage-3-result-transformation)
  - [Project Structure](#project-structure)
  - [Setup](#setup)
  - [License](#license)

## Overview
This project is a **Deep Learning-based Influencer Selection System** designed to assist in identifying influencers who consistently drive better engagement in social media campaigns.  
The system analyzes ~200 videos, extracts unique faces of influencers, computes their average performance, and updates results dynamically when new data is provided.  

The solution is designed to scale, allowing seamless integration of new data and automatic updates to existing influencer records.

## Problem Statement
In the crowded world of social media, choosing the right influencer can make or break a campaign's success.  
You are tasked with building a **data-driven approach to influencer selection** using ~200 videos with their performance numbers.

### Objectives:
- **Identify unique influencers** appearing across these videos.
- **Calculate average performance** for each influencer.
- **Enable consistent evaluation** of influencers by dynamically updating results when new data is provided.

## Project Workflow
The project involves a **3-step pipeline** designed for professional use:
1. **Data Cleaning**: Deduplicate and clean video URLs, ensuring only unique content is processed.
2. **Face Extraction and Performance Mapping**: Extract unique faces and update influencer scores across videos.
3. **Result Transformation**: Update and maintain records dynamically, accounting for new influencers or data.

## Pipeline Components

### Stage 1: Data Cleaning
- **Objective**: Clean URLs and remove duplicate videos based on content.
- **Steps**:
  1. Parse video URLs and check for duplicate content.
  2. Retain only the first occurrence of a video with unique content.
  3. Append cleaned URLs to the existing URL repository for future reference.
  
### Stage 2: Gathering Results
- **Objective**: Extract unique faces from videos and compute performance scores.
- **Steps**:
  1. Use **Deep Learning models** to detect and extract faces from videos.
  2. Identify unique influencers across videos by comparing extracted face embeddings.
  3. Aggregate and update performance scores for each identified influencer.

### Stage 3: Result Transformation
- **Objective**: Transform and update results based on gathered data.
- **Steps**:
  1. Check if extracted influencers already exist in the database.
  2. Update the average performance scores for existing influencers.
  3. Add new influencers and their scores if they do not already exist.

## Project Structure
**Here is a detailed project structure if anyone cares:**
```bash
📂 influencer-selection                 # Root directory of the project
├── 📄 Assignment Data.xlsx             # Spreadsheet containing data to be analyzed
├── 📄 LICENSE                          # License file for the project
├── 📄 config.yaml                      # Configuration file for the project
├── 📂 logs                             # Directory for log files
│   └── 📄 logging.log                  # Log file for application runtime
├── 📄 main.py                          # Main script for running the project
├── 📂 main_data                        # Directory for main datasets
│   ├── 📂 influencer_avg_data         # Directory containing average influencer data
│   │   └── 📄 clean_data.xlsx         # Cleaned influencer average data
│   ├── 📂 model_training_data         # Directory containing data for model training
│   │   └── 📄 clean_data.xlsx         # Cleaned model training data
│   └── 📂 urls_score_data             # Directory containing URL and score data
│       └── 📄 clean_data.xlsx         # Cleaned URL and score data
├── 📄 requirements.txt                # List of Python dependencies
├── 📂 research_deepface               # Directory for deep learning-based research on face extraction
│   ├── 📄 cleaning-test.ipynb         # Jupyter notebook for testing cleaning
│   ├── 📄 final_img_extraction.ipynb  # Jupyter notebook for extracting final images
│   ├── 📄 tesssst.ipynb               # Test notebook for experiments
│   ├── 📄 test-metric-Final_copy.ipynb # Jupyter notebook for testing metrics (final copy)
│   └── 📄 test-metric-Final.ipynb     # Jupyter notebook for testing metrics
├── 📂 research_modular                # Directory for modular research notebooks
│   ├── 📄 data_cleaning.ipynb         # Jupyter notebook for data cleaning module
│   ├── 📄 model_training.ipynb        # Jupyter notebook for model training module
│   └── 📄 result_transformation.ipynb # Jupyter notebook for result transformation module
├── 📂 src                              # Source code directory
│   ├── 📄 __init__.py                 # Initialization file for the source module
│   ├── 📂 components                  # Directory for core components of the pipeline
│   │   ├── 📄 __init__.py             # Initialization file for components
│   │   ├── 📂 __pycache__             # Cached Python files for components
│   │   │   ├── 📄 __init__.cpython-39.pyc
│   │   │   ├── 📄 data_cleaning.cpython-39.pyc
│   │   │   ├── 📄 model_training.cpython-39.pyc
│   │   │   └── 📄 result_transformation.cpython-39.pyc
│   │   ├── 📄 data_cleaning.py        # Data cleaning component
│   │   ├── 📄 model_training.py       # Model training component
│   │   └── 📄 result_transformation.py # Result transformation component
│   ├── 📂 config                       # Directory for configuration files
│   │   ├── 📄 __init__.py             # Initialization file for configuration
│   │   ├── 📂 __pycache__             # Cached Python files for config
│   │   │   ├── 📄 __init__.cpython-39.pyc
│   │   │   └── 📄 configuration.cpython-39.pyc
│   │   └── 📄 configuration.py        # Configuration script
│   ├── 📂 constants                   # Directory for constant values
│   │   ├── 📄 __init__.py             # Initialization file for constants
│   │   └── 📂 __pycache__             # Cached Python files for constants
│   │       └── 📄 __init__.cpython-39.pyc
│   ├── 📂 entity                      # Directory for entity definitions
│   │   ├── 📄 __init__.py             # Initialization file for entity module
│   │   ├── 📂 __pycache__             # Cached Python files for entity
│   │   │   ├── 📄 __init__.cpython-39.pyc
│   │   │   └── 📄 config_entity.cpython-39.pyc
│   │   └── 📄 config_entity.py        # Entity configuration script
│   ├── 📂 pipeline                    # Directory for the pipeline components
│   │   ├── 📄 __init__.py             # Initialization file for pipeline module
│   │   ├── 📂 __pycache__             # Cached Python files for pipeline
│   │   │   ├── 📄 __init__.cpython-39.pyc
│   │   │   ├── 📄 data_cleaning.cpython-39.pyc
│   │   │   ├── 📄 model_training.cpython-39.pyc
│   │   │   └── 📄 result_transformation.cpython-39.pyc
│   │   ├── 📄 data_cleaning.py        # Data cleaning pipeline component
│   │   ├── 📄 model_training.py       # Model training pipeline component
│   │   └── 📄 result_transformation.py # Result transformation pipeline component
│   └── 📂 utils                       # Utility functions
│       ├── 📄 __init__.py             # Initialization file for utils
│       ├── 📂 __pycache__             # Cached Python files for utils
│       │   ├── 📄 __init__.cpython-39.pyc
│       │   └── 📄 common.cpython-39.pyc
│       └── 📄 common.py               # Common utility functions
├── 📂 static                          # Directory for static files (e.g., images, styles)
├── 📂 temp_data                       # Temporary data storage
│   ├── 📂 influencer_avg_data        # Temporary data for influencer average scores
│   ├── 📂 model_training_data        # Temporary data for model training
│   │   └── 📄 2024-12-02_02-28-53.xlsx # Temporary model training data file
│   └── 📂 url_score_data             # Temporary data for URL and score information
│       ├── 📂 clean                  # Cleaned temporary data
│       │   └── 📄 2024-12-02_01-37-26.xlsx # Cleaned data
│       └── 📂 raw                    # Raw temporary data
│           └── 📄 Assignment Data.xlsx # Raw data for assignment
├── 📂 temp_unique_faces               # Temporary directory for unique face images
│   └── 📄 temp_face.jpg               # Temporary face image
├── 📂 templates                       # Directory for HTML templates
│   └── 📄 table.html                  # HTML file for displaying tables
├── 📄 test.py                         # Test script
└── 📂 test_dir                        # Directory for testing purposes
    └── 📄 temp_face_0.jpg             # Test face image
```

## Setup
Follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/influencer-selection.git
   cd influencer-selection
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Prepare Data**
   ```bash
   Place the raw video files in the data/raw_videos directory.
   Ensure all input videos are in an acceptable format (e.g., .mp4, .avi)

## Usage
**To execute the pipeline, follow these steps:**
  ```bash
  python main.py
```

**To execute the Flask Web App, follow these steps:**
```bash
  python test.py
```

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).