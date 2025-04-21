from nersc_api_client import NERSCApiClient


def main():
    print("Hello from nersonic!")

    client = NERSCApiClient()
    client.connect()

    if client.connected:
        print("Connected to NERSC API.")
    else:
        print("Failed to connect to NERSC API.")

    response = client.get("account/projects")
    if response.status_code == 200:
        print("Request successful.")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Text: {response.text}")


if __name__ == "__main__":
    main()
