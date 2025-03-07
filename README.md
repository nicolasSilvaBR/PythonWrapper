## Version 1.0
## 04/03/2025
## Python 3.12.5   
# Change

# Support Document
[Sharepoint](https://icmcslie.sharepoint.com/:x:/s/ProjectsHub/EV0hjbjXNOhOhazL9NTmA-EB9GBIjwxfRDutUlmldeCO2Q?e=gTkvdX)

# Table of Contents
1. [Overview](#overview)  
2. [Installation Instructions](#installation-instructions)  
   - 2.1 [Choose an Installation Directory](#choose-an-installation-directory)  
     - 2.1.1 [Decide where you want the application files to be installed](#decide-where-you-want-the-application-files-to-be-installed)  
     - 2.1.2 [Move and Extract the ZIP Folder](#move-and-extract-the-zip-folder)  
     - 2.2.3 [Navigate to the Extracted Folder](#navigate-to-the-extracted-folder)  
3. [Installing Python](#installing-python)  
4. [Run the Setup Batch File](#run-the-setup-batch-file)  
5. [Access the Application](#access-the-application)  
6. [Setting Up Automatic Background Execution of Streamlit Apps on Windows](#setting-up-automatic-background-execution-of-streamlit-apps-on-windows)  
   - 6.1 [Step 1: Create a Batch Script to Run Streamlit Apps in the Background](#step-1-create-a-batch-script-to-run-streamlit-apps-in-the-background)  
     - 6.1.1 [Creating the .bat file](#creating-the-bat-file)  
     - 6.1.2 [Save the file](#save-the-file)  
   - 6.2 [Step 2: Set Up Task Scheduler to Run the Script at Startup](#step-2-set-up-task-scheduler-to-run-the-script-at-startup)  
     - 6.2.1 [Opening the Task Scheduler](#opening-the-task-scheduler)  
   - 6.3 [Step 3: Create a New Task](#step-3-create-a-new-task)  
   - 6.4 [Step 4: Configure Triggers](#step-4-configure-triggers)  
   - 6.5 [Step 5: Configure Actions](#step-5-configure-actions)  
   - 6.6 [Step 6: Test the Task](#step-6-test-the-task)  
7. [Required Software and Libraries](#required-software-and-libraries)  
   - 7.1 [Python](#python)  
   - 7.2 [pip (Python Package Installer)](#pip-python-package-installer)  
   - 7.3 [Pre-downloaded Python Dependencies (.whl files)](#pre-downloaded-python-dependencies-whl-files)  
   - 7.4 [Streamlit](#streamlit)  
8. [Python Naming Conventions and Best Practices](#python-naming-conventions-and-best-practices)  
   - 8.1 [Summary of Naming Conventions](#summary-of-naming-conventions)  
9. [App](#app)

---

## 1. Overview
The Infeed700 application is an interactive platform developed by ICMC Solutions using Streamlit. It provides embedded dashboards and SSRS (SQL Server Reporting Services) reports, allowing users to access and visualize data efficiently in an on-premises environment. This application is designed to serve multiple clients, offering a user-friendly and responsive interface.

## 2. Installation Instructions
Follow these steps to set up the Infeed700 application on your local machine:

### 2.1 Choose an Installation Directory
#### 2.1.1 Decide where you want the application files to be installed
This could be a specific directory, such as `C:\Program Files\Infeed700` or a custom folder like `C:\MyProjects\Infeed700`. If the directory doesn't exist, you may need to create it.

#### 2.1.2 Move and Extract the ZIP Folder
Copy or move the ZIP folder to your chosen directory. Right-click on the ZIP folder and select "Extract All..." (or use an extraction tool if you have one). Choose the extraction location (if prompted) and confirm.

#### 2.2.3 Navigate to the Extracted Folder
Once unzipped, navigate to the extracted folder where you’ll find the necessary files to proceed with the installation or setup.

## 3. Installing Python
Navigate to the directory where the Infeed700Plus files are located, find the folder named `python_offline_installer`, and inside, locate the Python 3.12.5 offline installer (`python-3.12.5-amd64`). Double-click the installer and follow the steps to complete the installation.

If you need to install from the internet, follow these steps:
1. Visit the official Python website: [https://www.python.org/downloads](https://www.python.org/downloads)
2. Download Python version 3.12.5 (make sure to choose the installer compatible with your operating system).
3. Run the installer and check the box that says "Add Python to PATH" during the installation.

## 4. Run the Setup Batch File
Navigate to the Infeed700 directory, locate the `setup.bat` file, right-click it, and select "Run as administrator." A CMD window will appear, and it will begin installing all necessary libraries in offline mode. Ensure that the folder named `libs` is in the same directory as `setup.bat`.

## 5. Access the Application
After running the setup, the Streamlit application should automatically launch in your web browser. If it doesn't, you can manually open your browser and go to [http://localhost:8501](http://localhost:8501).

By following these steps, you will have the Infeed700 application set up and running on your local machine. If you encounter any issues, please refer to the troubleshooting section of this documentation or seek assistance from your IT support team.

---

## 6. Setting Up Automatic Background Execution of Streamlit Apps on Windows
This section explains how to set up your Streamlit applications to run in the background automatically when your PC starts or restarts using a batch script and the Windows Task Scheduler.

### 6.1 Step 1: Create a Batch Script to Run Streamlit Apps in the Background
#### 6.1.1 Creating the .bat file
Open a text editor (such as Notepad) and paste the following content (only follow this step if there is no `setup.bat` file in the directory):

```bat
@echo off
start /b "" streamlit run main.py --server.port 8501
start /b "" streamlit run functions/documentation.py --server.port 8502
exit
```

## 6.1.2 Save the file
Save this file as `run_streamlit_apps.bat` in the same directory where all the `.py` files are located.

## 6.2 Step 2: Set Up Task Scheduler to Run the Script at Startup
Once the `.bat` file is created, we will configure the Windows Task Scheduler to run it automatically at startup.

### 6.2.1 Opening the Task Scheduler
Press `Win + R` to open the Run dialog.  
Type `taskschd.msc` and press Enter to open Task Scheduler.

## 6.3 Step 3: Create a New Task
In Task Scheduler, click "Create Task."  
In the General tab:  
- Name the task, e.g., "Run Streamlit Apps."
- Select "Run whether user is logged on or not."
- Check "Do not store password" if you want the task to run without needing a password.

## 6.4 Step 4: Configure Triggers
In the Triggers tab, click "New."  
In the "Begin the task" dropdown, select "at startup."  
Click "OK" to save the trigger.

## 6.5 Step 5: Configure Actions
In the Actions tab, click "New."  
Select "Start a program" from the Action dropdown.  
In "Program/script," click Browse and select the `run_streamlit_apps.bat` file.  
In "Start in (optional)," enter the full directory path where the `.bat` and `.py` files are located. For example:  
- Program/script: `C:\path\to\your\directory\run_streamlit_apps.bat`
- Start in: `C:\path\to\your\directory\`

Click "OK" to save the action.

## 6.6 Step 6: Test the Task
In Task Scheduler, right-click on the task and select "Run" to test whether the Streamlit apps start correctly.  
Restart your computer to confirm that the task runs automatically on startup.

**Notes:**
- If the `.bat` file and the Python scripts are in the **same directory**, you don't need to specify the full paths to the `.py` files in the script.
- Make sure to enter the correct path in the **Start in (optional)** field when creating the task in **Task Scheduler** to ensure it runs in the correct directory.

---

## 7. Required Software and Libraries
To run the batch file you provided, the following software and libraries are required:

### 7.1 Python
- **Version:** Python should be installed on the machine. The batch file checks if Python is installed using `python --version`. You can download Python from [https://www.python.org/](https://www.python.org/).
- **Ensure Python is in your system's PATH**: So it can be accessed from the command line. If it's not, the batch file will fail with the error message "Python is not installed or not found in the PATH."

### 7.2 pip (Python Package Installer)
- **Installed with Python**: Pip comes installed by default with Python. It is used to install the `.whl` files (Python wheel files) found in the `libs` folder. The command `pip install --no-index --find-links="%LIBS_DIR%" "%%f"` is used to install these dependencies without fetching from the internet.

### 7.3 Pre-downloaded Python Dependencies (.whl files)
- You need to have pre-downloaded Python wheel (`.whl`) files for all required packages stored in the `libs` directory. These `.whl` files must be compatible with your Python version and system architecture.

### 7.4 Streamlit
- **Python package**: The batch file assumes that your project uses Streamlit, a Python-based web application framework. One of the `.whl` files in the `libs` folder should be `streamlit`. You will also need any other dependencies required by your Streamlit application (e.g., `pandas`, `numpy`, etc.).
- **Running the Streamlit application**: The command `streamlit run main.py` is used to start the Streamlit app, so Streamlit must be installed in the environment.

---

## 8 Python Naming Conventions and Best Practices
This document outlines Python naming conventions and best practices for naming files, functions, variables, classes, and constants in Python projects. Following these conventions ensures consistency, readability, and maintainability across your codebase. The guidelines are based on **PEP 8**, the official style guide for Python code.

### 8.1 Summary of Naming Conventions

| Entity          | Naming Convention               | Example                  |
|-----------------|---------------------------------|--------------------------|
| Files           | snake_case                      | `database_connection.py` |
| Functions       | snake_case()                    | `fetch_data()`           |
| Variables       | snake_case                      | `total_weight`           |
| Classes         | PascalCase                      | `UserProfile`            |
| Constants       | UPPERCASE_WITH_UNDERSCORES      | `MAX_RETRIES`            |
| Private Methods | underscore_prefix()             | `_connect_to_database()` |

---

## 9 App
Content related to the app.
[https://streamlit.io/](https://streamlit.io/)
