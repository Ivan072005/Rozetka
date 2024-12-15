import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
import os


def update_characteristic(item, key, value, index, data):
    if isinstance(value, str):
        if isinstance(item[key], list):
            item[key][index]['value_title'] = value
        else:
            item[key] = value
    with open('data.json.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"Updated {key}: {value}")


def show_details(item):
    details_window = tk.Toplevel(root)
    details_window.title(item['title'])
    details_window.configure(bg='#ADD8E6')  # Голубой цвет фона

    scrollbar = tk.Scrollbar(details_window, orient="vertical")
    canvas = tk.Canvas(details_window, yscrollcommand=scrollbar.set, bg='#ADD8E6')  # Голубой цвет фона
    scrollbar.config(command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canvas, bg='#ADD8E6')  # Голубой цвет фона
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    row = 0
    for key, values in item.items():
        if key not in ['photoUrl', 'picture-container__picture_1', 'picture-container__picture_2',
                       'picture-container__picture_3', 'picture-container__picture_4']:
            label_key = tk.Label(scrollable_frame, text=f"{key}: ", bg='#ADD8E6',
                                 fg='black')  # Белый текст, голубой фон
            label_key.grid(row=row, column=0, padx=10, pady=5, sticky="e")

            if isinstance(values, list):
                index = 0
                for docket in values:
                    if 'value_title' in docket:
                        editable_var = tk.StringVar(value=docket['value_title'])
                        editable_entry = tk.Entry(scrollable_frame, textvariable=editable_var, bg='black',
                                                  fg='#ADD8E6')  # Голубой текст, белый фон
                        editable_entry.grid(row=row, column=1, padx=10, pady=5)
                        save_button = tk.Button(
                            scrollable_frame, text="Сохранить", bg='#ADD8E6', fg='black',  # Белый текст, голубой фон
                            command=lambda k=key, v=editable_var, i=item, idx=index, d=data: update_characteristic(i, k,
                                                                                                                   v.get(),
                                                                                                                   idx,
                                                                                                                   d))
                        save_button.grid(row=row, column=2, padx=10, pady=5)
                        index += 1
                    else:
                        editable_var = tk.StringVar(value=values)
                        editable_entry = tk.Entry(scrollable_frame, textvariable=editable_var, bg='white', fg='#ADD8E6')
                        editable_entry.grid(row=row, column=1, padx=10, pady=5)
                        save_button = tk.Button(
                            scrollable_frame, text="Сохранить", bg='#ADD8E6', fg='black',
                            command=lambda k=key, v=editable_var, i=item, d=data: update_characteristic(i, k, v.get(),
                                                                                                        0, d))
                        save_button.grid(row=row, column=2, padx=10, pady=5)
            else:
                editable_var = tk.StringVar(value=values)
                editable_entry = tk.Entry(scrollable_frame, textvariable=editable_var, bg='black', fg='#ADD8E6')
                editable_entry.grid(row=row, column=1, padx=10, pady=5)
                save_button = tk.Button(
                    scrollable_frame, text="Сохранить", bg='#ADD8E6', fg='black',
                    command=lambda k=key, v=editable_var, i=item, d=data: update_characteristic(i, k, v.get(), 0, d))
                save_button.grid(row=row, column=2, padx=10, pady=5)
            row += 1

    def on_frame_configure(event):
        """Configure the canvas scroll region to encompass the inner frame"""
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)


root = tk.Tk()
root.title("Каталог телефонов")
root.configure(bg='#ADD8E6')  # Голубой цвет фона

# Добавляем контейнер для всех элементов
main_frame = tk.Frame(root, bg='#ADD8E6')  # Голубой цвет фона
main_frame.pack(side="left", fill="both", expand=True)

canvas_phone = tk.Canvas(main_frame, bg='#ADD8E6')  # Голубой цвет фона
scrollbar_phone = tk.Scrollbar(main_frame, orient="vertical", command=canvas_phone.yview)
frame_phone = tk.Frame(canvas_phone, bg='#ADD8E6')  # Голубой цвет фона

frame_phone.bind("<Configure>", lambda e: canvas_phone.configure(scrollregion=canvas_phone.bbox("all")))
canvas_phone.create_window((0, 0), window=frame_phone, anchor="nw")
canvas_phone.configure(yscrollcommand=scrollbar_phone.set, bg='#ADD8E6')  # Голубой цвет фона

scrollbar_phone.pack(side="right", fill="y")
canvas_phone.pack(side="left", fill="both", expand=True)

# Читаем данные из JSON файла
with open('data.json.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

phone_count = len(data)
row_count = (phone_count + 4) // 5  # Округляем вверх, чтобы получить нужное количество строк

for i, item in enumerate(data):
    frame = tk.Frame(frame_phone, bg='#ADD8E6')  # Голубой цвет фона
    frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

    # Загрузка и отображение главного изображения
    image_url = item['photoUrl']
    image_path = os.path.basename(image_url)
    response = requests.get(image_url)
    with open(image_path, 'wb') as file:
        file.write(response.content)
    image = Image.open(image_path)
    image = image.resize((100, 100), Image.BICUBIC)
    photo = ImageTk.PhotoImage(image)
    label_image = tk.Label(frame, image=photo, bg='#ADD8E6')  # Голубой цвет фона
    label_image.image = photo
    label_image.pack()

    # Отображение названия телефона
    label_title = tk.Label(frame, text=item['title'], bg='#ADD8E6', fg='black')  # Белый текст, голубой фон
    label_title.pack()

    # Кнопка для показа деталей
    button_details = tk.Button(frame, text="Подробнее", bg='#ADD8E6', fg='white',
                               command=lambda item=item: show_details(item))  # Белый текст, голубой фон
    button_details.pack()

root.mainloop()
