import requests
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from environment variables
ZENDESK_API_URL = os.getenv("ZENDESK_API_URL")
ZENDESK_API_KEY = os.getenv("ZENDESK_API_KEY")
NETSUITE_API_URL = os.getenv("NETSUITE_API_URL")
NETSUITE_API_KEY = os.getenv("NETSUITE_API_KEY")
UPC_FIELD_ID = os.getenv("UPC_FIELD_ID")
DROPSHIP_MACRO_ID = os.getenv("DROPSHIP_MACRO_ID")
FRAME_ONLY_MACRO_ID = os.getenv("FRAME_ONLY_MACRO_ID")
SUPPLIED_IDENTITY_MACRO_ID = os.getenv("SUPPLIED_IDENTITY_MACRO_ID")
SPECIAL_ORDER_IDENTITY_MACRO_ID = os.getenv("SPECIAL_ORDER_IDENTITY_MACRO_ID")

def get_uncategorized_tickets():
    url = f"{ZENDESK_API_URL}/search.json?query=type:ticket status:open"
    headers = {
        "Authorization": f"Bearer {ZENDESK_API_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tickets = response.json().get('results', [])
        return [ticket['id'] for ticket in tickets if 'uncategorized' in ticket['tags']]
    except requests.RequestException as e:
        logger.error(f"Error fetching uncategorized tickets: {e}")
        return []

def get_ticket_info(ticket_id):
    url = f"{ZENDESK_API_URL}/tickets/{ticket_id}.json"
    headers = {
        "Authorization": f"Bearer {ZENDESK_API_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching ticket info: {e}")
        return None

def search_netsuite_item(upc):
    headers = {
        "Authorization": f"Bearer {NETSUITE_API_KEY}"
    }
    params = {
        "q": upc
    }
    try:
        response = requests.get(NETSUITE_API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error searching NetSuite item: {e}")
        return None

def update_zendesk_ticket(ticket_id, upc):
    url = f"{ZENDESK_API_URL}/tickets/{ticket_id}.json"
    headers = {
        "Authorization": f"Bearer {ZENDESK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "ticket": {
            "custom_fields": [
                {
                    "id": UPC_FIELD_ID,
                    "value": upc
                }
            ]
        }
    }
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error updating Zendesk ticket: {e}")
        return None

def apply_macro(ticket_id, macro_id):
    url = f"{ZENDESK_API_URL}/tickets/{ticket_id}/macros/{macro_id}/apply.json"
    headers = {
        "Authorization": f"Bearer {ZENDESK_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error applying macro {macro_id} to ticket {ticket_id}: {e}")
        return None

def process_ticket(ticket_id):
    ticket_info = get_ticket_info(ticket_id)
    if not ticket_info:
        logger.error(f"Failed to get ticket info for ticket {ticket_id}, skipping.")
        return
    
    ticket = ticket_info['ticket']
    subject = ticket.get('subject', '').lower()
    upc = ticket.get('upc')
    if not upc:
        logger.info(f"No UPC found in ticket {ticket_id}.")
        return

    netsuite_item = search_netsuite_item(upc)
    if not netsuite_item:
        logger.error(f"Failed to search NetSuite item for UPC {upc}, skipping ticket {ticket_id}.")
        return
    
    in_stock = netsuite_item.get('in_stock', False)

    if "frame only" in subject or "to view" in subject:
        if in_stock:
            apply_macro(ticket_id, FRAME_ONLY_MACRO_ID)
            logger.info(f"Applied 'Supplied: Frame Only' macro to ticket {ticket_id}.")
        else:
            apply_macro(ticket_id, DROPSHIP_MACRO_ID)
            logger.info(f"Applied 'Special Order: Dropship' macro to ticket {ticket_id}.")
    elif "identity optical" in subject or "iol" in subject:
        if in_stock:
            apply_macro(ticket_id, SUPPLIED_IDENTITY_MACRO_ID)
            logger.info(f"Applied 'Supplied: Identity' macro to ticket {ticket_id}.")
        else:
            apply_macro(ticket_id, SPECIAL_ORDER_IDENTITY_MACRO_ID)
            logger.info(f"Applied 'Special Order: Identity' macro to ticket {ticket_id}.")
    
    if in_stock:
        result = update_zendesk_ticket(ticket_id, upc)
        if result:
            logger.info(f"Successfully updated Zendesk ticket {ticket_id} with UPC {upc}.")
        else:
            logger.error(f"Failed to update Zendesk ticket {ticket_id}.")
    else:
        logger.info(f"Item with UPC {upc} is not in stock for ticket {ticket_id}.")

def main():
    uncategorized_ticket_ids = get_uncategorized_tickets()
    for ticket_id in uncategorized_ticket_ids:
        process_ticket(ticket_id)

# Example usage
if __name__ == "__main__":
    main()
