from socket import *
import base64
import ssl
import CreatorMsg


endmsg = "\r\n.\r\n"
# Выбираем почтовый сервер
mailserver = ("smtp.mail.ru", 465)  # Замените "smtp.example.com" на ваш SMTP-сервер и 25 на порт

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket = ssl.wrap_socket(clientSocket)

# Создаем сокет clientSocket и устанавливаем TCP-соединение
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024)
print(recv)
if recv[:3] != b'220':
    print('код 220 от сервера не получен.')



# Отправляем команду HELO и выводим ответ сервера.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != b'250':
    print('код 250 от сервера не получен.')

# Аутентификация с использованием пароля приложения
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
recv2 = clientSocket.recv(1024)
print(recv2)

# Отправляем закодированный в base64 логин и пароль приложения
username = base64.b64encode(b'posti.ilya@mail.ru').decode() + '\r\n'
clientSocket.send(username.encode())
recv3 = clientSocket.recv(1024)
print(recv3)

password = base64.b64encode(b'XXXXXXXXXXX').decode() + '\r\n'  # Замените на ваш пароль приложения
clientSocket.send(password.encode())
recv4 = clientSocket.recv(1024)
print(recv4)


# Отправляем команду MAIL FROM и выводим ответ сервера.
mailFromCommand = 'MAIL FROM: posti.ilya@mail.ru\r\n'  # Замените на ваш адрес электронной почты
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024)
print(recv2)

# Отправляем команду RCPT TO и выводим ответ сервера.
rcptToCommand = 'RCPT TO: posti.ilya@mail.ru\r\n'  # Замените на адрес получателя
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024)
print(recv3)

# Отправляем команду DATA и выводим ответ сервера.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024)
print(recv4)

# Отправляем данные сообщения.
clientSocket.send(CreatorMsg.create_mime_message().as_bytes())

# Сообщение завершается одинарной точкой.
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024)
print(recv5)

# Отправляем команду QUIT, получаем ответ сервера
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024)
print(recv6)

# Закрываем соединение.
clientSocket.close()
