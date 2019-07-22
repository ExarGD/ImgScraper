#!/usr/bin/python

import os, requests, re, shutil
import click
from requests_html import HTMLSession


@click.command()
@click.option("--url")
def get_page(url):
    url = url.rstrip("/")
    session = HTMLSession()
    r = session.get(url)
    r.html.render()  # Attempt to bypass some scraping protection by rendering page for JS execution
    content = str(r.content)  # Get all data
    relative_urls = re.findall(
        r"(?:[/|.|\w|\s|-])*\.(?:jpg|jpeg|gif|png)(?:[\w])*", content
    )  # I can parse raw html for images
    links = img_links(r.html)  # And i can use cheats =P
    links = "\n".join(links)
    print(links)
    # print("\n".join(relative_urls))
    print("Found " + str(len(links)) + " images!")
    # for img in relative_urls:
    # download_img(url, img)
    print("DONE! Downloaded " + str(len(links)) + " images!")


def img_links(html):
    def gen():
        for img_link in html.find("img"):
            try:
                src = img_link.attrs["src"].strip()
                if (
                    src.endswith("jpg")
                    or src.endswith("jpeg")
                    or src.endswith("png")
                    or src.endswith("gif")
                ):
                    yield src
            except KeyError:
                pass

    return set(gen())


def process_url(url, img_url):
    img_url = img_url.strip('"')
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
        print("Downloading " + img_name)
        with open("images/" + img_name, "wb") as out_img:
            shutil.copyfileobj(response.raw, out_img)  # Save image
        del response
        print("OK")
    else:
        print(response.status_code + "\nFAILED TO DOWNLOAD IMAGE: " + result_img_url)


if __name__ == "__main__":
    get_page()
