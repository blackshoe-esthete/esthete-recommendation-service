import requests

def send_get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청이 실패할 경우 예외 발생
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Failed to fetch data from", url)
        print("Error:", e)
        return None
    
def send_post_request(url, data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # 요청이 실패할 경우 예외 발생
        print("Data successfully sent to", url)
    except requests.exceptions.RequestException as e:
        print("Failed to send data to", url)
        print("Error:", e)