import re
import ast
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from collections import Counter, defaultdict
from datetime import datetime

log_data = []

fortio_status_codes = []

#Reading data from file
with open('api_log.log', 'r') as file:
    #Looping through each line of the file
    for line in file:

        #Creating regex to read only from API log results, not from Fortio
        api_match = re.search(r"INFO - (\{.*\})", line)

        #Creating regex to read only from Fortio results, not from the API
        fortio_match = re.search(r'"[A-Z]+ .* HTTP/1.1" (\d{3})', line)

        #If a match for the API log result was found in the current line
        if api_match:
            try:
                api_entry = ast.literal_eval(api_match.group(1))
                log_data.append(api_entry)
            
            except(ValueError, SyntaxError):
                continue
        
        #If a match for the Fortio log result was found in the current line
        if fortio_match:
            try:
                status_code = int(fortio_match.group(1))
                fortio_status_codes.append(status_code)

            except(ValueError, SyntaxError):
                continue
                

#Organizing data for API analysis
api_endpoints = [api_entry['endpoint'] for api_entry in log_data if 'endpoint' in api_entry]
api_methods = [api_entry['method'] for api_entry in log_data if 'method' in api_entry]
api_status_codes = [api_entry['http-status'] for api_entry in log_data if 'http-status' in api_entry]


#Counting code frequencies 
status_counts = Counter(fortio_status_codes)

#Plotting fortio http status codes
plt.figure(figsize=(8, 5))
plt.bar(status_counts.keys(), status_counts.values(), width=0.1 , color='green')
plt.title('HTTP Status Codes from Fortio Logs')
plt.xlabel('HTTP Status Code')
plt.ylabel('Request Count')
plt.xticks(list(status_counts.keys()))
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#Time series per method
time_series = defaultdict(list)
for api_entry in log_data:
    if 'date' in api_entry and 'method' in api_entry:
        timestamp = datetime.strptime(api_entry['date'], "%Y-%m-%d, %H:%M:%S")
        time_series[api_entry['method']].append(timestamp)


#---- Plotting ----
#Requests per endpoint
plt.figure(figsize=(10, 5))
Counter_endpoints = Counter(api_endpoints)
plt.bar(Counter_endpoints.keys(), Counter_endpoints.values())
plt.xticks(rotation=45)
plt.title("Requests per Endpoint")
plt.xlabel("Endpoint")
plt.ylabel("Request Count")
plt.tight_layout()
plt.show()
plt.close()


#Status code distribution
plt.figure(figsize=(6, 4))
Counter_status = Counter(api_status_codes)
plt.pie(Counter_status.values(), labels=Counter_status.keys(), autopct='%1.1f%%', startangle=90)
plt.title("HTTP Status Code Distribution")
plt.tight_layout()
plt.show()
plt.close()


#GET vs. POST over time on different graphics
fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
for i, (method, timestamps) in enumerate(time_series.items()):
    timestamps.sort()
    axs[i].plot(timestamps, range(len(timestamps)), label=method, color='blue' if method == 'GET' else 'orange')
    axs[i].set_ylabel("Cumulative")
    axs[i].legend()

axs[1].set_xlabel("Time")
fig.suptitle("GET vs POST Over Time")
plt.tight_layout()
plt.show()
plt.close()


#Requests per minute (load duration)
requests_per_minute = defaultdict(int)
for api_entry in log_data:
    if 'date' in api_entry:
        timestamp = datetime.strptime(api_entry['date'], "%Y-%m-%d, %H:%M:%S")
        rounded_time = timestamp.replace(second=0)
        requests_per_minute[rounded_time] += 1

times = sorted(requests_per_minute)
counts = [requests_per_minute[t] for t in times]

plt.figure(figsize=(12, 5))
plt.plot(times, counts, marker='o')
plt.title("Requests Per Minute (Load Duration)")
plt.xlabel("Time (HH:MM)")
plt.ylabel("Request Count")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()
