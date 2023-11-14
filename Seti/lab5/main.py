from socket import *
import threading

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]

        # Открываем и считываем содержимое файла
        try:
            with open(filename[1:], 'rb') as file:
                outputdata = file.read()

            # Отправляем HTTP-заголовок клиенту
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")

            # Отправляем содержимое файла клиенту
            connectionSocket.sendall(outputdata)

        except IOError:
            # Если файл не найден, отправляем HTTP-сообщение 404 Not Found
            connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>")
    finally:
        # Закрываем клиентский сокет
        connectionSocket.close()

def main():
    # Создаем основной сокет сервера
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', 8080))
    serverSocket.listen(5)
    print('Готов к обслуживанию...')

    while True:
        # Принимаем соединение от клиента
        connectionSocket, addr = serverSocket.accept()
        print(f"Получено соединение от {addr}")

        # Создаем новый поток для обработки запроса клиента
        client_handler = threading.Thread(target=handle_client, args=(connectionSocket,))
        client_handler.start()

if __name__ == "__main__":
    main()
