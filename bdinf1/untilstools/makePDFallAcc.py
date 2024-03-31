from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors, fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dbtools.models import Base, tblClient, tblAccount
from datetime import datetime



from fastapi import Depends

from dbtools.database import get_db

dbsession: Session = next(get_db())

pdfmetrics.registerFont(TTFont('DudkaRegular', 'src/DudkaRegular.ttf'))
fonts.addMapping('FONTNAME', 0, 0, 'DudkaRegular')
body_style = ParagraphStyle('Body', fontName="DudkaRegular", fontSize=10)

def create_reportAllAcc():
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    pathtmp = "./tmp/"
    filename = f"accounts_report_{current_datetime}.pdf"
    
    doc = SimpleDocTemplate(pathtmp+filename, pagesize=A4)
    content = []

    clients = dbsession.query(tblClient).all()

    for client in clients:
        # Информация о клиенте
        client_info = [
            ["ФИО:", f"{client.txtClientSurname} {client.txtClientName} {client.txtClientSecondName}"],
            ["Дата рождения:", str(client.datBirthday)],
            ["Адрес:", client.txtClientAddress]
        ]

        # Счета клиента
        accounts_data = [
            ["Номер счета", "Тип счета", "Дата открытия", "Сумма на счете"]
        ]
        for account in client.accounts:
            accounts_data.append([
                account.txtAccountNumber,
                account.account_type.txtAccountTypeName,
                str(account.datAccountBegin),
                str(account.fltAccountSum)
            ])

        # Создание таблицы для счетов клиента
        table = Table(accounts_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'DudkaRegular'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        for cinf in client_info:
            content.append(Paragraph(f"{cinf[0]} {cinf[1]}",style=body_style))
            

        content.append(table)
        content.append(Paragraph(f"Суммарное количество счетов: {len(client.accounts)}",style=body_style))
        content.append(Paragraph("-" * 100, body_style))  # Горизонтальная черта между клиентами

    # Общая сумма на всех счетах
    total_sum = sum([account.fltAccountSum for client in clients for account in client.accounts])
    content.append(Paragraph(f"Общая сумма на всех счетах: {total_sum}", body_style))

    doc.build(content)

    return filename