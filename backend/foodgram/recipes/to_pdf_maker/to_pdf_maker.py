import io
from django.http import FileResponse

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def shopping_cart_to_pdf(shopping_list):
    buffer = io.BytesIO()

    pdfmetrics.registerFont(
        TTFont('FreeSans', 'recipes/to_pdf_maker/FreeSans.ttf')
    )
    content = canvas.Canvas(buffer, pagesize=A4)
    content.setFont('FreeSans', 20)

    content.translate(1.5 * cm, 28 * cm)
    content.drawString(6 * cm, 0, 'Список покупок')
    content.setFont('FreeSans', 12)
    new_page_counter = 0

    for ingredient in shopping_list:
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['amount']
        content.translate(0, -0.8 * cm)
        content.drawString(0, 0, f'{name}: {amount} {measurement_unit}')
        new_page_counter += 1
        if new_page_counter == 33:
            new_page_counter = 0
            content.showPage()
            content.translate(1.5 * cm, 28 * cm)
    content.save()

    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='shopping_cart.pdf'
    )
