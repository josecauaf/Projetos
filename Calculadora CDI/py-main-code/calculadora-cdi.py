from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QFont
from decimal import Decimal
import locale
import webbrowser
import sys
import os

di_tax = Decimal(10.40) # Current DI rate, update if needed

# Setting a variable for dark mode stylesheet
dark_mode_style = '''
                           QMainWindow#mainwindow{
                           background-color: #262929}

                           QLabel#label01, #label02, #label03, #label11{
                           color: #e0e0e0}

                           QLabel#label04, #label05, #label06, #label07, #label08, #label09{
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
                           
                           QPushButton#button01, #button02{
                           color: #3a3a3a;
                           text-align: center;
                           background-color: #ababab;
                           border-style: solid;
                           border-width: 2px;
                           border-color : gray;
                           font: bold 14px;
                           padding: 6px}

                           QPushButton#button01:pressed, #button02:pressed {
                           background-color: #868686;
                           border-style: inset}

                           QPushButton#button03{
                           color: #0084ff;
                           background-color: #d6d6d6;
                           border-style: solid;
                           border-width: 1px;
                           border-color: #0084ff;
                           border-radius: 3px}

                           QPushButton#button03:pressed {
                           background-color: #afb3b0;
                           border-style: inset}
                                               
                           QPushButton#button04{
                           color: #525252;
                           background-color: #e3e3e3;
                           border-style: solid;
                           border-width: 1px;
                           border-color: #ffffff;
                           border-radius: 3px}
                                               
                           QPushButton#button04:pressed {
                           background-color: #afb3b0;
                           border-radius: 5px;
                           border-style: inset}
'''

# Setting a variable for light mode style sheet
light_mode_style = '''
                            QMainWindow#mainwindow{
                            background-color: #f2f2f2}

                            QLabel#label01, #label02, #label03, #label11{
                            color: #424242}

                            QLabel#label04, #label05, #label06, #label07, #label08, #label09{
                            color: #424242;
                            border: 2px solid #5b5b5b;}

                            QLineEdit{ 
                            color: #474747; 
                            background-color: #c2c2c2;
                            selection-color: white;
                            selection-background-color: #474747 }

                            QSpinBox{
                            color: #2b2b2b; 
                            background-color: #c2c2c2;
                            selection-color: white;
                            selection-background-color: #474747}
                           
                            QPushButton#button01, #button02{
                            color: #3a3a3a;
                            text-align: center;
                            background-color: #ababab;
                            border-style: solid;
                            border-width: 2px;
                            border-color : gray;
                            font: bold 14px;
                            padding: 6px}

                            QPushButton#button01:pressed, #button02:pressed {
                            background-color: #868686;
                            border-style: inset}

                            QPushButton#button03{
                            color: #0084ff;
                            background-color: #d6d6d6;
                            border-style: solid;
                            border-width: 1px;
                            border-color: #0084ff;
                            border-radius: 3px}

                            QPushButton#button03:pressed {
                            background-color: #afb3b0;
                            border-style: inset}
                                                   
                            QPushButton#button04{
                            color: #fafafa;
                            background-color: #919191;
                            border-style: solid;
                            border-width: 1px;
                            border-color: #393939;
                            border-radius: 3px}
                                                   
                            QPushButton#button04:pressed {
                            background-color: #afb3b0;
                            border-radius: 5px;
                            border-style: inset}
'''

# Setting a locale for BRL currency as a value
locale.setlocale(locale.LC_ALL, 'C')

# Creating the main app window as a class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting the "calculadora_cdi" function start variables
        self.cdi_value = 0
        self.main_value = 0
        self.months = 0 
        self.current_mode_number = 0


        # Main window configuration
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        self.icon = QIcon(icon_path) 

        self.setWindowTitle('Calculadora CDI') # Title
        self.setWindowIcon(self.icon) # Setting the main window icon
        self.setGeometry(190, 195, 1000, 400) # Setting the coordinates (x, y, #, #) and minimal size (#, #, w, h)]
        self.setObjectName('mainwindow') # Setting an ID to self.QMainWindow

        self.show() # Just to show the main app window
    
        # Styling Widgets
        self.current_mode = self.setStyleSheet(dark_mode_style)

        # Label storage
        label01 = QLabel('Coloque aqui seu percentual CDI')
        label01.setObjectName('label01') # Setting a name to a Label, QLineEdit, etc, we can use it on stylesheet for exemple.

        label02 = QLabel('Coloque aqui o valor a ser calculado')
        label02.setObjectName('label02')

        label03 = QLabel('Em quantos meses?')
        label03.setObjectName('label03')

        self.label04 = QLabel(f'Taxa aplicada do IR -> 0%')
        self.label04.setObjectName('label04')
        self.label04.setFixedWidth(600)

        self.label05 = QLabel(f'Rendimento Total -> R$0')
        self.label05.setObjectName('label05')
        self.label05.setFixedWidth(600)

        self.label06 = QLabel(f'Taxa do CDI inserido por mês -> 0%')
        self.label06.setObjectName('label06')
        self.label06.setFixedWidth(600)

        self.label07 = QLabel(f'Rendimento bruto de juros -> R$0')
        self.label07.setObjectName('label07')
        self.label07.setFixedWidth(600)

        self.label08 = QLabel('Taxa do IR -> R$0')
        self.label08.setObjectName('label08')
        self.label08.setFixedWidth(600)

        self.label09 = QLabel('Rendimento com IR descontado -> R$0')
        self.label09.setObjectName('label09')
        self.label09.setFixedWidth(600)

        self.label10 = QLabel('<a href=''''https://github.com/josecauaf>Meu perfil no GitHub</a>''')
        self.label10.setObjectName('label10')
        self.label10.setOpenExternalLinks(True)

        self.label11 = QLabel('Versão atual (0.8.0 Beta)')
        self.label11.setObjectName('label11')

        # Input (QLineEdit) storage
        self.input01 = QLineEdit()
        self.input01.setMaxLength(30)
        self.input01.setPlaceholderText('Insira sua porcentagem do CDI (Ex.: 100, 94.88)')

        self.input02 = QLineEdit()
        self.input02.setMaxLength(30)
        self.input02.setPlaceholderText('Insira o valor usando apenas números e/ou ponto(s) (Ex.: 120, 540.345)')

        self.input03 = QSpinBox()
        self.input03.setMinimum(1)

        # Buttons storage
        self.button01 = QPushButton('Como utilizar?')
        self.button01.setObjectName('button01')
        self.button01.clicked.connect(self.help_button)

        self.button02 = QPushButton('Calcular')
        self.button02.setFixedWidth(300)
        self.button02.setObjectName('button02')
        self.button02.clicked.connect(self.cdi_calculator)

        self.button03 = QPushButton('Deseja contribuir?')
        self.button03.setObjectName('button03')
        self.button03.setFixedSize(200, 20)
        self.button03.clicked.connect(self.donate)

        self.button04 = QPushButton('Mudar para o Light Mode')
        self.button04.setObjectName('button04')
        self.button04.setFixedSize(200, 20)
        self.button04.clicked.connect(self.changing_current_mode)

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
        self.label08.setFont(label_font01)
        self.label09.setFont(label_font01)

        self.input01.setFont(label_font01) # Inputs
        self.input02.setFont(label_font01)
        self.input03.setFont(label_font01)
        
        # Creating the main Layout
        layout01 = QVBoxLayout()

        # Creating secondary Layouts
        layout02 = QHBoxLayout()                 

        layout03 = QHBoxLayout()
        layout03.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        ) # Center alignment

        layout04 = QHBoxLayout()
        layout04.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        ) # Center alignment

        layout05 = QHBoxLayout()
        layout05.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        ) # Center alignment

        layout06 = QHBoxLayout()
        #layout06.setAlignment(
        #    Qt.AlignmentFlag.AlignCenter
        #) # Center alignment

        # Adding widgets to the main Layout in order
        layout02.addWidget(label01, alignment=Qt.AlignmentFlag.AlignLeft) # Adding secondary Layout widgets first
        layout02.addWidget(self.button01, alignment=Qt.AlignmentFlag.AlignRight) # Making a alignment to make it responsivity
        layout01.addLayout(layout02) # Adding the secondary Layout first

        layout01.addWidget(self.input01)
        layout01.addWidget(label02)
        layout01.addWidget(self.input02)
        layout01.addWidget(label03)
        layout01.addWidget(self.input03)
        layout01.addWidget(self.button02, alignment=Qt.AlignmentFlag.AlignCenter) # Center alignment

        # Adding secondary Layouts to Main Layout
        layout01.addLayout(layout03)
        layout01.addLayout(layout04)
        layout01.addLayout(layout05)
        layout01.addLayout(layout06)

        # Adding widgets to secondary Layouts in order
        layout03.addWidget(self.label04, alignment=Qt.AlignmentFlag.AlignLeft) # Left alignment
        layout03.addWidget(self.label05)

        layout04.addWidget(self.label06)
        layout04.addWidget(self.label07)

        layout05.addWidget(self.label08)
        layout05.addWidget(self.label09)

        layout06.addWidget(self.label10, alignment=Qt.AlignmentFlag.AlignLeft)
        layout06.addWidget(self.button03)
        layout06.addWidget(self.button04)
        layout06.addWidget(self.label11, alignment=Qt.AlignmentFlag.AlignRight)

        layout01.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        ) # Center/Top alignment

        # Creating a container
        container = QWidget()
        container.setLayout(layout01) # Setting the Main Layout to the container

        self.setCentralWidget(container) # Centralizing the container

    def help_button(self): # Creating a function to a help button, that helps the user of how to use the app
        help_msg = QMessageBox()
        help_msg.setWindowTitle('Como utilizar a calculadora')
        help_msg.setText('Olá! Irei lhe auxiliar na utilização da calculadora')
        help_msg.setWindowIcon(self.icon)
        help_msg.setInformativeText('''
O programa recebe 3 dados, sendo eles a porcentagem CDI, o valor a ser calculado e a quantidade de meses.\n
1. Primeiro insira sua porcentagem CDI no campo CDI\n(Exemplo: 1-> 100, 2-> 94.5)\nOBS: Utilize somente pontos.\n
2. Depois, insira o valor desejável a ser calculado no campo Valor\n(Exemplo: 1-> 100, 2-> 545.340)\nOBS: Utilize somente pontos, vírgulas não são aceitas, ou seja, o campo CDI não aceita centavos como valor (545.340 = R$ 545.340,00) mas o resultado poderá ter centavos.\n
3. E finalmente, insira a quantidade de meses desejável (insira ou alterne no final do campo)\n1 Mês = 30 dias\n OBS: O imposto de renda é mostrado de acordo com o mês atual do imposto. (Levando em consideração que o imposto de 22,5% é aplicado nos primeiros 180 dias, o imposto de 20% será aplicado no dia 181)\n
Informações adicionais: 1. O programa é de uso e distribuição totalmente gratuíta, sendo dispensado a cobrança de valores, tarifas, taxas, impostos, assinaturas, créditos, recargas e todo tipo de cobrança para o uso do programa, use sempre a versão original para melhor desempenho. 2. A contribuição existe de fato, mas é totalmente voluntária, sendo possível acessar no aplicativo principal através do botão "Deseja contribuir?", e lembre-se, é uma ação totalmente voluntária, não será enviado e-mail, sms ou qualquer outro tipo de comunicação solicitando contribuição, favor, sempre verifique as fontes e evite golpes. 3. Caso queira entrar em contato comigo, favor enviar e-mail para: asrieldremdev@gmail.com
''')
        help_msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        help_msg.setIcon(QMessageBox.Icon.Information)
        
        help_button01 = help_msg.button(QMessageBox.Save)
        help_button01.setText('OK! Entendi :D')
        help_button02 = help_msg.button(QMessageBox.Cancel)
        help_button02.setText('Voltar')

        help_msg.exec()
    
    def changing_current_mode(self): # Creating a function that changes modes between dark and light
        if self.current_mode_number == 0:
            self.current_mode_number = 1
            self.button04.setText('Mudar para o Dark Mode')
            self.current_mode = self.setStyleSheet(light_mode_style)
        elif self.current_mode_number == 1:
            self.current_mode_number = 0
            self.button04.setText('Mudar para o Light Mode')
            self.current_mode = self.setStyleSheet(dark_mode_style)
            
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
            try: # waiting comment... (updated)
                self.main_value = self.value02.replace('.', '')
                self.main_value = int(self.main_value)
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

        # Calculation that performs data processing, reduction and conversion
        reduced_cdi = self.cdi_value / 100 * di_tax
        monthly_tax = reduced_cdi / 12 / 100
        monthly_tax = Decimal(monthly_tax)
        monthly_tax_illustration = reduced_cdi / 12
        result = self.main_value * (1 + monthly_tax) ** self.months

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
        self.label04.setText(f'Taxa aplicada do IR -> {ir_tax_demo}%')
        self.label05.setText(f'Rendimento Total -> R${result:,.2f}')
        self.label06.setText(f'Taxa do CDI inserido por mês -> {monthly_tax_illustration:.2f}%')
        self.label07.setText(f'Rendimento bruto de juros -> R${only_tax:,.2f}')
        self.label08.setText(f'Taxa do IR -> R${ir_result:.2f}')
        self.label09.setText(f'Rendimento com IR descontado -> R${ir_liquid:,.2f}')

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