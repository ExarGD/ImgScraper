#!/usr/bin/python

import os, requests, re, shutil
import click
from requests_html import HTMLSession  # Cheat, helps to render pages for javascript


@click.command()
@click.option("--url")
def get_img(url):
    try:
        url = url.rstrip("/")
    except AttributeError:
        print("URL is not specified")
        exit()
    session = HTMLSession()
    r = session.get(url)
    content = str(r.content)  # Get all data
    relative_urls = re.findall(
        r"(?:[/|.|\w|\s|-])*\.(?:jpg|jpeg|gif|png)(?:[\w])*", content
    )  # I can parse raw html for images
    re_count = len(relative_urls)
    # print("\n".join(links))
    print("\n".join(relative_urls))
    print("Found " + str(re_count) + " images!")
    for img in relative_urls:
        download_img(url, img)
    print("DONE! Downloaded images: " + str(re_count))


def process_url(url, img_url):
    img_url = img_url.strip()
    result_url = img_url
    if img_url.startswith("http"):
        return result_url
    else:
        if img_url.startswith("//"):
            result_url = "https:" + img_url
            # print(result_url)
        else:
            if img_url.startswith("/"):
                result_url = url + img_url
            else:
                print("Invalid image URL!" + result_url)
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
        print("Downloading " + result_img_url)
        with open("images/" + img_name, "wb") as out_img:
            shutil.copyfileobj(response.raw, out_img)  # Save image
        del response
        print("OK")
    else:
        print(response.status_code + "\nFAILED TO DOWNLOAD IMAGE: " + result_img_url)


if __name__ == "__main__":
    get_img()
