#!/usr/bin/python

import os, requests, re, shutil
import click
from tqdm import tqdm
from requests_html import HTMLSession


@click.command()
@click.option("--url")
def get_page(url):
    url = url.rstrip("/")
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    content = str(r.content)  # Get all data
    # print(r.html.text)
    relative_urls = re.findall(
        r"(?:[/|.|\w|\s|-])*\.(?:jpg|jpeg|gif|png)(?:[\w])*", content
    )
    # print("\n".join(not_relative_urls))
    print("\n".join(relative_urls))
    matches_list = relative_urls
    print(matches_list)
    for img in tqdm(matches_list):
        # img = process_url(url, img)
        print(img)
        download_img(url, img)
    print("DONE!")


def process_url(url, img_url):
    img_url = img_url.strip('"')
    result_url = img_url
    if img_url.startswith("http"):
        return result_url
    else:
        if img_url.startswith("//"):
            result_url = "https:" + img_url
            print(result_url)
        else:
            if img_url.startswith("/"):
                result_url = url + img_url
                print(result_url)
            else:
                print("Invalid image URL!")
    return result_url


def get_name(img_url):
    return str(re.findall(r"[^\/]+$", img_url)).strip("[']\"")


def download_img(url, img_url):
    result_img_url = process_url(url, img_url)
    response = requests.get(result_img_url, stream=True)
    if response.status_code == 200:
        os.makedirs(
            "images/", exist_ok=True
        )  # Create directory for images, skip if exists
        img_name = get_name(img_url)
        print(img_name)
        with open("images/" + img_name, "wb") as out_img:
            shutil.copyfileobj(response.raw, out_img)  # Save image
        del response
    else:
        print(response.status_code + "\nFAILED TO DOWNLOAD IMAGE: " + result_img_url)
        print(response.status_code)


if __name__ == "__main__":
    get_page()

