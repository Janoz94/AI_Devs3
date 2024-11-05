import configparser

import click

import task0
import task_s1e1

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
        base_url = config.get("URLS", "robots_system"),
        ai_devs_key = config.get("KEYS", "AI_DEVS"),
        openai_key = config.get("KEYS", "OPEN_AI"),
        xyz_agents_username = config.get("XYZ_AGENTS", "username"), 
        xyz_agents_pass = config.get("XYZ_AGENTS", "password"),
        system_prompt = config.get("PROMPTS", "xyz_agents")
    )


@group.command()
def day0_task():
    _day0_task()


@group.command()
def s1e1_task():
    _s1e1_task()


if __name__ == "__main__":
    group()
