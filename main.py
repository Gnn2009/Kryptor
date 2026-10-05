import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, 
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QStackedWidget, QLineEdit, QSpinBox
)

# -------------------------------------------------------------------
# FUNCIONES PARA ABRIR Y GUARDAR ARCHIVOS
# -------------------------------------------------------------------
def select_file():
    archivo, _ = QFileDialog.getOpenFileName(window, "KRYPTOR")
    if archivo:
        try:
            with open(archivo, "r", encoding="utf-8") as file:
                input_box.setPlainText(file.read())  
        except Exception as e:
            QMessageBox.critical(window, "Error", f"No se pudo abrir el archivo:\n{e}")

def save_file():
    archivo, _ = QFileDialog.getSaveFileName(window, "KRYPTOR", "", "Archivos de texto (*.txt)")
    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as file:
                file.write(output_box.toPlainText())
        except Exception as e:
            QMessageBox.critical(window, "Error", f"No se pudo guardar el archivo:\n{e}")
def encrypt():
    match methods_list.currentRow():
        case 0: 
            output_box.setPlainText(cesar(input_box.toPlainText()))


def cesar(text):
    encrypted_text = []
    for i in range(len(text)):
        if(97 <= ord(text[i]) <= 122):
            encrypted_text.append(chr(97 + (ord(text[i]) - 97 + spin_cesar.value()) % 26))
        elif(65 <= ord(text[i]) <= 90):
            encrypted_text.append(chr(65 + (ord(text[i]) - 65 + spin_cesar.value()) % 26))
        elif(text[i].isspace()):
            encrypted_text.append(" ")
        else:
            encrypted_text.append(text[i])
    return("".join(encrypted_text))
# -------------------------------------------------------------------
# CONFIGURACIÓN DE LA VENTANA
# -------------------------------------------------------------------
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("KRYPTOR")
app.setWindowIcon(QIcon("icon.png"))
window.resize(900, 600)

main_layout = QHBoxLayout(window)  # Divide la pantalla en Izquierda y Derecha

# -------------------------------------------------------------------
# PANEL IZQUIERDO: Lista de Métodos
# -------------------------------------------------------------------
left_panel = QVBoxLayout()
left_panel.addWidget(QLabel("MÉTODOS"))

methods_list = QListWidget()
methods_list.setFixedWidth(200)
methods_list.addItems([
    "Cifrado César",      # 0
    "Cifrado Vigenère",   # 1
    "Cifrado Atbash",     # 2
    "Cifrado Rail Fence", # 3
    "AES-256"             # 4
])
left_panel.addWidget(methods_list)

main_layout.addLayout(left_panel)

# -------------------------------------------------------------------
# PANEL DERECHO: Área de Trabajo
# -------------------------------------------------------------------
right_panel = QVBoxLayout()

# 1. Clave o Parámetro (Panel cambiante)
stack_params = QStackedWidget()
stack_params.setFixedHeight(30)

spin_cesar = QSpinBox() # César
spin_cesar.setRange(-25, 25)

key_vigenere = QLineEdit() # Vigenère
key_vigenere.setPlaceholderText("Escribe la clave...")

key_aes = QLineEdit() # AES
key_aes.setPlaceholderText("Contraseña secreta...")

stack_params.addWidget(spin_cesar)                   # 0: César
stack_params.addWidget(key_vigenere)                 # 1: Vigenère
stack_params.addWidget(QLabel("Sin clave requerida"))# 2: Atbash
stack_params.addWidget(QLabel("Número de rieles"))   # 3: Rail Fence
stack_params.addWidget(key_aes)                      # 4: AES

right_panel.addWidget(QLabel("Clave / Parámetro:"))
right_panel.addWidget(stack_params)

# 2. Caja de Texto de Entrada
input_box = QTextEdit()
input_box.setStyleSheet("font-size: 15px;")
right_panel.addWidget(QLabel("Texto de Entrada:"))
right_panel.addWidget(input_box)

# 3. Botones principales
buttons_layout = QHBoxLayout()

encrypt_button = QPushButton("ENCRYPT")
decrypt_button = QPushButton("DECRYPT")
save_plain_txt_button = QPushButton("SAVE AS...")
load_button = QPushButton("LOAD")

buttons_layout.addWidget(encrypt_button)
buttons_layout.addWidget(decrypt_button)
buttons_layout.addWidget(save_plain_txt_button)
buttons_layout.addWidget(load_button)

right_panel.addLayout(buttons_layout)

# 4. Caja de Texto de Salida
output_box = QTextEdit()
output_box.setReadOnly(True)
output_box.setStyleSheet("font-size: 15px;")
right_panel.addWidget(QLabel("Resultado:"))
right_panel.addWidget(output_box)

main_layout.addLayout(right_panel)

# -------------------------------------------------------------------
# CONEXIONES Y MOSTRAR VENTANA
# -------------------------------------------------------------------
methods_list.currentRowChanged.connect(stack_params.setCurrentIndex)
methods_list.setCurrentRow(0)

load_button.clicked.connect(select_file)
save_plain_txt_button.clicked.connect(save_file)
encrypt_button.clicked.connect(encrypt)
window.show()
sys.exit(app.exec())