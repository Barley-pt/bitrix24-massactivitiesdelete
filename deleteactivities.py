import requests
import time
import traceback
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def log_error(message, exception=None, log_file="delete_errors.log"):
    with open(log_file, "a") as log:
        log.write("ERROR: " + message + "\n")
        if exception:
            log.write(traceback.format_exc() + "\n")

def delete_activity(webhook_url, activity_id):
    try:
        delete_endpoint = webhook_url.rstrip("/") + "/crm.activity.delete"
        response = requests.post(delete_endpoint, json={"id": activity_id})
        data = response.json()

        if response.status_code != 200 or data.get("result") != True:
            raise Exception(f"Failed to delete ID {activity_id}. Response: {data}")
        print(f"🗑️ Deleted activity ID: {activity_id}")
        return True
    except Exception as e:
        log_error(f"Failed to delete activity ID: {activity_id}", e)
        print(f"❌ Failed to delete ID: {activity_id}")
        return False

def fetch_activity(webhook_url, activity_id):
    try:
        get_endpoint = webhook_url.rstrip("/") + "/crm.activity.get"
        response = requests.post(get_endpoint, json={"id": activity_id})
        data = response.json()
        return data.get("result", {})
    except Exception as e:
        log_error(f"Failed to fetch activity ID: {activity_id}", e)
        return {}

def choose_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a TXT or Excel File",
        filetypes=[("Text files", "*.txt"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    return file_path

def main():
    print("⚠️ WARNING: This operation will permanently delete CRM activities in Bitrix24.")
    print("Make sure the input file is correct and matches your intention.")
    print("❗ If misused, it can cause irreversible data loss.")
    confirm = input("Type 'Yes' to continue: ")
    if confirm.strip().lower() != "yes":
        print("🛑 Aborted by user.")
        return

    webhook_url = input("🔗 Enter your Bitrix24 webhook URL: ").strip()
    print("📂 Please choose the TXT or Excel file containing the activity IDs...")
    file_path = choose_file_dialog()
    if not file_path:
        print("🛑 No file selected. Exiting.")
        return

    subject_to_match = input("🔍 Enter the exact SUBJECT text to match: ").strip()

    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    if file_path.endswith(".xlsx"):
        import pandas as pd
        try:
            df = pd.read_excel(file_path)
            activity_ids = df.iloc[:, 0].dropna().astype(int).tolist()
        except Exception as e:
            print("❌ Failed to read Excel file.")
            log_error("Failed to read Excel file", e)
            return
    else:
        with open(file_path, "r") as file:
            activity_ids = [line.strip() for line in file if line.strip().isdigit()]

    print(f"\n🚀 Loaded {len(activity_ids)} IDs. Checking SUBJECT and deleting matches...\n")

    deleted_count = 0
    for activity_id in activity_ids:
        activity = fetch_activity(webhook_url, activity_id)
        if not activity:
            continue
        subject = activity.get("SUBJECT", "")
        if subject.strip().lower() == subject_to_match.strip().lower():
            success = delete_activity(webhook_url, activity_id)
            if success:
                deleted_count += 1
        else:
            print(f"⏭️ Skipped ID {activity_id} (SUBJECT: '{subject}')")

        time.sleep(0.4)

    print(f"\n✅ Finished. Total activities deleted: {deleted_count} out of {len(activity_ids)}.")

if __name__ == "__main__":
    main()
