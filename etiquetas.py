import sys
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class DataInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Etiquetas de Datos para la empresa Appareil Ltda.')
        self.setGeometry(100, 100, 400, 500)

        # Estilo de la interfaz
        self.setStyleSheet("""
            background-color: #f0f0f0;
            font-family: Arial;
        """)

        # Preguntar por el tipo de cliente (Particular o Privado)
        self.client_type_label = QLabel('<b>¿Es el cliente Particular o Privado?</b>')
        self.client_type_label.setStyleSheet("font-size: 16px;")
        self.client_type_label.setWordWrap(True)

        # Opción para escribir la respuesta en lugar de seleccionar
        self.client_type_input = QLineEdit()
        self.client_type_input.setPlaceholderText("Escribe tu respuesta aquí")

        # Ingresar RUT
        self.rut_label = QLabel('<b>Ingrese el RUT:</b>')
        self.rut_label.setStyleSheet("font-size: 16px;")
        self.rut_input = QLineEdit()
        self.rut_input.setPlaceholderText("Escribe tu respuesta aquí")

        # Ubicación de la empresa y comuna
        self.company_location_label = QLabel('<b>Ubicación y Comuna:</b>')
        self.company_location_label.setStyleSheet("font-size: 16px;")
        self.company_location_input = QLineEdit()
        self.company_location_input.setPlaceholderText("Escribe tu respuesta aquí")

        # Nombre y apellido del cliente
        self.client_name_label = QLabel('<b>Nombre del Cliente:</b>')
        self.client_name_label.setStyleSheet("font-size: 16px;")
        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Escribe tu respuesta aquí")

        # Número de teléfono y correo electrónico
        self.contact_phone_label = QLabel('<b>Número de Teléfono:</b>')
        self.contact_phone_label.setStyleSheet("font-size: 16px;")
        self.contact_phone_input = QLineEdit()
        self.contact_phone_input.setPlaceholderText("Escribe tu respuesta aquí")

        self.email_label = QLabel('<b>Correo Electrónico:</b>')
        self.email_label.setStyleSheet("font-size: 16px;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Escribe tu respuesta aquí")

        # Número de factura
        self.invoice_number_label = QLabel('<b>Número de Documento:</b>')
        self.invoice_number_label.setStyleSheet("font-size: 16px;")
        self.invoice_number_input = QLineEdit()
        self.invoice_number_input.setPlaceholderText("Escribe tu respuesta aquí")

        # Constante de porcentaje de escala de la imagen
        self.scale_percent = 62

        # Botones de generación, guardar e imprimir
        self.submit_button = QPushButton('Generar PDF')
        self.submit_button.setStyleSheet("""
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        """)
        self.save_button = QPushButton('Guardar PDF')
        self.save_button.setStyleSheet("""
            background-color: #008CBA;
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        """)
        self.print_button = QPushButton('Imprimir PDF')
        self.print_button.setStyleSheet("""
            background-color: #f44336;
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.client_type_label)
        layout.addWidget(self.client_type_input)
        layout.addWidget(self.rut_label)
        layout.addWidget(self.rut_input)
        layout.addWidget(self.company_location_label)
        layout.addWidget(self.company_location_input)
        layout.addWidget(self.client_name_label)
        layout.addWidget(self.client_name_input)
        layout.addWidget(self.contact_phone_label)
        layout.addWidget(self.contact_phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.invoice_number_label)
        layout.addWidget(self.invoice_number_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.print_button)

        layout.addLayout(button_layout)

        self.submit_button.clicked.connect(self.generate_pdf)
        self.save_button.clicked.connect(self.save_pdf)
        self.print_button.clicked.connect(self.print_pdf)
        self.setLayout(layout)
        self.pdf_counter = 1  # Inicializamos el contador de PDFs

    def generate_pdf(self):
        # Obtener los datos ingresados por el usuario
        client_type = self.client_type_input.text().upper()
        company_location = self.company_location_input.text().upper()
        rut = self.rut_input.text()
        client_name = self.client_name_input.text().upper()
        contact_phone = self.contact_phone_input.text()
        email = self.email_input.text()
        invoice_number = self.invoice_number_input.text()

        # Crear el contenido del PDF
        pdf_filename = f'cliente_info_{self.pdf_counter}.pdf'
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()

        # Cargar la fuente Calibri
        pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))

        # Estilo personalizado para centrar y ajustar el tamaño de fuente
        centered_style = ParagraphStyle(
            name='CenteredStyle',
            parent=styles['Normal'],
            fontName='Calibri',
            fontSize=16,
            alignment=1  # 0=Left, 1=Center, 2=Right
        )

        title_style = ParagraphStyle(
            name='TitleStyle',
            parent=styles['Normal'],
            fontName='Calibri',
            fontSize=24,
            alignment=1,
            textColor=colors.black,
            spaceAfter=24
        )

        bold_style = ParagraphStyle(
            name='BoldStyle',
            parent=styles['Normal'],
            fontName='Calibri',
            fontSize=16,
            textColor=colors.black,
            spaceAfter=12
        )

        content = []

        # Agregar título al PDF
        content.append(Paragraph('<b>ETIQUETA DE DATOS</b>', title_style))

        # Agregar contenido al PDF con saltos de línea
        content.append(Spacer(1, 24))
        content.append(Paragraph(f'<b>{client_type}</b>', centered_style))
        content.append(Paragraph(f'{company_location}', centered_style))
        content.append(Paragraph(f'{rut}', centered_style))
        content.append(Paragraph(f'<b>{client_name}</b>', centered_style))
        content.append(Paragraph(f'{contact_phone}\n{email}', centered_style))
        content.append(Spacer(1, 24))
        content.append(Paragraph('<b>FACTURA</b>', centered_style))
        content.append(Paragraph(f'<b>N° {invoice_number}</b>', centered_style))

        # Agregar la imagen al final del PDF y escalarla
        img_path = 'C:/Users/Appareil/OneDrive/Escritorio/Programa/imagen_HD_pie.png'
        img = Image(img_path)
        img.drawWidth = img.drawWidth * self.scale_percent / 100  # Escalar el ancho
        img.drawHeight = img.drawHeight * self.scale_percent / 100  # Escalar la altura
        content.append(Spacer(1, 24))
        content.append(img)

        doc.build(content)
        self.pdf_counter += 1

        QMessageBox.information(self, "PDF Generado", f'Se ha generado el archivo PDF: {pdf_filename}')

    def save_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "", "Archivos PDF (*.pdf)")
        if file_path:
            # Obtener el nombre del archivo PDF generado
            pdf_filename = f'cliente_info_{self.pdf_counter - 1}.pdf'
            
            # Copiar el PDF generado al destino especificado
            shutil.copy(pdf_filename, file_path)
            
            QMessageBox.information(self, "PDF Guardado", f'El PDF se ha guardado en: {file_path}')

    def print_pdf(self):
        self.generate_pdf()  # Generar el PDF primero
        QMessageBox.information(self, "PDF Impreso", "El PDF se ha enviado a la impresora.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataInputWidget()
    window.show()
    sys.exit(app.exec_())
