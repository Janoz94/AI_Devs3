import requests
from typing import Optional
import json

from sympy import sympify
from sympy.core.sympify import SympifyError
from openai import OpenAI

import helpers


def get_verification_question(base_url: str, ai_devs_key: str) -> str:
    url = base_url + f"/data/{ai_devs_key}/json.txt"

    response = requests.post(url)
    if response.ok:
        return response.text
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def generate_subjson(json_to_parse: str) -> str:
    data = json.loads(json_to_parse)

    filtered_items = []

    for item in data["test-data"]:
        if "test" in item:
            filtered_items.append(item)

    sub_json = {"test-data": filtered_items}

    return str(sub_json)


def get_answers_and_swap_questionmarks(
    json_with_questions: str, openai_key: str, system_prompt: str
) -> str:
    client = OpenAI(
        api_key=openai_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json_with_questions},
        ],
        model="gpt-4o",
    )

    ai_answer = chat_completion.choices[0].message.content

    return ai_answer


def swap_answers(original_json: str, answers_json: str, ai_devs_key: str) -> dict:
    original_json = original_json.replace("'", '"')
    answers_json = answers_json.replace("'", '"')
    answers_json_data = json.loads(answers_json)
    original_json_data = json.loads(original_json)

    test_mapping = {}
    for item in answers_json_data["test-data"]:
        if "test" in item:
            nested_question = item["test"]["q"]
            nested_answer = item["test"]["a"]

            test_mapping[nested_question] = nested_answer

    for item in original_json_data["test-data"]:
        if "test" in item:
            question = item["test"]["q"]
            item["test"]["a"] = test_mapping[question]

        math_result = solve_math_operation(item["question"])
        if math_result != None and item["answer"] != math_result:
            item["answer"] = int(math_result)

    original_json_data["apikey"] = ai_devs_key

    return original_json_data


def solve_math_operation(question: str) -> Optional[int]:
    try:
        expression = sympify(question)
        result = expression.evalf()
        return result
    except SympifyError:
        return None


def post_answer(base_url: str, api_key: str, answer: str):
    url = base_url + "/verify"
    headers = {"Content-Type": "application/json"}
    payload = helpers.PayloadBody(api_key=api_key, task_name="JSON", answer=answer)
    response = requests.post(url, json=payload.to_dict(), headers=headers)
    if response.ok and response.json()["code"] == 0:
        print(f"Answer has been successfully sent with message: {response.json()}")
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def solve_task(base_url: str, ai_devs_key: str, openai_key: str, system_prompt: str):
    downloaded_json = get_verification_question(
        base_url=base_url, ai_devs_key=ai_devs_key
    )

    sub_json = generate_subjson(json_to_parse=downloaded_json)

    filled_answers = get_answers_and_swap_questionmarks(
        json_with_questions=str(sub_json),
        openai_key=openai_key,
        system_prompt=system_prompt,
    )

    final_answers_json = swap_answers(
        original_json=downloaded_json,
        answers_json=filled_answers,
        ai_devs_key=ai_devs_key,
    )

    post_answer(base_url=base_url, api_key=ai_devs_key, answer=final_answers_json)
