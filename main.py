import os
import pandas as pd
import os
import pandas as pd
from requests import Session
import requests
from bs4 import BeautifulSoup
import ssl
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding
from datetime import datetime, timedelta


# Direktoria ku do ruhen file-t Excel
directory = './site_to_scraper'

# Emri që kërkohet
search_name = 'test'

# File i ri Excel ku do të ruhen rezultatet
output_file = 'rezultatet.xlsx'

# DataFrame bosh për të ruajtur rezultatet
result_df = pd.DataFrame()

# Funksioni për të lexuar file Excel dhe për të kërkuar për emrin specifik
def search_excel_files(directory, search_name):
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            file_path = os.path.join(directory, filename)
            try:
                excel_file = pd.ExcelFile(file_path)
                for sheet in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_name).any(), axis=1)]
                    if not filtered_df.empty:
                        filtered_df['File'] = filename
                        filtered_df['Sheet'] = sheet
                        global result_df
                        result_df = pd.concat([result_df, filtered_df], ignore_index=True)
            except Exception as e:
                print(f"An error occurred while processing the file {filename}: {e}")

# Kërkoni në file-t Excel dhe ruani rezultatet
search_excel_files(directory, search_name)

# Ruani rezultatet në një file të ri Excel
if not result_df.empty:
    result_df.to_excel(output_file, index=False)
    print(f"Rezultatet u ruajtën në file-n {output_file}")
else:
    print("Nuk u gjetën rezultate për emrin specifik.")