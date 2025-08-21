import requests

# API endpoint URL where the file is available
file_url = "http://192.168.1.46:5003"

# Making the GET request to fetch the file
response = requests.get(file_url, stream=True)  # 'stream=True' to download large files in chunks

# Check if the request was successful
if response.status_code == 200:
    # Open a local file for writing the downloaded content
    with open("downloaded_file.txt", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):  # Download in chunks
            if chunk:  # Filter out keep-alive new chunks
                file.write(chunk)
    print("File downloaded successfully.")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
