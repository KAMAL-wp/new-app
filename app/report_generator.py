# This file handles generating a downloadable CSV report
# It takes the list of summaries and saves them as a CSV file

import csv
import os

def generate_csv(summaries):
    # This function creates a CSV file with all document summaries
    # summaries = list of dictionaries with 'filename' and 'summary' keys
    
    # Save the CSV file inside the 'static' folder
    # Flask serves files from the static folder automatically
    path = "static/report.csv"
    
    # Create the static folder if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    # Open the CSV file for writing
    with open(path, 'w', newline='', encoding='utf-8') as f:
        
        # Create a CSV writer with column headers
        writer = csv.DictWriter(f, fieldnames=["filename", "summary"])
        
        # Write the header row (filename, summary)
        writer.writeheader()
        
        # Write one row for each document summary
        writer.writerows(summaries)
    
    # Return the path of the saved CSV file
    return path