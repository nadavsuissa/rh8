# Imports
import sqlite3
from xml.etree import ElementTree
import os.path
import requests
import xmltodict

# Api
URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Bill()?$filter=SubTypeID%20eq%2054&$expand=KNS_BillInitiators"
# Create DB File
db = sqlite3.connect('knsbill.db')
# Get Api and Parse XML TO PYTHON DIC
response = requests.get(URL)
response.raise_for_status()
xml_data = xmltodict.parse(response.content)  # Parse
xmlnodes = xml_data.get('feed').get('entry')  # Root is feed and nodes are entry
cursor = db.cursor()
# Create TABLE - Other Fields ar not is use - Look
cursor.execute('''
CREATE TABLE bills(
             BillID INTEGER PRIMARY KEY,
             KnessetNum INTEGER,
             Name TEXT,
             PrivateNumber INTEGER,
             StatusID INTEGER,
             Number INTEGER
             )''')
db.commit() # Commit Creation
cursor.execute("DROP TABLE bills")
db.commit()# Commit Drop
# Call Get From Api
# Go Over Nodes That Contain data
for bill_data in xmlnodes:
    info = bill_data.get('content').get('m:properties')
    # Get Data
    a = int(info['d:BillID']['#text'])
    b = str(info['d:Name'])
    c = int(info['d:KnessetNum']['#text'])
    d = int(info['d:StatusID']['#text'])
    e = int(info['d:PrivateNumber']['#text'])
    # Insert Data
    cursor.execute('''INSERT INTO bills(
                       BillID,Name,KnessetNum,StatusID,PrivateNumber)
                       VALUES(?,?,?,?,?)''', (a, b, c, d, e))
    print("Data Entered")
    # Commit EveryTime
    db.commit()
    # Finnaly Close
db.close()
