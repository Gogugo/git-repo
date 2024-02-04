from tkinter import *
import socket
from scapy.all import ARP, Ether, srp, sniff
import requests
import webbrowser
import os


def find_document_path(document_name, search_directories):
    for directory in search_directories:
        for root, dirs, files in os.walk(directory):
            if document_name.lower() in map(str.lower, files):
                return os.path.join(root, document_name)
    return None

def open_document(document_path):
    os.startfile(document_path)

def open_document_button_clicked():
    document_name = "Мануал 1.txt"
    search_directories = ['C:\\', 'D:\\', 'E:\\']  # Здесь вы можете добавить или изменить список директорий для поиска
    document_path = find_document_path(document_name, search_directories)
    
    if document_path:
        open_document(document_path)
        result_label.config(text='Документ успешно открыт!')
    else:
        result_label.config(text='Документ не найден.')
def open_document_button_clicked1():
    document_name = "Мануал 2.txt"
    search_directories = ['C:\\', 'D:\\', 'E:\\']  # Здесь вы можете добавить или изменить список директорий для поиска
    document_path = find_document_path(document_name, search_directories)
    
    if document_path:
        open_document(document_path)
        result_label.config(text='Документ успешно открыт!')
    else:
        result_label.config(text='Документ не найден.')
# Функция для проверки ссылок и открытия рабочей ссылки в браузере
def check_and_open_links():
    # Список ссылок
    ссылки = [
        "http://192.168.0.1",
        "http://192.168.1.1",
    ]
    
    # Перебор ссылок
    for ссылка in ссылки:
        try:
            # Отправляем GET-запрос к ссылке
            response = requests.get(ссылка)

            # Проверяем статус код ответа
            if response.status_code == 200:
                print(f"Рабочая ссылка: {ссылка}")
                # Открываем ссылку в браузере без закрытия
                webbrowser.open_new_tab(ссылка)
                break
            else:
                print(f"Нерабочая ссылка: {ссылка}")
        except requests.exceptions.RequestException:
            print(f"Ошибка при подключении к ссылке: {ссылка}")





# Функция, которую вы можете добавить
def custom_function():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем соединение с внешним хостом (например, google.com)
    try:
        sock.connect(("google.com", 80))

    # Получаем IP-адрес и порт, который был использован для исходящего соединения
        wifi_ip, _ = sock.getsockname()

    except socket.error:
        wifi_ip = "Не удалось определить IP-адрес Wi-Fi"


# Создание пакета ARP запроса
    arp = ARP(pdst=wifi_ip+"/24")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

# Отправка и прием пакетов через сокет
    result = srp(packet, timeout=3, verbose=0)[0]

# Обработка результатов сканирования
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

# Вывод результатов сканирования
    print("Устройства, подключенные к Wi-Fi:")
    print("----------------------------------")
    smart_devices = []
    for device in devices:
        print(f"IP: {device['ip']}\tMAC: {device['mac']}")
        a = (f"{device['mac']}")
        def is_smart_device(mac_address):
            try:
        # Получение производителя по MAC-адресу из базы данных
                response = requests.get(f"https://api.macvendors.com/{mac_address}")
                manufacturer = response.text
                print(f"Производитель: {manufacturer}")
                # Проверка ключевых слов для умных устройств
                smart_keywords = ["smart", "iot", "wifi", "home", "automation"]
                for keyword in smart_keywords:
                    if keyword in manufacturer.lower():
                        smart_devices.append(manufacturer)
                        return True
                        
                return False

            except Exception as e:
                print(f"Произошла ошибка при определении устройства: {str(e)}")
                return False
            # Пример использования
        mac_address = a
        is_smart = is_smart_device(mac_address)
        if is_smart:
            print("Умное")
        else:
            print(" ")
            
        print("Список умных устройств: ")
        for device in smart_devices:
            print(device)

pass
# Создание главного окна программы
root = Tk()
root.title("Безопасность умного дома")
root.geometry("400x300")


# Создание метки для приветствия
greeting_label = Label(root, text="Добро пожаловать!")
greeting_label.pack()



# Создание кнопки для вызова пользовательской функции
custom_button = Button(root, text="Мои устройсва в сети", command=custom_function)
custom_button.pack()


custom_button1 = Button(root, text="Мануал для создания гостевой сети", command=open_document_button_clicked)
custom_button1.pack()


custom_button2 = Button(root, text="Мануал для добавления умных устройств к гостевой сети", command=open_document_button_clicked1)
custom_button2.pack()


custom_button3 = Button(root, text="Переход к созданию гостевой сети и добавления их в эту сеть", command=check_and_open_links)
custom_button3.pack()


# Запуск цикла обработки событий главного окна
root.mainloop()
