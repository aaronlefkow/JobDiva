from base64 import b64decode
import json
import os
import tkinter as tk
from tkinter import filedialog

# Converts Base64 data inside of JSON and turns it into a PDF
# Job Diva API https://api.jobdiva.com/jobdiva-api.html#/DataRetrieval/CandidateApplicationRecordsUsingGET
# DataRetrieval -> GET CandidateApplicationRecords
# /api/bi/CandidateApplicationRecords

#------------------------------------------------STORE JSON FILECONTENT AS A VARIABLE------------------------------------------------#

#prompt for JSON File
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
basename = os.path.basename(file_path)

# Opening JSON file
f = open(basename)
data = json.load(f)

# Define the Base64 string of the PDF file
b64 = data["data"][0]["FILECONTENT"]
  
# Closing file
f.close()

#-------------------------------------------------------Convert Base64 to PDF-------------------------------------------------------#

# Decode the Base64 string, making sure that it contains only valid characters
bytes = b64decode(b64, validate=True)

# Perform a basic validation to make sure that the result is a valid PDF file
# Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
# Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
if bytes[0:4] != b'%PDF':
  raise ValueError('Missing the PDF file signature')

# Write the PDF contents to a local file
new_filename = basename.replace(".json","")
f = open(new_filename + '.pdf', 'wb')
f.write(bytes)
f.close()
