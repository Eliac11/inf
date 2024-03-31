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
from dbtools.models import Base, tblClient, tblAccount, tblOperation
from datetime import datetime



from fastapi import Depends

from dbtools.database import get_db

dbsession: Session = next(get_db())

pdfmetrics.registerFont(TTFont('DudkaRegular', 'src/DudkaRegular.ttf'))
fonts.addMapping('FONTNAME', 0, 0, 'DudkaRegular')
body_style = ParagraphStyle('Body', fontName="DudkaRegular", fontSize=10)

def create_reportEndAcc():
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    pathtmp = "./tmp/"
    filename = f"endedAccounts_report_{current_datetime}.pdf"

    closed_accounts = dbsession.query(tblAccount).filter(and_(tblAccount.datAccountEnd != None, tblAccount.datAccountEnd < datetime.now())).all()
    
    doc = SimpleDocTemplate(pathtmp+filename, pagesize=A4)

    report_content = []

    # Добавляем заголовок
    report_content.append(Paragraph("Закрытые счета", body_style))

    # Для каждого закрытого счета формируем информацию
    for account in closed_accounts:
        account_info = []
        account_info.append(Paragraph("Тип счета: {}".format(account.account_type.txtAccountTypeName), body_style))
        account_info.append(Paragraph("Номер счета: {}".format(account.txtAccountNumber), body_style))
        account_info.append(Paragraph("Дата открытия: {}".format(account.datAccountBegin), body_style))
        account_info.append(Paragraph("Дата закрытия: {}".format(account.datAccountEnd), body_style))
        client_info = "ФИО клиента: {} {} {}".format(account.client.txtClientSurname, account.client.txtClientName, account.client.txtClientSecondName)
        account_info.append(Paragraph(client_info, body_style))
        account_info.append(Paragraph("Адрес клиента: {}".format(account.client.txtClientAddress), body_style))
        
        # Получаем операции по счету
        operations = dbsession.query(tblOperation).filter_by(intAccountId=account.intAccountId).all()
        operations_data = [["Дата операции", "Тип операции", "Сумма"]]
        for operation in operations:
            operations_data.append([operation.datOperation, operation.operation_type.txtOperationTypeName, operation.fltValue])
        
        # Добавляем таблицу операций
        operations_table = Table(operations_data)
        operations_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'DudkaRegular'),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        report_content.extend(account_info)
        report_content.append(operations_table)
        report_content.append(Paragraph("Количество операций: {}".format(len(operations)), body_style))  # Вычитаем заголовок таблицы
        report_content.append(Paragraph("-" * 100, body_style))

    # Добавляем содержимое в документ и закрываем его
    doc.build(report_content)
    return filename