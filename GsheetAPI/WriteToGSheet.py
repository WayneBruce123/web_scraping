import pandas as pd
from Google import Create_Service

# Replace with the path to your Excel file
excel_file = 'Products.xlsx'

# Load the Excel data into a Pandas dataframe
df = pd.read_excel(excel_file)

# Convert the dataframe to a list of lists
rngData = df.values.tolist()

# Google Sheet Id
gsheet_id = '1Uz8azuQY3VgFml57cGBJR4w5kkfY_luppd8S5Oq_jsA'
CLIENT_SECRET_FILE = 'GsheetAPI/client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

# Append the data to the new spreadsheet
response = service.spreadsheets().values().append(
    spreadsheetId=gsheet_id,
    valueInputOption='RAW',
    range='Sheet1!A1',
    body=dict(
        majorDimension='ROWS',
        values=rngData
    )
).execute()

