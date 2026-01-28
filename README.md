# Kitchen Inventory Bot

A personal kitchen inventory management discord bot that lets you track groceries and pantry items via chat commands.


## Google Service Account Setup (Required for Google Sheets access)

This project uses a Google service account to access a Google Sheet.

### Step 1: Create `service_account.json`

1. Go to the **[Google Cloud Console](https://console.cloud.google.com/)**. 
2. Select (or create) a project.
3. Navigate to **IAM & Admin → Service Accounts**.
4. Click **Create Service Account**.
5. Give it a name and click **Create and Continue**.
6. Assign the required roles for this project (Editor).
7. Click **Done**.
8. Navigate to the **Manage Keys** option in the **Actions** menu.
9. Click **Add Key → Create new key**.
10. Select **JSON** and download the key file.
11. Rename the downloaded file to `service_account.json`.
12. Place it in the root directory of this project.

> **Do not commit `service_account.json`**

### Step 2: Share the Google Sheet with the Service Account

The service account acts like a user and must be given access to the Google Sheet.

1. Open `service_account.json` in a text editor.
2. Copy the value of the `client_email` field  
   (it will look like `something@your-project.iam.gserviceaccount.com`).
3. Open the Google Sheet you want the bot to access.
4. Click **Share**.
5. Paste the service account email into the share dialog.
6. Grant **Editor** access.
7. Click **Send**.

The service account should now has access to the sheet.
