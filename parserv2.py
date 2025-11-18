import requests
from bs4 import BeautifulSoup
import fake_useragent as f_user
import tkinter as tk
from tkinter import ttk, messagebox

def num_pic():
    global image_count
    image_count = ent1.get()

def main():
    ua = f_user.UserAgent().random

    headers = {
        'user-agent': ua
    }
    page_num = 1
    image_num = 0
    link = 'https://wallpaperscraft.ru'

    responce = requests.get(f'{link}/all/page{6900}', headers=headers).text
    soup = BeautifulSoup(responce, 'lxml')

    soup_for_count = soup.find('ul', class_='pager__list')
    all_a = soup_for_count.find_all('a', class_='pager__link')
    my_list = [int(a.text) for a in all_a if a.text.isdigit()]
    max_page = max(my_list)
    
    flag = False

    for page_num in range(1, max_page):
        responce2 = requests.get(f'{link}/all/page{page_num}', headers=headers).text
        soup2 = BeautifulSoup(responce2, 'lxml')
        block = soup2.find('div', class_='content-main')
        all_image = block.find_all('li', class_='wallpapers__item')
        for image in all_image:
            download_image = image.find('img').get('src')

            image_bytes = requests.get(f'{download_image}').content
            
            with open(f"image2/{image_num}.jpg", 'wb') as file:
                file.write(image_bytes)

            image_num += 1
            print(f"Image num {image_num} download success!")
            if image_num == int(image_count):
                flag = True
                break
        if flag == True:
            break
    messagebox.showinfo("end", 'all you image is download!, you can close app.')

def draw_gradient(canvas, width, height, color1, color2):
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_line(0, i, width, i, fill=color)            

def start():
    main()

root = tk.Tk()
root.maxsize(1200, 800)
root.minsize(600, 400)
root.title("Main window")
width, height = 600, 400
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill='both', expand=True)
draw_gradient(canvas, width, height, "blue", "purple")

tk.Label(root, text='How much pictures you want pars?', font=("Georgia", 15)).pack(pady=10)
ent1 = tk.Entry(root, width=30)
ent1.pack(pady=10)
btn1 = tk.Button(root, text='save value', font=("Impact", 15), bg='powderblue',fg='snow', command=num_pic)
btn1.pack(pady=10)
btn2 = tk.Button(root, text="start parser", font=("Impact", 15), bg='powderblue',
                 fg='snow', command=start)
btn2.pack(pady=10)

root.mainloop()