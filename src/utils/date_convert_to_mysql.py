from datetime import datetime

def convert_date_format_to_store_sql(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')


def parse_datetime(date_string):
    formats = [
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ',  # Format with fractional seconds
        '%Y-%m-%dT%H:%M:%S.%f',   # Format with fractional seconds without 'Z'
        '%Y-%m-%dT%H:%M:%S%z',    # Format with timezone
        '%Y-%m-%dT%H:%M:%SZ',     # Format without fractional seconds
        '%Y-%m-%dT%H:%M:%S',      # Format without fractional seconds and 'Z'
        '%Y-%m-%d %H:%M:%S'       # Common format without 'T'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date format for '{date_string}' not recognized.")


