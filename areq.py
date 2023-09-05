import asyncio
import aiohttp
import aiofiles
import requests
import pathlib
import warnings
import time

warnings.filterwarnings("ignore", category=RuntimeWarning)
# fetch and save file in async way


async def func(url: str, session: aiohttp.ClientSession, size, **kwargs):
    t1 = time.perf_counter()
    print(f"getting content for {url}and size {size} Mb ")
    response = await session.get(url, **kwargs)
    content = await response.read()
    print(f"got content for {url}")
    return content

async def save_file(url, filename, size, **kwargs):
    t1 = time.perf_counter()
    content = await func(url, size=size, **kwargs)

    async with aiofiles.open(f"areq/{filename}", "wb") as f:
        await f.write(content)
        t2 = time.perf_counter()

        print(f"saved file {filename}, {size}Mb and time ={t2-t1}")


async def bulk_download(urls: list, **kwargs):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(
                save_file(
                    url=url,
                    filename=url.split("/")[-1] + ".mp4",
                    session=session,
                    size=kwargs["filesize"][urls.index(url)],
                )
            )
        await asyncio.gather(*tasks)


# https://link.testfile.org/60MB

if __name__ == "__main__":
    # here = pathlib.Path(__file__).parent
    t1 = time.perf_counter()
    urls = (
        "https://bit.ly/1GB-testfile",
        "https://link.testfile.org/PDF100MB",
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
        
    )

    asyncio.run(
        bulk_download(
            urls,
            filesize=[
                1024,
                100,
                46,
                35,
                16,
                11,
                26,
                87,
                33,
                200,
                10,
                20,
            ],
        )
    )
    t2 = time.perf_counter()
    print(f"finished in {t2-t1} seconds")
