# Imports
import sqlite3
from xml.etree import ElementTree
import os.path

import requests
import xmltodict

# Api
URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Bill()?$filter=SubTypeID%20eq%2054&$expand=KNS_BillInitiators"
db = sqlite3.connect('knsbill.db')
response = requests.get(URL)
response.raise_for_status()
xml_data = xmltodict.parse(response.content)
xmlnodes = xml_data.get('feed').get('entry')  # Root is feed and nodes are entry
cursor = db.cursor()
cursor.execute('''
CREATE TABLE bills(
             BillID INTEGER PRIMARY KEY,
             KnessetNum INTEGER,
             Name TEXT,
             PrivateNumber INTEGER,
             StatusID INTEGER,
             Number INTEGER
             )''')
db.commit()
cursor.execute("DROP TABLE bills")
db.commit()
# Call Get From Api

for bill_data in xmlnodes:
    info = bill_data.get('content').get('m:properties')
    a = int(info['d:BillID']['#text'])
    b = str(info['d:Name'])
    c = int(info['d:KnessetNum']['#text'])
    d = int(info['d:StatusID']['#text'])
    e = int(info['d:PrivateNumber']['#text'])
    cursor.execute('''INSERT INTO bills(
                       BillID,Name,KnessetNum,StatusID,PrivateNumber)
                       VALUES(?,?,?,?,?)''', (a, b, c, d, e))
    print("Data Entered")
    db.commit()
db.close()
