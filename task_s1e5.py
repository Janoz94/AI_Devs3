import requests
from typing import Optional
import json

import helpers


def get_agents_data(base_url: str, ai_devs_key: str):
    url = base_url + f"/data/{ai_devs_key}/cenzura.txt"

    response = requests.post(url)
    if response.ok:
        return response.text
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def censor_data(base_url: str, system_prompt: str, data: str) -> Optional[str]:
    url = base_url + "/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "gemma2:2b",
        "prompt": f"[SYSTEM] {system_prompt} [USER] {data}",
        "stream": False,
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()["response"]
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def post_answer(base_url: str, api_key: str, answer: str):
    url = base_url + "/verify"
    headers = {"Content-Type": "application/json"}
    payload = helpers.PayloadBody(api_key=api_key, task_name="CENZURA", answer=answer)
    response = requests.post(url, json=payload.to_dict(), headers=headers)
    if response.ok and response.json()["code"] == 0:
        print(f"Answer has been successfully sent with message: {response.json()}")
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def solve_task(agency_url: str, local_url: str, ai_devs_key: str, system_prompt: str):
    agents_data = get_agents_data(base_url=agency_url, ai_devs_key=ai_devs_key)

    censored_data = censor_data(
        base_url=local_url, system_prompt=system_prompt, data=agents_data
    )

    post_answer(base_url=agency_url, api_key=ai_devs_key, answer=censored_data)
