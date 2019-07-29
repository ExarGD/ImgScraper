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
    r.html.render()  # Attempt to bypass some scraping protection by rendering page for JS execution
    links = img_links(r.html)  # And i can use cheats =P
    link_count = len(links)
    # print("\n".join(links))
    print("Found " + str(link_count) + " images!")
    for img in links:
        download_img(url, img)
    print("DONE! Downloaded images: " + str(link_count))


# This function uses requests-html functionality to search for a tags
def img_links(html):
    def gen():
        for img_link in html.find("img"):
            try:
                src = img_link.attrs["src"].strip()
                print("SRC: " + src)
                if (
                    src.endswith("jpg")
                    or src.endswith("jpeg")
                    or src.endswith("png")
                    or src.endswith("gif")
                ):
                    yield src
            except requests.exceptions.MissingSchema:
                print("Invalid URL " + img_link)
                print("Terminating")

    return set(gen())


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
