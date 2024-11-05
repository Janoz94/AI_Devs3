import requests
from typing import Optional

from openai import OpenAI

import helpers


def get_verification_question(base_url: str, ai_devs_key: str) -> str:
    url = base_url + "/verify"
    headers = {"Content-Type": "application/json"}
    payload = {"msgID": 0, "text": "READY"}

    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def get_verification_answer(question: str, openai_key: str, system_prompt: str) -> str:
    client = OpenAI(
        api_key=openai_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": question,
            },
        ],
        model="gpt-4o-mini",
    )

    ai_answer = chat_completion.choices[0].message.content

    return ai_answer


def send_verification_answer(base_url: str, msg_id: int, answer: str):
    url = base_url + "/verify"
    headers = {"Content-Type": "application/json"}
    payload = {"msgID": msg_id, "text": answer}

    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        print(response.json()["text"])
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def solve_task(base_url: str, ai_devs_key: str, openai_key: str, system_prompt: str):

    question_stacked = get_verification_question(
        base_url=base_url, ai_devs_key=ai_devs_key
    )

    msg_id = int(question_stacked["msgID"])
    question = question_stacked["text"]

    answer = get_verification_answer(
        question=question, openai_key=openai_key, system_prompt=system_prompt
    )

    print(f"question: {question}")
    print(f"msg_id: {msg_id}")
    print(f"answer: {answer}")
    send_verification_answer(base_url=base_url, msg_id=msg_id, answer=answer)
