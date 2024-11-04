import requests

import helpers

def get_task(base_url: str) -> dict:
    url = base_url + "/dane.txt"
    response = requests.post(url)
    if response.ok:
        return response.text.splitlines()
    else:
        raise Exception(f"Request failed: {response.text}")


def post_answer(base_url: str, api_key: str):
    url = base_url + "/verify"
    headers = {"Content-Type": "application/json"}
    answer = get_task(base_url = base_url)
    payload = helpers.PayloadBody(
        api_key = api_key,
        task_name = "POLIGON",
        answer = answer 
    )
    print(answer)
    response = requests.post(url, json=payload.to_dict(), headers=headers)
    if response.ok and response.json()["code"] == 0:
        print(f"Answer has been successfully sent with message: {response.json()}")
    else:
        raise Exception(f"Sending answer failed with following error: {response.json()}")
