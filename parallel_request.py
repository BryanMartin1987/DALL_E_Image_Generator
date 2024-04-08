import os
from multiprocessing import Process, Manager
import openai

openai.api_key = "" # add your own key

def func1(a, b, results):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=a,
        n=1,
        size="1792x1024",
        quality="standard"
    )

    url = response['data'][0]['url']
    results.append(url)

if __name__ == "__main__":
    num_cores = os.cpu_count()
    print(f"Number of CPU cores: {num_cores}")

    with Manager() as manager:
        urls = manager.list()
        processes = []

        for _ in range(num_cores):
            p = Process(target=func1, args=('A cat with wings', 'Running', urls))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        print(list(urls))
