import requests
from typing import Optional

from bs4 import BeautifulSoup
from openai import OpenAI

import helpers


def get_question(base_url: str) -> Optional[str]:
    try:
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        keyword = ""
        paragraph = soup.find("p", id="human-question")

        if paragraph and ":" in paragraph.get_text():
            year = paragraph.get_text().split(sep=":")[1]
            print(year)
            return year
        else:
            print("Error: No paragraph found with id'")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")


def get_answer(question: str, api_key: str, system_prompt: str) -> Optional[str]:
    client = OpenAI(
        api_key=api_key,
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

    predicted_year = chat_completion.choices[0].message.content

    try:
        year_as_int = int(predicted_year)
        print(year_as_int)
        return year_as_int
    except ValueError:
        print("The value is not an year.")
        return None


def post_task_answer(
    base_url: str, xyz_agents_username: str, xyz_agents_pass: str, year: int
):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "username": xyz_agents_username,
        "password": xyz_agents_pass,
        "answer": year,
    }

    response = requests.post(base_url, json=body, headers=headers)
    if response.ok:
        print(response.text)
    else:
        raise Exception(
            f"Sending answer failed with following error: {response.json()}"
        )


def solve_task(
    base_url: str,
    ai_devs_key: str,
    openai_key: str,
    xyz_agents_username: str,
    xyz_agents_pass: str,
    system_prompt: str,
):
    question = get_question(base_url=base_url)

    year = get_answer(
        question=question, api_key=openai_key, system_prompt=system_prompt
    )

    post_task_answer(
        base_url=base_url,
        xyz_agents_username=xyz_agents_username,
        xyz_agents_pass=xyz_agents_pass,
        year=year,
    )
