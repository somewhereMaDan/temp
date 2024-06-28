import requests
from bs4 import BeautifulSoup

def search_510k_device(device_name, limit=10):
    base_url = 'https://api.fda.gov/device/510k.json'
    params = {
        'search': f'device_name:"{device_name}"',
        'limit': limit
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def fetch_device_details(k_number):
    details_url = f'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={k_number}'
    response = requests.get(details_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch device details: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    reg_number_tag = soup.find(string='Regulation Number').find_next('a')
    
    if reg_number_tag:
        reg_number = reg_number_tag.text.strip()
        return reg_number
    else:
        raise Exception(f"Regulation number not found for 510(k) Number: {k_number}")

def fetch_cfr_text(regulation_number):
    url = f'https://www.ecfr.gov/cgi-bin/text-idx?SID=0ec70c0b155b7c84a33b4b6abbbf3e0d&mc=true&node=se21.8.{regulation_number}'

    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch CFR text: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Debug: Print the raw HTML content
    print("Raw HTML content:")
    print(soup.prettify())
    
    # Attempt to find the CFR text
    section_div = soup.find('div', {'class': 'section'})
    
    if section_div:
        cfr_text = section_div.get_text(strip=True)
        return cfr_text
    else:
        raise Exception("CFR text section not found")

def main():
    device_name = "STAINLESS STEEL SURGICAL SUTURE"
    try:
        # Step 1: Search for the device
        data = search_510k_device(device_name)
        
        if 'results' in data and len(data['results']) > 0:
            for entry in data['results']:
                print(f"Device Name: {entry['device_name']}")
                print(f"510(k) Number: {entry['k_number']}")
                
                # Step 2: Fetch the regulation number
                regulation_number = fetch_device_details(entry['k_number'])
                print(f"Regulation Number: {regulation_number}")
                
                # Step 3: Fetch the CFR text based on the regulation number
                try:
                    cfr_text = fetch_cfr_text(regulation_number.replace('.', ''))
                    print(f"CFR Text for Regulation Number {regulation_number}:")
                    print(cfr_text)
                except Exception as e:
                    print(f"Could not fetch CFR text automatically: {e}")
                    print(f"Please manually access the CFR text for regulation number {regulation_number} at https://www.ecfr.gov/")
                print("------------------------------------------------")
        else:
            print(f"No results found for device name: {device_name}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()