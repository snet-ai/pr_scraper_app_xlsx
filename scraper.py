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



# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Generate a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"My Organization"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mydomain.com"),
])
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .sign(private_key, hashes.SHA256())
)

# Write our certificate out to disk.
with open("mycert.pem", "wb") as f:
    f.write(cert.public_bytes(Encoding.PEM))

# Write our key out to disk.
with open("mykey.pem", "wb") as f:
    f.write(private_key.private_bytes(
        Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption())
    )

# Function to scrape the website
def scrape_website(url):
  session = Session()

  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
  }
  
  response = requests.get(url, verify='mycert.pem')
  if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    print(html_content)
    # Find all the <th> elements with the specified style
    th_elements = soup.find_all('th', style='border: 1px solid black;')
    print(f"Found {len(th_elements)} <th> elements.")
    # Iterate over the <th> elements
    for th in th_elements:
      # Find the <a> element within the <th>
      a = th.find('a')
      if a:
        # Get the href attribute value
        href = a['href']
        # Download the file
        download_url = url + href
        response = requests.get(download_url)
        if response.status_code == 200:
          # Save the file
          file_name = href.split('/')[-1]
          with open('./site_to_scraper/' + file_name, 'wb') as file:
            file.write(response.content)
          print(f"File {file_name} downloaded successfully.")
        else:
          print(f"Failed to download file {href}. Status code: {response.status_code}")
  else:
    print(f"Failed to scrape the website. Status code: {response.status_code}")

# Scrape the website
scrape_website('https://financa.gov.al/pagesat-e-kryera-2024-2/')