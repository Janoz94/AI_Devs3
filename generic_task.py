import configparser

import click

import task0
import task_s1e1
import task_s1e2
import task_s1e3
import task_s1e5

# consts
config = configparser.ConfigParser()
with open("config.cfg") as config_file:
    config.read_file(config_file)


@click.group()
def group():
    pass


def _day0_task():
    task0.post_answer(
        base_url=config.get("URLS", "poligon_aidevs"),
        api_key=config.get("KEYS", "AI_DEVS"),
    )


def _s1e1_task():
    task_s1e1.solve_task(
        base_url=config.get("URLS", "robots_system"),
        ai_devs_key=config.get("KEYS", "AI_DEVS"),
        openai_key=config.get("KEYS", "OPEN_AI"),
        xyz_agents_username=config.get("XYZ_AGENTS", "username"),
        xyz_agents_pass=config.get("XYZ_AGENTS", "password"),
        system_prompt=config.get("PROMPTS", "xyz_agents_year"),
    )


def _s1e2_task():
    task_s1e2.solve_task(
        base_url=config.get("URLS", "robots_system"),
        ai_devs_key=config.get("KEYS", "AI_DEVS"),
        openai_key=config.get("KEYS", "OPEN_AI"),
        system_prompt=config.get("PROMPTS", "xyz_agents_facts"),
    )


def _s1e3_task():
    task_s1e3.solve_task(
        base_url=config.get("URLS", "aidevs_agency"),
        ai_devs_key=config.get("KEYS", "AI_DEVS"),
        openai_key=config.get("KEYS", "OPEN_AI"),
        system_prompt=config.get("PROMPTS", "centrala_answer_and_fill"),
    )


def _s1e5_task():
    task_s1e5.solve_task(
        agency_url=config.get("URLS", "aidevs_agency"),
        local_url=config.get("URLS", "local_host"),
        ai_devs_key=config.get("KEYS", "AI_DEVS"),
        system_prompt=config.get("PROMPTS", "anonimize_data"),
    )


@group.command()
def day0_task():
    _day0_task()


@group.command()
def s1e1_task():
    _s1e1_task()


@group.command()
def s1e1_task():
    _s1e1_task()


@group.command()
def s1e2_task():
    _s1e2_task()


@group.command()
def s1e3_task():
    _s1e3_task()


@group.command()
def s1e5_task():
    _s1e5_task()


if __name__ == "__main__":
    group()
