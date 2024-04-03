from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors, fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import and_
from dbtools.models import Base, tblClient, tblAccount, tblOperation, tblAccountType
from datetime import datetime



from fastapi import Depends

from dbtools.database import get_db

dbsession: Session = next(get_db())

pdfmetrics.registerFont(TTFont('DudkaRegular', 'src/DudkaRegular.ttf'))
fonts.addMapping('FONTNAME', 0, 0, 'DudkaRegular')
body_style = ParagraphStyle('Body', fontName="DudkaRegular", fontSize=10)

def create_reportinfoAcc(account_number):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    pathtmp = "./tmp/"
    filename = f"InfoAccount_report_{current_datetime}.pdf"

    
    doc = SimpleDocTemplate(pathtmp+filename, pagesize=A4)

    account_info = dbsession.query(
        tblAccount, tblAccountType, tblClient
    ).join(
        tblAccountType, tblAccount.intAccountTypeId == tblAccountType.intAccountTypeId
    ).join(
        tblClient, tblAccount.intClientId == tblClient.intClientId
    ).filter(
        tblAccount.txtAccountNumber == account_number
    ).first()

    # Получаем операции по счету, упорядоченные по убыванию даты
    operations = dbsession.query(
        tblOperation
    ).filter(
        tblOperation.intAccountId == account_info[0].intAccountId
    ).order_by(
        tblOperation.datOperation.desc()
    ).all()

    
    elements = []

    elements.append(Paragraph("Информация по счету", body_style))
    # Добавляем информацию о счете в документ
    account_data = [
        ["Номер счета", "Наименование типа счета", "ФИО клиента", "Дата открытия счета"],
        [account_info[0].txtAccountNumber, account_info[1].txtAccountTypeName, 
         f"{account_info[2].txtClientSurname} {account_info[2].txtClientName} {account_info[2].txtClientSecondName}",
         account_info[0].datAccountBegin.strftime("%d.%m.%Y")]
    ]
    account_table = Table(account_data)
    account_table.setStyle(TableStyle([
                                       ('FONTNAME', (0, 0), (-1, 0), 'DudkaRegular')]))
    elements.append(account_table)
    elements.append(Paragraph("-"*100 + "\n\n", body_style))

    # Добавляем информацию об операциях по счету в документ
    operation_data = [["Дата проведения операции", "Наименование типа операции", "Сумма"]]
    for operation in operations:
        operation_data.append([
            operation.datOperation.strftime("%d.%m.%Y"),
            operation.operation_type.txtOperationTypeName,
            str(operation.fltValue)
        ])

    elements.append(Paragraph("Операции по счету", body_style))

    operation_table = Table(operation_data)
    operation_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                         ('FONTNAME', (0, 0), (-1, -1), 'DudkaRegular'),
                                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                         ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(operation_table)

    
    doc.build(elements)
    return filename