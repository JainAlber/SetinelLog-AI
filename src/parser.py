import pandas as pd
import io
import re

def parse_logs(file_content, file_extension):
    """
    Parses CSV or line-separated Syslog file into a standardized Pandas DataFrame.
    Standardized columns: timestamp, source_ip, user, action, status, severity, country
    """
    if file_extension == 'csv':
        df = pd.read_csv(io.BytesIO(file_content))
    else:
        # Advanced Regex for Syslog/Auth logs (Simplified for this project)
        # Pattern: timestamp source_ip user action status severity country
        lines = file_content.decode('utf-8').splitlines()
        data = []
        for line in lines:
            # Matches space-delimited values, potentially in quotes
            parts = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
            if len(parts) >= 7:
                data.append(parts[:7])
            elif len(parts) >= 5:
                # Fill missing columns with defaults if necessary
                row = parts[:5] + ["Low", "Unknown"]
                data.append(row)
        
        df = pd.DataFrame(data, columns=['timestamp', 'source_ip', 'user', 'action', 'status', 'severity', 'country'])
    
    # Ensure timestamp is a datetime object for rule processing
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df
