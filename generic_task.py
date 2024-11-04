import configparser

import click

import task0

# consts
config = configparser.ConfigParser()
with open('config.cfg') as config_file:
    config.read_file(config_file)
poligon_base_url = config.get("URLS", "poligon_aidevs")

@click.group()
def group():
    pass


def _day0_task():
    task0.post_answer(base_url = poligon_base_url, api_key = config.get("KEYS", "API_KEY"))

@group.command()
def day0_task():
    _day0_task()

if __name__ == "__main__":
    group()
