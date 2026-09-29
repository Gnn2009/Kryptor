import sys

from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QFileDialog, QMessageBox, QLabel

def select_file():
    archivo, _ = QFileDialog.getOpenFileName(
        window,
        "KRYPTOR",
    )

    if archivo:
        print("Archivo seleccionado:", archivo)
    try:
        with open(archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            text_box.setPlainText(contenido)     
    except Exception as e:
        QMessageBox.critical("Error", f"No se pudo abrir el archivo:\n{e}")
def save_file():
    archivo, _ = QFileDialog.getSaveFileName(
        window,
        "KRYPTOR",
        "",
        "Archivos de texto (*.txt)"
    )
    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as archivo:
                archivo.write(text_box.toPlainText())
            print("Archivo guardado:", archivo)
        except Exception as e:
            QMessageBox.critical(
                window,
                "Error",
                f"No se pudo guardar el archivo:\n{e}"
            )

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("KRYPTOR")
window.resize(800, 700)
text_box = QTextEdit(window)
text_box.resize(600, 300)
text_box.move(10, 10)
text_box = QTextEdit(window)
text_box.resize(600, 300)
text_box.move(10, 10)
text_box.setStyleSheet("""
    QTextEdit {
        font-family: monospace;
        font-size: 16px;
    }
""")
loadutton = QPushButton("LOAD", window)
loadutton.resize(80, 20)
loadutton.move(10, 320)
savePlainTxtButton = QPushButton("SAVE AS...", window)
savePlainTxtButton.resize(80, 20)
savePlainTxtButton.move(90, 320)
window.show()

loadutton.clicked.connect(select_file)
savePlainTxtButton.clicked.connect(save_file)
sys.exit(app.exec())