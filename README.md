🗑️ Bitrix24 Activity Deletion Tool
This Python script allows you to safely and selectively delete CRM activities from Bitrix24 based on a specific SUBJECT field, using a list of activity IDs from a TXT or Excel file. It includes confirmation prompts and error logging for safety.

⚠️ Warning
This operation is irreversible. Use with caution. Make sure you have a backup or are working in a test environment before proceeding.

📦 Features
Deletes Bitrix24 CRM activities via REST API using a webhook

Filters deletions by exact SUBJECT match

Accepts TXT or Excel files with a list of activity IDs

Error handling with logs saved to delete_errors.log

Simple GUI file picker using tkinter

🛠️ Requirements
Python 3.7+

requests

tkinter (standard in most Python installations)

pandas (only if using Excel input files)

openpyxl (recommended for .xlsx file parsing)

Install missing dependencies with:

bash
Copy
Edit
pip install requests pandas openpyxl
🚀 How to Use
Clone or download this repository.

Run the script:

bash
Copy
Edit
python deleteactivities.py
Follow the prompts:

Confirm the warning by typing Yes

Enter your Bitrix24 webhook URL

Choose a file with activity IDs (TXT or Excel)

Enter the exact SUBJECT of activities to delete

The script will fetch each activity, compare its SUBJECT, and delete only those that match.

📂 File Format
TXT: One activity ID per line.

Excel (.xlsx): Activity IDs in the first column.

📄 Example
TXT:

Copy
Edit
12345
67890
13579
Excel:

Activity ID
12345
67890
13579

🧾 Logs
Errors and failed deletions will be recorded in:

lua
Copy
Edit
delete_errors.log
📜 License
MIT License. Use at your own risk.
