import requests
from bs4 import BeautifulSoup
import fake_useragent as f_usr

ua = f_usr.UserAgent().random
page = 1
image_num = 0
link = 'https://zastavok.net'

headers = {
    'user-agent': ua,
}

response = requests.get(f'{link}/{page}', headers=headers).text
soup = BeautifulSoup(response, 'lxml')
main_block = soup.find('div', class_='block-photo')
all_image = main_block.find_all('div', class_='short_full')

for image in all_image:
    image_link = image.find('a').get('href')
    download_page = requests.get(f'{link}/{image_link}').text
    download_soup = BeautifulSoup(download_page, 'lxml')
    download_block = download_soup.find('div', class_='image_data').find('div', class_='block_down')
    result_link = download_block.find('a').get('href')

    image_bytes = requests.get(f'{link}/{result_link}').content

    with open(f'image/{image_num}', 'wb') as file:
        file.write(image_bytes)
    
    image_num += 1
    print(f'Image {image_num}.jpg success download!')