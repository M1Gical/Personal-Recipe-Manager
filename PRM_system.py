import sys
import os
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QListWidget, QHBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

CSV_FILE = "user_data.csv"
RECIPES_CSV_FILE = "recipes_data.csv"

def create_recipes_csv_if_not_exists():
    if not os.path.exists(RECIPES_CSV_FILE):
        with open(RECIPES_CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Title", "Ingredients", "Instructions", "PrepTime", "CookTime"])

def add_recipe_to_csv(username, recipe):
    with open(RECIPES_CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, recipe.title, recipe.ingredients, recipe.instructions, recipe.prep_time, recipe.cook_time])

def load_recipes_for_user(username):
    recipes = []
    create_recipes_csv_if_not_exists()
    with open(RECIPES_CSV_FILE, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == username:
                recipes.append(Recipe(row[1], row[2], row[3], row[4], row[5]))
    return recipes

def create_csv_if_not_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password"])

def add_user_to_csv(username, password):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def check_user_in_csv(username, password):
    with open(CSV_FILE, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
        return False

class Recipe:
    def __init__(self, title, ingredients, instructions, prep_time, cook_time):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.prep_time = prep_time
        self.cook_time = cook_time

    def __str__(self):
        return f"{self.title} - {self.cook_time} min cook"

class LoginWindow(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.switch_to_signup)
        layout.addWidget(self.signup_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if check_user_in_csv(username, password):
            self.main_app.show_main_menu(username)
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def switch_to_signup(self):
        self.main_app.show_signup()

    

class SignUpWindow(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.signup)
        layout.addWidget(self.signup_button)

        self.login_button = QPushButton("Back to Login")
        self.login_button.clicked.connect(self.switch_to_login)
        layout.addWidget(self.login_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            add_user_to_csv(username, password)
            QMessageBox.information(self, "Success", "User registered successfully!")
            self.switch_to_login()
        else:
            QMessageBox.warning(self, "Error", "Invalid input for username or password")

    def switch_to_login(self):
        self.main_app.show_login()
        self.close()

    

class MainMenu(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.recipes = load_recipes_for_user(username)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Personal Recipe Manager")
        self.setFixedSize(800, 400)

        background_label = QLabel(self)
        pixmap = QPixmap("/Users/m1gical/Desktop/Screenshot 2023-11-24 at 12.02.04.png")
        background_label.setPixmap(pixmap)
        background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        layout = QVBoxLayout()
        layout.addStretch()

        self.label_1 = QLabel()
        self.label_1.setText('Personal Recipe Manager')
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    

        font = QFont()
        font.setPointSize(42)
        font.setFamily("Arial Rounded MT Bold")
        self.label_1.setFont(font)

        self.label_1.setStyleSheet("QLabel {"
                                   "    color: white;"
                                   "    border: none;"
                                   "    padding: 10px 20px;"
                                   "    border-radius: 5px;"
                                   "}"
                                   )

        layout.addWidget(self.label_1)
    
        layout.addStretch()


        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_widget.setLayout(button_layout)

        self.view_recipes_button = QPushButton("View Recipes")
        self.view_recipes_button.clicked.connect(self.show_recipes)
        self.view_recipes_button.setStyleSheet("QPushButton {"
                                               "    background-color: #007acc;"
                                               "    color: white;"
                                               "    border: none;"
                                               "    padding: 10px 20px;"
                                               "    border-radius: 5px;"
                                               "}"
                                               "QPushButton:hover {"
                                               "    background-color: #005faa;"
                                               "}")
        self.view_recipes_button.setFixedSize(200, 100)
        font.setPointSize(20)
        self.view_recipes_button.setFont(font)
        button_layout.addWidget(self.view_recipes_button)

        self.add_recipe_button = QPushButton("Add New Recipe")
        self.add_recipe_button.clicked.connect(self.add_recipe)
        self.add_recipe_button.setStyleSheet("QPushButton {"
                                             "    background-color: #28a745;"
                                             "    color: white;"
                                             "    border: none;"
                                             "    padding: 10px 20px;"
                                             "    border-radius: 5px;"
                                             "}"
                                             "QPushButton:hover {"
                                             "    background-color: #218838;"
                                             "}")
        self.add_recipe_button.setFixedSize(200, 100)
        font.setPointSize(20)
        self.add_recipe_button.setFont(font)
        button_layout.addWidget(self.add_recipe_button)

        layout.addWidget(button_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_recipes(self):
        self.recipe_list_window = RecipeListWindow(self.recipes, self)
        self.recipe_list_window.show()

    def add_recipe(self):
        self.recipe_form_window = RecipeFormWindow(self)
        self.recipe_form_window.show()

    def add_recipe_to_list(self, recipe):
        self.recipes.append(recipe)

class RecipeDetailsWindow(QMainWindow):
    def __init__(self, recipe):
        super().__init__()
        self.recipe = recipe
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Recipe Details")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Title:"))
        layout.addWidget(QLabel(self.recipe.title))

        layout.addWidget(QLabel("Ingredients:"))
        layout.addWidget(QLabel(self.recipe.ingredients))

        layout.addWidget(QLabel("Instructions:"))
        layout.addWidget(QLabel(self.recipe.instructions))

        layout.addWidget(QLabel(f"Preparation Time: {self.recipe.prep_time} minutes"))
        layout.addWidget(QLabel(f"Cooking Time: {self.recipe.cook_time} minutes"))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

class RecipeListWindow(QMainWindow):
    def __init__(self, recipes, main_menu):
        super().__init__()
        self.recipes = recipes
        self.main_menu = main_menu
        
        self.init_ui()
        

    def init_ui(self):
        self.setWindowTitle("Recipe List")
        self.setGeometry(100, 100, 400, 300)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.show_recipe_details)

        for recipe in self.recipes:
            self.list_widget.addItem(str(recipe))

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.back_button)

        self.delete_button = QPushButton("Delete Recipe")
        self.delete_button.clicked.connect(self.delete_recipe)
        layout.addWidget(self.delete_button)

        self.search_input = QLineEdit()
        layout.addWidget(QLabel("Search by Ingredient:"))
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_recipes)
        layout.addWidget(self.search_button)

        self.min_time_input = QLineEdit()
        self.max_time_input = QLineEdit()
        
        layout.addWidget(QLabel("Min Time (minutes):"))
        layout.addWidget(self.min_time_input)
        layout.addWidget(QLabel("Max Time (minutes):"))
        layout.addWidget(self.max_time_input)

        self.filter_button = QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.apply_time_filter)
        layout.addWidget(self.filter_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

    def apply_time_filter(self):
        min_time_str = self.min_time_input.text()
        max_time_str = self.max_time_input.text()

        try:
            min_time = int(min_time_str)
            max_time = int(max_time_str)

            filtered_recipes = [recipe for recipe in self.recipes if min_time <= int(recipe.cook_time) <= max_time]

            self.sorted_recipe_list(filtered_recipes)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid time values.")


    def show_recipe_details(self, item):
        selected_recipe = None
        for recipe in self.recipes:
            if str(recipe) == item.text():
                selected_recipe = recipe
                break

        if selected_recipe:
            self.details_window = RecipeDetailsWindow(selected_recipe)
            self.details_window.show()

    def delete_recipe(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            recipe_title = selected_item.text().split(' - ')[0]
            self.remove_recipe_from_csv(recipe_title)
            self.update_recipe_list()

    def remove_recipe_from_csv(self, title):
        with open(RECIPES_CSV_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            recipes = [row for row in reader if row[1] != title]

        with open(RECIPES_CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(recipes)

    def search_recipes(self):
        ingredient = self.search_input.text().lower()
        self.filtered_recipes = [recipe for recipe in self.recipes if ingredient in recipe.ingredients.lower()]
        self.sorted_recipe_list(self.filtered_recipes)

    def sorted_recipe_list(self, recipes_to_show=None):
        self.list_widget.clear()
        if recipes_to_show is None:
            recipes_to_show = self.recipes
        for recipe in recipes_to_show:
            self.list_widget.addItem(str(recipe))


    def update_recipe_list(self):
        self.list_widget.clear()
        self.recipes = load_recipes_for_user(self.main_menu.username)
        for recipe in self.recipes:
            self.list_widget.addItem(str(recipe))

class RecipeFormWindow(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        self.ingredients_input = QTextEdit()
        layout.addWidget(QLabel("Ingredients:"))
        layout.addWidget(self.ingredients_input)

        self.instructions_input = QTextEdit()
        layout.addWidget(QLabel("Instructions:"))
        layout.addWidget(self.instructions_input)

        self.prep_time_input = QLineEdit()
        layout.addWidget(QLabel("Preparation Time (minutes):"))
        layout.addWidget(self.prep_time_input)

        self.cook_time_input = QLineEdit()
        layout.addWidget(QLabel("Cooking Time (minutes):"))
        layout.addWidget(self.cook_time_input)

        self.save_button = QPushButton("Save Recipe")
        self.save_button.clicked.connect(self.save_recipe)
        self.save_button.setStyleSheet("QPushButton {"
                                       "    background-color: #007acc;"
                                       "    color: white;"
                                       "    border: none;"
                                       "    padding: 10px 20px;"
                                       "    border-radius: 5px;"
                                       "}"
                                       "QPushButton:hover {"
                                       "    background-color: #005faa;"
                                       "}")
        layout.addWidget(self.save_button)

        self.upload_button = QPushButton("Upload Recipes")
        self.upload_button.clicked.connect(self.upload_recipes)
        layout.addWidget(self.upload_button)

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.clicked.connect(self.close)
        layout.addWidget(self.back_button)

        self.setLayout(layout) 

    def save_recipe(self):
        username = self.main_menu.username

        title = self.title_input.text()
        ingredients = self.ingredients_input.toPlainText()
        instructions = self.instructions_input.toPlainText()
        prep_time = self.prep_time_input.text()
        cook_time = self.cook_time_input.text()

        new_recipe = Recipe(title, ingredients, instructions, prep_time, cook_time)

        add_recipe_to_csv(username, new_recipe)

        self.main_menu.add_recipe_to_list(new_recipe)

        self.close()

    def upload_recipes(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;JSON Files (*.json)")
        if file_name:
            self.parse_and_add_recipes(file_name)

    def parse_and_add_recipes(self, file_name):
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                new_recipe = Recipe(row[1], row[2], row[3], row[4], row[5])
                self.main_menu.add_recipe_to_list(new_recipe)
                add_recipe_to_csv(self.main_menu.username, new_recipe) 

class MainApp:
    def __init__(self):
        self.login_window = LoginWindow(self)
        self.signup_window = SignUpWindow(self)
        self.main_menu = None

    def show_main_menu(self, username):
        self.main_menu = MainMenu(username)
        self.main_menu.show()

    def show_login(self):
        self.login_window.show()

    def show_signup(self):
        self.signup_window.show()

def main():
    create_csv_if_not_exists()
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show_login()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()