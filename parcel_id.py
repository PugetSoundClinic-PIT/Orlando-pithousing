import requests
import json

def fetch_parcel_ids(page):
    # Replace URL for different property type

    # Residential HOA
    url = f"https://ocpa-mainsite-afd-standard.azurefd.net/api/PropertyUseSearch/GetSearchInfoByPropertyType?useCode=0019,0049,0119,0499&jurisdiction=&zipCode=&valueParameter=&minValue=1&acreage=&page={page}&size=100&sortBy=ParcelID&sortDir=ASC"
    '''
    Condo url: https://ocpa-mainsite-afd-standard.azurefd.net/api/PropertyUseSearch/GetSearchInfoByPropertyType?useCode=0400,0401,0450,0471,0472,0473,0474,0550&jurisdiction=&zipCode=&valueParameter=&minValue=1&acreage=&page={page}&size=100&sortBy=ParcelID&sortDir=ASC
    Multi-family url: https://ocpa-mainsite-afd-standard.azurefd.net/api/PropertyUseSearch/GetSearchInfoByPropertyType?useCode=0175,0800,0805,0806,0812,0813,0814,0822,0823,0824&jurisdiction=&zipCode=&valueParameter=&minValue=1&acreage=&page={page}&size=100&sortBy=ParcelID&sortDir=ASC
    Single-family: https://ocpa-mainsite-afd-standard.azurefd.net/api/PropertyUseSearch/GetSearchInfoByPropertyType?useCode=0100,0101,0102,0103,0104,0105,0106,0120,0121,0122,0123,0130,0131,0135,0140,0150,0181,0182,0200,0201&jurisdiction=&zipCode=&valueParameter=&minValue=1&acreage=&page={page}&size=100&sortBy=ParcelID&sortDir=ASC
    Vacant Residential Land: https://ocpa-mainsite-afd-standard.azurefd.net/api/PropertyUseSearch/GetSearchInfoByPropertyType?useCode=0000,0001,0004,0020,0030,0031,0035,0040&jurisdiction=&zipCode=&valueParameter=&minValue=1&acreage=&page={page}&size=100&sortBy=ParcelID&sortDir=ASC

    '''
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'ocpa-mainsite-afd-standard.azurefd.net',
        'Origin': 'https://ocpaweb.ocpafl.org',
        'Referer': 'https://ocpaweb.ocpafl.org/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
        'x-user-key': 'a5250bb5-c321-4926-a966-9e907f560f31',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        properties = response.json()
        parcel_ids = [property["parcelId"] for property in properties]
        return parcel_ids
    else:
        print(f"Failed to retrieve data from page {page}, status code: {response.status_code}")
        return []

def main():
    all_parcel_ids = []
    for page in range(1, 2):  # Adjust range for more pages
                              # 151 pages for Residential HOA
                              # 504 pages for Condo
                              # 2 pages for Multi-family
                              # 3435 pages for Single-family
                              # 225 pages for Vacant Residential Land
        parcel_ids = fetch_parcel_ids(page)
        all_parcel_ids.extend(parcel_ids)

    # Writing fetched Parcel IDs to a JSON file
    with open('/Users/minhanhtruong/Desktop/Orlando-pithousing/parcel_ids.json', 'w') as json_file:
        json.dump(all_parcel_ids, json_file)

    print(f"Total fetched Parcel IDs written to parcel_ids.json: {len(all_parcel_ids)}")

if __name__ == "__main__":
    main()
