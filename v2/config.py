"""
Configuration for v2 Institutional Footprint Detector

Store sensitive keys here. In production, use environment variables instead.
"""
import os

# Alpha Vantage API Key
# Free tier: 25 requests/day
# Get your key at: https://www.alphavantage.co/support/#api-key
ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "6IID07YUQ344LUDG")

# API Base URL
ALPHAVANTAGE_BASE_URL = "https://www.alphavantage.co/query"
