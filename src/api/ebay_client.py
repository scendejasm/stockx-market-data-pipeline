import requests
import logging
from urllib.parse import quote

# Replace with your actural ebay App ID 
EBAY_APP_ID = "YOUR_APP_ID"
FINDING_API_URL = "https://svcs.ebay.com/services/search/FindingService/v1"

# HEADERS = {
#     "X-EBAY-SOA-OPERATION-NAME": "findItemsByKeywords",
#     "X-EBAY-SOA-SERVICE-VERSION": "1.13.0",
#     "X-EBAY-SOA-SECURITY-APPNAME": EBAY_APP_ID,
#     "X-EBAY-SOA-RESPONSE-DATA-FORMAT": "JSON",
# }

def search_product(query, limit=10):
    """Search ebay for products by keyword.

        Args:
            query (str): Product name or keywrord (e.g. 'Jordan 1 Chcago')
            limit (int): Maxx number of results to return
        Returns:
            list[dict]: List of products with basic metadata
    """
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.13.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST_PAYLOAD": "",
        "keywords": query,
        "paginationInput.entriesPerPage": limit,
    }

    try:
        response = requests.get(FINDING_API_URL, params=params, timeout=10) # *Removed : headers=HEADERS
        response.raise_for_status()
        data = response.json()
        itmes = data.get("findItemsByKeywordsResponse", [])[0].get("searchResult", [])[0].get("item", [])

        results = []
        for item in items:
            results.append({
                "title": item.get("title", [None])[0],
                "price": item.get("sellingStatus",[{}])[0].get("currentPrice", [{}])[0].get("__value__"),
                "currency": item.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("@currencyId"),
                "condition": item.get("condition", [{}])[0].get("conditionDisplayName", [None])[0],
                "location": item.get("location", [None])[0],
                "viewItemUrl": item.get("viewItemURL", [None])[0], 
            })

        return results
    
    except Exception as e:
        logging.error(f"eBay search failed: {e}")
        return []

if __name__ == "__main__":
    from pprint import pprint 
    sneakers = search_product("Jordan 1 Chicago", limit=5)
    pprint(sneakers)
