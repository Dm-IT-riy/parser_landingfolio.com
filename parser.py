import requests
import json
import os
import time

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36',
    'accept': '*/*'
}

def get_data(headers):
    '''Collect data and return a JSON file'''
    
    URL = 'https://landingfolio.com'

    r = requests.get(url = URL, headers = HEADERS)
    with open('index.html', 'w', encoding = 'utf-8') as file:
        file.write(r.text)

    offset = 0
    img_count = 0
    result_list = []
    while True:
        url = f'https://s1.landingfolio.com/api/v1/inspiration/?offset={offset}&color=%23undefined'
        response = requests.get(url = url, headers = HEADERS)
        data = response.json()

        for item in data:
            if 'description' in item:
                images = item.get('images')
                img_count += len(images)
                for img in images:
                    img.update({'url': f'https://landingfoliocom.imgix.net/{img.get("url")}'})

                result_list.append(
                    {
                        'title': item.get('title'),
                        'description': item.get('description'),
                        'url': item.get('url'),
                        'images': images
                    }
                )
            else:
                with open('result_list.json', 'a', encoding = 'utf-8') as file:
                    json.dump(result_list, file, indent = 4, ensure_ascii = False)

                    return f'\n{"#" * 33}\nWork finished. Images count: {img_count}\n{"#" * 33}'

        print(f'Processed {offset}')
        offset += 1

def download_images(file_path):

    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
    }

    try:
        with open(file_path) as file:
            src = json.load(file)
    except Exception as _ex:
        print(_ex)
        print('Check the file path')

    items_len = len(src)
    count = 1

    for item in src:
        item_name = item.get('title')
        item_imgs = item.get('images')

        if not os.path.exists(f'data/{item_name}'):
            os.mkdir(f'data/{item_name}')

            for img in item_imgs:
                r = requests.get(url = img['url'], headers = headers)
                with open(f'data/{item_name}/{img["type"]}.png', 'wb') as file:
                    file.write(r.content)

            print(f'Download {count}/{items_len}')
            count += 1
    
    print('Work finished')

def main():
    start_time = time.time()

    print(get_data(headers = HEADERS))
    print(download_images('result_list.json'))

    finish_time = time.time() - start_time
    print(f'Worked time: {finish_time}')
if __name__ == '__main__':
    main()