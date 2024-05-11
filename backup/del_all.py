import requests

def delete_data(data_id):
    url = f"https://bus-tracker.ru/api/v1/statistics/data/{data_id}"
    headers = {'accept': 'application/json'}
    response = requests.delete(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"Object with data_id {data_id} deleted successfully.")
    else:
        print(f"Failed to delete object with data_id {data_id}. Status code: {response.status_code}")

def main():
    # Assuming the data_id range is from 2 to 745
    for data_id in range(2, 746):
        delete_data(data_id)

if __name__ == "__main__":
    main()

