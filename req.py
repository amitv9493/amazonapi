import requests
import pathlib
import time


def fetch_and_save(url, filesize, **kwargs):
    index = urls.index(url)
    print(f"Getting content for {url} (filesize: {filesize[index]} bytes)")
    start_time = time.time()

    response = requests.get(url, **kwargs)

    content = response.content
    print(f"Got content for {url}")

    filename = url.split("/")[-1] + ".mp4"

    with open(f"req/{filename}", "wb") as f:
        f.write(content)
        print(f"Saved file {filename}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")


def bulk_download(urls, file_sizes, **kwargs):
    for url in urls:
        fetch_and_save(url=url, filesize=file_sizes, **kwargs)


if __name__ == "__main__":
    urls =[
            "https://bit.ly/1GB-testfile",
            "https://link.testfile.org/ihDc9s",
            "https://link.testfile.org/DNnCeI",
            "https://link.testfile.org/bNYZFw",
            "https://link.testfile.org/aXCg7h",
            "https://link.testfile.org/DTrMLS",
            "https://link.testfile.org/lfSv97",
            "https://link.testfile.org/AY6sjl",
            "https://link.testfile.org/iK7sKT",
            "https://link.testfile.org/PDF10MB",
            "https://link.testfile.org/PDF20MB",
            "https://link.testfile.org/PDF100MB",
        ]
    file_sizes = [1024, 46, 35, 16, 11, 26, 87, 33,200, 10, 20, 100,]

    t1 = time.perf_counter()
    bulk_download(urls, file_sizes)
    t2 = time.perf_counter()
    print(f"Finished in {t2-t1} seconds")
