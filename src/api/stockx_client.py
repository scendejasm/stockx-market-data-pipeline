# src/api/stockx_client.@property
from fastapi import APIRouter, Request, HTTPException
import requests
import logging
import httpx
import os

router = APIRouter()

X_API_KEY = os.getenv("X_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
BASE_URL = "https://api.stockx.com"
VERSION = "v2"
ENDPOINT = "catalog"
# HEADERS = {
#     "Authorization": f"Bearer {token}",
#     "Accept": "application/json",
#     "User-Agent": "FastAPI-StockX-Client"
# }


@router.get("/authorize")
async def test_authorize(request: Request):
    token = request.session.get("ACCESS_TOKEN")
    if not token:
        return {"error": "Badges, we don't need no stinking Badges"}
    return {"token": token}

@router.get("/search")
async def search(query: str, request: Request):
    return await search_products(query, request)


async def search_products(query: str, request: Request) -> dict:
    """Search Stockx products by keyword."""
    token = request.session.get("ACCESS_TOKEN")
    print(f"jwt: {token}")
    if not token:
        raise HTTPException(status_code=404, detail="No access token found in session")

    headers = {
        "Authorization": f"Bearer {token}",
        # "Accept": "application/json",
        "x-api-key": X_API_KEY
    }
    print(f"KEY: {X_API_KEY}")
    url = f"{BASE_URL}/{VERSION}/{ENDPOINT}/search?query={query}"
    print(f"URL: {url}")
    print(f"Query: {query}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Serch Failed: {response.text}")
    
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

