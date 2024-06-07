# zensuite

A Zendesk and NetSuite Integration Script. 

## Overview

This script, `main.py`, integrates Zendesk and NetSuite by automating the processing of uncategorized Zendesk tickets. It retrieves tickets, searches for related items in NetSuite using UPC codes, updates tickets, and applies macros based on specific conditions.

## Business Use Case

In customer service operations, handling and categorizing tickets efficiently is crucial. This script helps by:

- Automatically fetching uncategorized Zendesk tickets.
- Searching for corresponding items in NetSuite based on UPC codes found in the tickets.
- Updating the tickets in Zendesk with relevant UPC codes.
- Applying specific macros to tickets based on item availability and ticket content.

By automating these tasks, the script reduces manual effort, ensures tickets are processed consistently, and improves overall efficiency.

## Features

- **Fetch Uncategorized Tickets**: Retrieves all open uncategorized tickets from Zendesk.
- **Get Ticket Information**: Fetches detailed information for each ticket.
- **Search NetSuite Items**: Searches for items in NetSuite using UPC codes.
- **Update Zendesk Tickets**: Updates the UPC field in Zendesk tickets.
- **Apply Macros**: Applies appropriate macros to tickets based on item availability and ticket subject.

## Configuration

The script requires the following environment variables to be set:

- `ZENDESK_API_URL`: Base URL for Zendesk API.
- `ZENDESK_API_KEY`: API key for accessing Zendesk.
- `NETSUITE_API_URL`: Base URL for NetSuite API.
- `NETSUITE_API_KEY`: API key for accessing NetSuite.
- `UPC_FIELD_ID`: Custom field ID for the UPC in Zendesk tickets.
- `DROPSHIP_MACRO_ID`: Macro ID for "Special Order: Dropship".
- `FRAME_ONLY_MACRO_ID`: Macro ID for "Supplied: Frame Only".
- `SUPPLIED_IDENTITY_MACRO_ID`: Macro ID for "Supplied: Identity".
- `SPECIAL_ORDER_IDENTITY_MACRO_ID`: Macro ID for "Special Order: Identity".

## Installation

1. Clone the repository.
2. Install the required Python library:
   ```bash
   pip install requests
   ```
3. Set the required environment variables in your system.

## Usage

1. Ensure all necessary environment variables are set.
2. Run the script:
   ```bash
   python main.py
   ```

## Logging

The script uses Python's built-in logging module to log information and errors during execution. Logs can help in troubleshooting issues and understanding the script's flow.

## License

This project is licensed under the MIT License.
