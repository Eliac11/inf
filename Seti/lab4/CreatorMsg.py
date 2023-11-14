from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def create_mime_message():
    # Создаем объект MIME-сообщения
    msg = MIMEMultipart()

    # Добавляем текстовую часть письма
    text = "Я люблю компьютерные сети!"
    msg.attach(MIMEText(text, 'plain'))

    # Добавляем изображение
    with open('./image.png', 'rb') as img_file:
        img_data = img_file.read()
    image = MIMEImage(img_data, name='image.png')
    msg.attach(image)

    return msg