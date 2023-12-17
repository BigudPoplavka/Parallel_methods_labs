import os
from urllib.parse import urlparse, urlunparse
from urllib.request import (
    urlopen, urlparse, urlunparse, urlretrieve)
import requests
from bs4 import BeautifulSoup as bs
import shutil
from progress.bar import IncrementalBar
import concurrent.futures


def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc) and bool(parsed_url.scheme)


def download_images(img_tags, url, path):
    img_attr_keys = ["src", "data-srcset", "data-src", "data-fallback-src"]
    img_extensions = ['png', 'jpg', 'gif', 'jpeg', 'svg']
    src_attr, link = '', ''

    bar = IncrementalBar('Progress: ', max=len(img_tags))

    for img_tag in img_tags:
            for attr_name in img_attr_keys:
                if not img_tag.attrs.get(attr_name):
                    continue
                else:
                    src_attr = attr_name
                    break

            img_src = img_tag[src_attr][2:] if img_tag[src_attr].startswith('..') else img_tag[src_attr]

            if img_src.startswith("https://"):
                link = img_src
            else:
                link = f"https://{url}{img_src}"
    
            if any([link.endswith(ext) for ext in img_extensions]):
                filename = link.split("/")[-1]
                outpath = os.path.join(path, filename)

                try:
                    response = requests.get(link, stream=True).raw

                    with open(outpath, "wb") as f:
                        response.decode_content = True
                        shutil.copyfileobj(response, f)
                        bar.next()

                except Exception as e:
                    print(f"Error! --- {e}\n")
            else:
                print(f"\nError! --- Link {url} is unsupported\n")
    bar.finish()

    return


def parse_data_from_page(url):
    print(f"\n{'-'*20}\nStart downloading: {url}\n")

    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(urlunparse(parsed_url))
        soup = bs(urlopen(url), features='lxml')
        images_folder_path = "Images_" + filename[:-5]

        if not os.path.exists(images_folder_path):
            os.mkdir(images_folder_path)

        img_tags = soup.find_all("img")
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            download_images(img_tags, parsed_url.netloc, images_folder_path)

    except Exception as e:
        print(f"Error! --- {e}\n")


def read_urls(path):
    with open(path, "r") as f:
        url_list =  [line.strip() for line in f if is_valid_url(line.strip())]
    return url_list


def start_threads(url_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [(executor.submit(parse_data_from_page, url), url) for url in url_list]

    for future in futures:
        print(f"Download complete: {future[1]}")

    print("Done")
    print("Adding images to archive")

    shutil.make_archive('images', 'zip', os.getcwd())
    print("Done")


def main():
    urls_txt_path = ("URLs.txt")

    if os.path.exists(urls_txt_path) and os.path.isfile(urls_txt_path):
        url_list = read_urls(urls_txt_path)        
        
        start_threads(url_list)
    else:
        raise FileNotFoundError(f"Ошибка! Файл {urls_txt_path} не найден")


main()
