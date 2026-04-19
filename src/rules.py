import pandas as pd

def detect_brute_force(df):
    alerts = []
    failed_logins = df[df['status'].str.lower() == 'failed']
    
    for ip in failed_logins['source_ip'].unique():
        ip_data = failed_logins[failed_logins['source_ip'] == ip].sort_values('timestamp')
        # Check window: > 5 failures in 5 minutes
        for i in range(len(ip_data) - 5):
            window = ip_data.iloc[i : i + 6]
            time_diff = (window['timestamp'].max() - window['timestamp'].min()).total_seconds()
            if time_diff <= 300:
                alerts.append({
                    "timestamp": window['timestamp'].max(),
                    "user": window['user'].iloc[0],
                    "type": "Brute Force Detection",
                    "details": f"6 failed logins from {ip} in {time_diff:.1f}s",
                    "severity": "High"
                })
                break # Avoid multiple alerts for the same window
    return alerts

def detect_geo_shift(df):
    alerts = []
    success_logins = df[df['status'].str.lower() == 'success'].sort_values('timestamp')
    
    for user in success_logins['user'].unique():
        user_data = success_logins[success_logins['user'] == user]
        for i in range(len(user_data) - 1):
            row1 = user_data.iloc[i]
            row2 = user_data.iloc[i+1]
            
            if row1['country'] != row2['country']:
                time_diff = (row2['timestamp'] - row1['timestamp']).total_seconds()
                if time_diff <= 3600: # 1 hour
                    alerts.append({
                        "timestamp": row2['timestamp'],
                        "user": user,
                        "type": "Geo-Shift Detected",
                        "details": f"Success from {row1['country']} then {row2['country']} in {time_diff/60:.1f}m",
                        "severity": "High"
                    })
    return alerts

def detect_privilege_escalation(df):
    alerts = []
    df_sorted = df.sort_values(['user', 'timestamp'])
    
    for user in df_sorted['user'].unique():
        user_data = df_sorted[df_sorted['user'] == user]
        for i in range(len(user_data) - 1):
            row1 = user_data.iloc[i]
            row2 = user_data.iloc[i+1]
            
            if row1['action'] == 'password_change' and row2['action'] == 'sudo':
                time_diff = (row2['timestamp'] - row1['timestamp']).total_seconds()
                if time_diff <= 120: # 2 minutes
                    alerts.append({
                        "timestamp": row2['timestamp'],
                        "user": user,
                        "type": "Privilege Escalation",
                        "details": f"sudo command executed {time_diff}s after password_change",
                        "severity": "Critical"
                    })
    return alerts

def get_all_alerts(df):
    return detect_brute_force(df) + detect_geo_shift(df) + detect_privilege_escalation(df)
