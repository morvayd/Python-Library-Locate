# Python-Library-Locate App
This Python script ([Python-Library-Locate.py](https://github.com/morvayd/Ollama-docling-RAG/tree/main) is a Python package location finder that searches your system for installed Python libraries.

**What It Does:**

Scans all Python library folders on your system.
Searches for specific packages you're interested in.
Identifies where each package is actually located on your hard drive
Exports results to a CSV file in your Documents folder

**Key Features:**

Cross-platform: Works on Windows, Linux, and macOS
Customizable search: Edit [strPackList](GitHub-Python Library Locate/Python-Library-Locate.py:50) to specify which packages to locate
Comprehensive scanning: Checks all Python path directories, filtering out non-folders and lib-dynload
Detailed output: CSV contains three columns: Hard Drive Path, Matched Folder, and Requested Library
Logging: Uses custom PythonLog module to track execution

This python app was developed utilizing Python 3.13.7
  - Testing occurred on Windows 11, MacOS 15.3.1 and Linux Mint 22.04.
  - Straightforward app, run as a .py file, no GUI built in.    

#  Install Procedure 

0) Install Python libraries
   - pip install pandas

#  Run the app within Python
1) python3 "Python-Library-Locate.py"
  - The app will initialize, run, find all the locations on the hard drive where the requested libraries reside.
  - A .csv will be created within the app folder.
  - PythonLogs folder - will contain a basic log of this apps' operation.

2) Issues, trouble, enhancements, please post within the repository issues.

Note:  the above summary was created using the IBM Project Bob AI.  

Thank you!

D. Morvay
