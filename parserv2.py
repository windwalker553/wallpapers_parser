import requests
from bs4 import BeautifulSoup
import fake_useragent as f_user

ua = f_user.UserAgent().random

headers = {
    'user-agent': ua
}

page_num = 1
image_num = 0
link = 'https://wallpaperscraft.ru'

responce = requests.get(f'{link}/all/page{page_num}', headers=headers).text
soup = BeautifulSoup(responce, 'lxml')
block = soup.find('div', class_='content-main')
all_image = block.find_all('li', class_='wallpapers__item')

soup_for_count = soup.find('ul', class_='pager__list')
all_a = soup_for_count.find_all('a', class_='pager__link')
my_list = []
for a in all_a:
    my_list.append(a)

len_ = int(len(my_list))
for page_num in range(1, len_ + 1):
    for image in all_image:
        download_image = image.find('img').get('src')

        image_bytes = requests.get(f'{download_image}').content
        
        with open(f"image2/{image_num}.jpg", 'wb') as file:
            file.write(image_bytes)

        image_num += 1
        print(f"Image num {image_num} download success!")
    page_num += 1