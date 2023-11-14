import socket
import sys

def http_client(host, port, filename):
    # Создаем сокет для клиента
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключаемся к серверу
    client_socket.connect((host, port))

    # Формируем HTTP-запрос
    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"

    # Отправляем запрос серверу
    client_socket.sendall(request.encode())

    # Получаем ответ от сервера
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    # Закрываем сокет клиента
    client_socket.close()

    # Выводим ответ сервера
    print(response.decode())

if __name__ == "__main__":
    # Проверяем количество аргументов командной строки
    if len(sys.argv) != 4:
        print("Использование: client.py хост_сервера порт_сервера имя_файла")
        sys.exit(1)

    # Получаем аргументы командной строки
    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    # Вызываем функцию http_client с переданными аргументами
    http_client(host, port, filename)
