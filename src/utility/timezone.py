# src/utility/timezone.py
from __future__ import annotations

import os
import logging
from datetime import datetime, date
from dotenv import load_dotenv

# For Python 3.9+ you could use zoneinfo (built-in) instead of pytz
# from zoneinfo import ZoneInfo
import pytz

# -----------------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------------
load_dotenv()

# Default to Dhaka time zone if not set in .env
_TZ_ENV = os.getenv("TIMEZONE", "Asia/Dhaka")

# -----------------------------------------------------------------------------
# Configure local timezone with fallback
# -----------------------------------------------------------------------------
try:
    LOCAL_TZ = pytz.timezone(_TZ_ENV)
    # If using zoneinfo in the future:
    # LOCAL_TZ = ZoneInfo(_TZ_ENV)
except Exception as exc:
    logging.getLogger(__name__).warning(
        "Invalid TIMEZONE '%s' in environment; falling back to Asia/Dhaka. Error: %s",
        _TZ_ENV,
        exc
    )
    LOCAL_TZ = pytz.timezone("Asia/Dhaka")
    # Or if using zoneinfo:
    # LOCAL_TZ = ZoneInfo("Asia/Dhaka")

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def now_local_dt_time() -> datetime:
    """
    Return the current time as a timezone-aware datetime in the configured local timezone.
    """
    return datetime.now(LOCAL_TZ) # 2025-10-04 13:40:15+06:00

def today_local_dt() -> date:
    """
    Return the current date in the configured local timezone.
    """
    return now_local_dt_time().date() # 2025-10-04