# src/api/stockx_client.@property
import requests
import logging
import os

BASE_URL = "https://stockx.com/api"

HEADERS = {
    "authority": "stockx.com",
    "method": "GET",
    "scheme": "https",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://stockx.com/",
    "sec-ch-ua": '"Chromium";v="123", "Not:A-Brand";v="8"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

def search_product(query):
    """Search Stockx products by keyword."""
    url = f"{BASE_URL}/browse?_search={query}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_product_details(product_slug):
    ''''Fetch detajiled product info by slug (e.g., air-jordan-1-chicago).'''
    url = f"{BASE_URL}/products/{product_slug}?includes=market"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def extract_market_data(product_json):
    """Parse our the key market stats you care about."""
    market_data = product_json["Product"]["market"]
    return {
        "lowest_ask": market_data.get("lowestAsk"),
        "highest_bid": market_data.get("highestBid"),
        "last_sale": market_data.get("lastSale"),
        "sales_last_72_hours": market_data.get("salesLast72Hours"),
        "volatility": market_data.get("vlatility"),
        "sku": product_json["Products"]["styleId"],
        "name": product_json["Product"]["title"]
    }


def working_example(query, limit=10):
    """Search StockX for products by keword.

        Args: 
            query (str): Prroduct name or keyword (e.g. 'Jordan 1 Chicago')
            limit (int): Max number of results to return

        Returns: 
            list[dict]: List of products with basic metadata
        """
    url = f"{BASE_URL}/browse?_search={query}&dataType=product"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        for product in data.get("Products", [])[:limit]:
            reslults.append({
                "title": product.get("title"),
                "slug": product.get("urlKey"),
                "style_id": product.get("styleId"),
                "retail_price": product.get("retailPrice"),
                "brand": product.get("brand"),
                "category": product.get("category"),
                "market": product.get("market", {}),
            })

        return results

    except requests.RequestException as e:
        logging.error(f"StockX search failed: {e}")
        return []

if __name__ == "__main__":
    query = "air jordan 1 chicago"
    products = working_example(query)

    for product in products:
        print(f"{product['title']} (SKU: {product['style_id']})")
        print(f"  Last Sale: {product['market'].get('lastSale')}")
        print(f"  Lowest Ask: {product['market'].get('lowestAsk')}")
        print(f"  Highest Bid: {product['market'].get('highestBid')}")
        print("-" * 40)

