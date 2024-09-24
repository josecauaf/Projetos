from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QFont
from decimal import Decimal
import webbrowser
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting the "calculadora_cdi" function start variables
        self.cdi_value = 0
        self.value = 0
        self.months = 0 

        # Main window configuration
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        self.icon = QIcon(icon_path) 

        self.setWindowTitle('Calculadora CDI') # Title
        self.setWindowIcon(self.icon) # Setting the main window icon
        self.setGeometry(190, 195, 1000, 400) # Setting the coordinates (x, y, #, #) and minimal size (#, #, w, h)]
        self.setObjectName('mainwindow') # Setting an ID to self.QMainWindow

        self.show()
    
        # Styling Widgets
        self.setStyleSheet('''
                           QMainWindow#mainwindow{
                           background-color: #1c1c1c}

                           QLabel#label04, #label05, #label06, #label07{
                           color: #e0e0e0;
                           border: 2px solid #5b5b5b;}

                           QLineEdit{ 
                           color: #505050; 
                           background-color: #e0e0e0;
                           selection-color: white;
                           selection-background-color: #474747 }

                           QSpinBox{
                           color: #505050; 
                           background-color: #e0e0e0;
                           selection-color: white;
                           selection-background-color: #474747}
                           
                           QPushButton#button01{
                           color: #3a3a3a;
                           text-align: center;
                           background-color: #ababab;
                           border-style: solid;
                           border-width: 2px;
                           border-color : gray;
                           font: bold 14px;
                           padding: 6px}

                           QPushButton#button01:pressed {
                           background-color: #868686;
                           border-style: inset}

                           QPushButton#button02{
                           color: #0084ff;
                           background-color: #d6d6d6;
                           border-style: solid;
                           border-width: 1px;
                           border-color: #0084ff;
                           border-radius: 3px}

                           QPushButton#button02:pressed {
                           background-color: #afb3b0;
                           border-style: inset}
                           ''')

        # Label storage
        label01 = QLabel('Coloque aqui seu percentual CDI (Ex.: 100% do CDI)')
        label01.setObjectName('label01')

        label02 = QLabel('Coloque aqui o valor a ser calculado')

        label03 = QLabel('Em quantos meses?')

        self.label04 = QLabel(f'Rendimento Total -> 0')
        self.label04.setObjectName('label04')
        self.label04.setFixedWidth(600)

        self.label05 = QLabel(f'Rendimento bruto de juros -> 0')
        self.label05.setObjectName('label05')
        self.label05.setFixedWidth(600)

        self.label06 = QLabel(f'Taxa do CDI inserido por mês -> 0%')
        self.label06.setObjectName('label06')
        self.label06.setFixedWidth(600)

        self.label07 = QLabel(f'Rendimento descontado do IR -> 0')
        self.label07.setObjectName('label07')
        self.label07.setFixedWidth(600)

        self.label08 = QLabel('<a href=''''https://github.com/josecauaf>Meu perfil no GitHub</a>''')
        self.label08.setOpenExternalLinks(True)

        self.label09 = QLabel('Versão atual (0.8.0 Beta)')

        # Input (QLineEdit) storage
        self.input01 = QLineEdit()
        self.input01.setMaxLength(30)
        self.input01.setPlaceholderText('Insira sua porcentagem do CDI')

        self.input02 = QLineEdit()
        self.input02.setMaxLength(30)
        self.input02.setPlaceholderText('Insira o valor usando apenas números e/ou ponto(s)')

        self.input03 = QSpinBox()
        self.input03.setMinimum(1)

        # Buttons storage
        self.button01 = QPushButton('Calcular')
        self.button01.setFixedWidth(300)
        self.button01.setObjectName('button01')
        self.button01.clicked.connect(self.cdi_calculator)

        self.button02 = QPushButton('Deseja contribuir? :)')
        self.button02.setObjectName('button02')
        self.button02.clicked.connect(self.donate)

        # Creating the fonts and parameters
        label_font01 = QFont("Calibri", 20)

        # Setting the fonts
        label01.setFont(label_font01) # Labels
        label02.setFont(label_font01)
        label03.setFont(label_font01)
        self.label04.setFont(label_font01)
        self.label05.setFont(label_font01)
        self.label06.setFont(label_font01)
        self.label07.setFont(label_font01)

        self.input01.setFont(label_font01) # Inputs
        self.input02.setFont(label_font01)
        self.input03.setFont(label_font01)
        
        # Creating the main Layout
        layout01 = QVBoxLayout()

        # Adding widgets to the main Layout in order
        layout01.addWidget(label01)
        layout01.addWidget(self.input01)
        layout01.addWidget(label02)
        layout01.addWidget(self.input02)
        layout01.addWidget(label03)
        layout01.addWidget(self.input03)
        layout01.addWidget(self.button01, alignment=Qt.AlignmentFlag.AlignCenter) # Center alignment

        # Creating secondary Layouts
        layout02 = QHBoxLayout()
        layout02.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        ) # Center alignment

        layout03 = QHBoxLayout()
        layout03.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        ) # Center alignment

        layout04 = QHBoxLayout()
        layout04.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        ) # Center alignment

        # Adding secondary Layouts to Main Layout
        layout01.addLayout(layout02)
        layout01.addLayout(layout03)
        layout01.addLayout(layout04)

        # Adding widgets to secondary Layouts in order
        layout02.addWidget(self.label04, alignment=Qt.AlignmentFlag.AlignLeft) # Left alignment
        layout02.addWidget(self.label05)

        layout03.addWidget(self.label06)
        layout03.addWidget(self.label07)

        layout04.addWidget(self.label08)
        layout04.addWidget(self.label09)
        layout04.addWidget(self.button02)

        layout01.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        ) # Center/Top alignment

        # Creating a container
        container = QWidget()
        container.setLayout(layout01) # Setting the Main Layout to the container

        self.setCentralWidget(container) # Centralizing the container

    def receiving_cdi(self): # Creating a function that receives, processes, and converts "CDI" data
        self.value01 = self.input01.text() # Receives the value of "input01"
        if self.value01 == '': # Firstly, if the field is empty, trigger an empty field error
            self.error01 = QMessageBox.warning(
                self,
                'Você precisa inserir dados! (Erro no campo "CDI")',
                'Insira número(s), caso seja número fracionado, utilize ponto. (Não utilize %, vírgulas, letras, etc... Apenas números!)',
                QMessageBox.StandardButton.Ok
                )
        else:
            try: # If it has a value, try converting it to decimal
                self.cdi_value = Decimal(self.value01)
                return 0
            except: # If there is a different value of numbers and points, trigger an invalid value error
                self.error01 = QMessageBox.warning(
                    self,
                    'Não foi possível inserir a porcentagem! (Erro no campo "CDI")',
                    'Insira apenas números, caso seja número fracionado, utilize ponto. (Não utilize %, vírgulas, letras, etc... Apenas números!)',
                    QMessageBox.StandardButton.Ok
                    )
            
    def receiving_value(self): # Creating a function that receives, processes, and converts "valor(value)" data
        self.value02 = self.input02.text()
        if self.value02 == '': # Firstly, if the field is empty, trigger an empty field error
            self.error02 = QMessageBox.warning(
                self,
                'Você precisa inserir dados! (Erro no campo "Valor")',
                'Insira número(s), caso seja número fracionado, utilize ponto. (Não utilize %, vírgulas, letras, etc... Apenas números!)',
                QMessageBox.StandardButton.Ok
                )
        else:
            try: # If it has a value, try converting it to decimal
                self.main_value = Decimal(self.value02)
                return 0
            except: # If there is a different value of numbers and points, trigger an invalid value error
                self.error02 = QMessageBox.warning(
                    self,
                    'Não foi possível inserir o valor! (Erro no campo "Valor")',
                    'Insira apenas números, caso seja número fracionado, utilize ponto. (Não utilize %, vírgulas, letras, etc... Apenas números!)',
                    QMessageBox.StandardButton.Ok
                    )
                return None
            
    def receiving_months(self): # Creating a function that receives, processes, and converts "meses(months)" data
        self.value03 = self.input03.text()
        if self.value03 == '': # Firstly, if the field is empty, trigger an empty field error
            self.error03 = QMessageBox.warning(
                self,
                'Você precisa inserir dados! (Erro no campo "Meses")',
                'Insira número(s) (Não utilize %, pontos, vírgulas, letras, etc... Apenas números!)',
                QMessageBox.StandardButton.Ok
                )
        else:
            try: # If it has a value, try converting it to integer
                self.months = int(self.value03)
                return 0
            except: # If there is a different value of numbers, trigger an invalid value error
                self.error03 = QMessageBox.warning(
                    self,
                    'Não foi possível inserir o(s) mese(s)! (Erro no campo "Meses")',
                    'Insira apenas números! (Não utilize %, pontos, vírgulas, letras, etc... Apenas números!)',
                    QMessageBox.StandardButton.Ok
                    )
                
    def cdi_calculator(self): # Creating the main function, which processes the data, calculates and displays
        # Creating variables for errors
        # If any previous value causes an error, it receives the value None to interrupt the current function
        is_error02 = self.receiving_cdi()
        is_error01 = self.receiving_value()
        is_error03 = self.receiving_months()

        # Checks if the return value of each function is None, if any is None, the current function will stop, if the value is different from None, continue the code
        if is_error01 == None:
            return 0
        if is_error02 == None:
            return 0
        if is_error03 == None:
            return 0 

        di_tax = Decimal(10.40) # Current DI rate

        # Calculation that performs data processing, reduction and conversion
        reduced_cdi = self.cdi_value / 100 * di_tax
        monthly_tax = reduced_cdi / 12 / 100
        monthly_tax = Decimal(monthly_tax)
        monthly_tax_illustration = reduced_cdi / 12
        result = self.main_value * (1 + monthly_tax) ** self.months

        result = Decimal(result) # Converting the default var result into a decimal

        only_tax = result - self.main_value # Creating a variable just to show the yield

        # Table with percentages of income imports in months (ir_"days") 30 days = 1 month
        ir_180 = Decimal(22.5)
        ir_181_360 = Decimal(20)
        ir_361_720 = Decimal(17.5)
        ir_721 = Decimal(15)

        # Creating variables to show specific values ​​with income tax
        ir_result = 0
        ir_tax_demo = 0

        # Treatment to know which month was entered to deduct the exact tax
        if self.months < 6:
            ir_result = (ir_180 * only_tax) / 100
            ir_tax_demo = ir_180
        if self.months >= 6:
            ir_result = (ir_181_360 * only_tax) / 100
            ir_tax_demo = ir_181_360
        if self.months >= 12:
            ir_result = (ir_361_720 * only_tax) / 100
            ir_tax_demo = ir_361_720
        if self.months >= 24:
            ir_result = (ir_721 * only_tax) / 100
            ir_tax_demo = ir_721

        # Creating a variable that shows the net income (already with the income import discounted
        ir_liquid = (result - ir_result) - self.main_value
        if ir_liquid < 0: # If the value is below 0, the value will be 0
            ir_liquid = 0
            
        # Showing the results as Labels (setting a "new" text)
        self.label04.setText(f'Rendimento Total -> {result:.2f}')
        self.label05.setText(f'Rendimento bruto de juros -> {only_tax:.2f}')
        self.label06.setText(f'Taxa do CDI inserido por mês -> {monthly_tax_illustration:.2f}%')
        self.label07.setText(f'Rendimento descontado do IR -> {ir_liquid:.2f}')
        
        # ({ir_result:.2f} deduzidos) (Taxa IR: {ir_tax_demo}%)' to use later

    # Creating a function to donate
    def donate(self):
        donate = QMessageBox()
        donate.setText('Olá! Você gostaria de contribuir doando algum valor?')
        donate.setWindowTitle('Gostaria de contribuir? :D')
        donate.setWindowIcon(self.icon)
        donate.setInformativeText('O programa é de uso e distribuição gratuita, mas caso você queira, pode contribuir para futuros projetos doando algum valor. \n\nVocê será redirecionado a minha página de contribuição. Obrigado por usar o programa!')
        donate.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        donate.setIcon(QMessageBox.Icon.Information)

        donate_button01 = donate.button(QMessageBox.Save)
        donate_button01.setText('Desejo contribuir :D')
        donate_button02 = donate.button(QMessageBox.Cancel)
        donate_button02.setText('Voltar')

        donate.exec()

        if donate.clickedButton() == donate_button01:
            webbrowser.open('https://josecauaf.github.io/Projetos/donation-site/')

# Creating the * app -> sys
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()