#!/usr/bin/python

import sys, getopt, requests
import click
from tqdm import tqdm
from time import sleep
import re


@click.command()
# def method(url):
#     for i in tqdm(range(5)):  # Progress bar
#         click.echo(url)


@click.option("--url")
def get_page(url):
    r = requests.get(url)
    content = str(r.content)
    matches = re.findall(r'"([^"]+(png|jpg))"', content)
    # matches = "\n".join(matches)

    print(matches)
    # print(r.text)


if __name__ == "__main__":
    get_page()

