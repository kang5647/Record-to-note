import requests
import sys
import base64
# Get the file path from the command-line arguments
# file_path = sys.argv[1]

file_path = sys.argv[1]
# Open the file in binary mode and read its contents
with open(file_path, 'rb') as file:
    mp3_data = base64.b64encode(file.read())

print(file_path)
# Set the API endpoint and headers
url = 'https://x11o87hbkc.execute-api.ap-southeast-1.amazonaws.com/stage_1/'
headers = {'Content-Type': 'multipart/form-data'}

# Set the data payload with the file binary and file name
data = {'mp3Data': mp3_data.decode(
    'utf-8'), 'mp3Name': file_path}
# Send the POST request with the file binary and file name as the data
response = requests.post(url, headers=headers, data=data)

# Print the response from the API
print(response.text)
