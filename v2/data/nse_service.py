"""
NSE Service - Fetches data directly from NSE using nsepython

This service provides access to official NSE data for:
- Board meetings (including for financial results/earnings)
"""
from nsepython import nse_eq
from datetime import datetime
from typing import Optional, List, Dict, Any
import pandas as pd

def fetch_next_earnings_date_from_nse(symbol: str) -> Optional[datetime]:
    """
    Fetch the next earnings date from NSE board meetings.
    
    Args:
        symbol: NSE stock symbol (e.g., "RELIANCE")
    
    Returns:
        datetime of the next board meeting for financial results, or None
    """
    print(f"\n[DEBUG][NSE] Fetching board meetings for {symbol}")
    try:
        # Fetch detailed equity data from nsepython
        data = nse_eq(symbol)
        
        # Log the raw response
        print(f"[DEBUG][NSE] Raw response from nse_eq('{symbol}'):")
        print(data)

        corporate_info = data.get('corporate', {})
        board_meetings = corporate_info.get('boardMeetings', [])

        if not board_meetings:
            print("[DEBUG][NSE] No board meetings found.")
            return None

        future_meetings = []
        for meeting in board_meetings:
            purpose = meeting.get('purpose', '').lower()
            date_str = meeting.get('purposedate')

            if not date_str:
                continue

            # Check if the purpose is related to earnings/financial results
            if "financial results" in purpose or "earnings" in purpose or "audited" in purpose or "unaudited" in purpose:
                try:
                    meeting_date = pd.to_datetime(date_str)
                    # Check if the meeting is in the future
                    if meeting_date >= pd.Timestamp.now().normalize():
                        future_meetings.append(meeting_date)
                except Exception as e:
                    print(f"[DEBUG][NSE] Error parsing date '{date_str}': {e}")
        
        if not future_meetings:
            print("[DEBUG][NSE] No future board meetings for financial results found.")
            return None
        
        # Return the earliest future meeting date
        next_meeting_date = min(future_meetings)
        print(f"[DEBUG][NSE] Found next earnings-related board meeting: {next_meeting_date}")
        return next_meeting_date

    except Exception as e:
        print(f"Error fetching data from nsepython for {symbol}: {e}")
        return None
