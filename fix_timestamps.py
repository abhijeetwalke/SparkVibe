#!/usr/bin/env python3
# Read the file
with open('combined_app.py', 'r') as f:
    content = f.read()

# Fix 1: Method 1 timestamp conversion
old1 = 'timestamp = earnings_date_info[0]\n                    earnings_date = pd.Timestamp(datetime.fromtimestamp(timestamp))'
new1 = '''timestamp = earnings_date_info[0]
                    # Handle both second and millisecond timestamps
                    if timestamp > 1e10:  # If timestamp is in milliseconds
                        timestamp = timestamp / 1000
                    earnings_date = pd.Timestamp(datetime.fromtimestamp(timestamp))'''
content = content.replace(old1, new1)

# Fix 2: Method 2 timestamp conversion  
old2 = 'elif isinstance(earnings_date, (int, float)):\n                            earnings_date = pd.Timestamp(datetime.fromtimestamp(earnings_date))'
new2 = '''elif isinstance(earnings_date, (int, float)):
                            # Handle both second and millisecond timestamps
                            if earnings_date > 1e10:  # If timestamp is in milliseconds
                                earnings_date = earnings_date / 1000
                            earnings_date = pd.Timestamp(datetime.fromtimestamp(earnings_date))'''
content = content.replace(old2, new2)

# Fix 3: Method 4 timestamp conversion
old3 = 'if next_earnings and isinstance(next_earnings, (int, float)):\n                        earnings_date = pd.Timestamp(datetime.fromtimestamp(next_earnings))'
new3 = '''if next_earnings and isinstance(next_earnings, (int, float)):
                        # Handle both second and millisecond timestamps
                        if next_earnings > 1e10:  # If timestamp is in milliseconds
                            next_earnings = next_earnings / 1000
                        earnings_date = pd.Timestamp(datetime.fromtimestamp(next_earnings))'''
content = content.replace(old3, new3)

# Write the fixed content back
with open('combined_app.py', 'w') as f:
    f.write(content)

print('Successfully fixed timestamp conversion issues!')
