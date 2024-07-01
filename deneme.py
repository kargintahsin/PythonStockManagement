import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
from PyQt5.QtGui import QIntValidator

class StockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stok Takip Uygulaması")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
        self.load_data()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Form Layout
        self.form_layout = QFormLayout()
        self.product_name_input = QLineEdit()
        self.product_quantity_input = QLineEdit()
        self.product_unit_input = QComboBox()
        self.int_validator = QIntValidator()
        self.product_quantity_input.setValidator(self.int_validator)
        self.form_layout.addRow("Ürün Adı:", self.product_name_input)
        self.form_layout.addRow("Ürün Miktarı:", self.product_quantity_input)
        self.form_layout.addRow("Birim:", self.product_unit_input)
        self.options = ["Metre", "Adet", "Kilo"]
        self.product_unit_input.addItems(self.options)

        # Search Layout
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Ara")
        self.search_button.clicked.connect(self.search_product)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        
        # Buttons Layout
        self.buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Ekle")
        self.update_button = QPushButton("Güncelle")
        self.delete_button = QPushButton("Sil")

        # Button styles
        self.add_button.setStyleSheet("background-color: green; color: white;")
        self.update_button.setStyleSheet("background-color: blue; color: white;")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.search_button.setStyleSheet("background-color: #2F4F4F; color: white;")

        self.add_button.clicked.connect(self.add_product)
        self.update_button.clicked.connect(self.update_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.delete_button)
        
        # Table Layout
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ürün Adı", "Ürün Miktarı", "Ürün Birimi"])
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.search_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.table)

    def load_data(self):
        if os.path.exists("products.json"):
            with open("products.json", "r", encoding="utf-8") as file:
                products = json.load(file)
                self.refresh_table(products)
        else:
            self.refresh_table([])

    def save_data(self, products):
        with open("products.json", "w", encoding="utf-8") as file:
            json.dump(products, file, ensure_ascii=False, indent=4)

    def add_product(self):
        product_name = self.product_name_input.text()
        product_quantity = self.product_quantity_input.text()
        product_unit = self.product_unit_input.currentText()
        if product_name and product_quantity:
            new_product = [product_name, product_quantity, product_unit]
            products = self.get_all_products()
            products.append(new_product)
            self.save_data(products)
            self.refresh_table(products)
            self.product_name_input.clear()
            self.product_quantity_input.clear()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")

    def update_product(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            product_name = self.product_name_input.text()
            product_quantity = self.product_quantity_input.text()
            product_unit = self.product_unit_input.currentText()
            if product_name and product_quantity:
                products = self.get_all_products()
                products[selected_row] = [product_name, product_quantity, product_unit]
                self.save_data(products)
                self.refresh_table(products)
                self.product_name_input.clear()
                self.product_quantity_input.clear()
            else:
                QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellenecek ürünü seçin.")

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            products = self.get_all_products()
            del products[selected_row]
            self.save_data(products)
            self.refresh_table(products)
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek ürünü seçin.")

    def search_product(self):
        search_term = self.search_input.text().lower()
        products = self.get_all_products()
        filtered_products = [product for product in products if search_term in product[0].lower()]
        self.refresh_table(filtered_products)

    def refresh_table(self, products):
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product[0]))
            self.table.setItem(row, 1, QTableWidgetItem(product[1]))
            self.table.setItem(row, 2, QTableWidgetItem(product[2]))

    def get_all_products(self):
        if os.path.exists("products.json"):
            with open("products.json", "r", encoding="utf-8") as file:
                return json.load(file)
        return []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())
