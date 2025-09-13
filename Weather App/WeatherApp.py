# Author: Jakub Orlowski

#Getting API key from enviromental Variable
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get('WEATHER_API_KEY')
# Sys import so we can exit the app well
import sys
# Import requests to pull from API
import requests
# PyQt5 is the GUI of choice im learning now
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize


# Creating weather app class
class WeatherApp(QMainWindow):
    def __init__(self):
        # Creating the app window
        super().__init__()
        # Setting window title
        self.setWindowTitle("Weather App Project")
        # Setting the initial size of the window, now resizable
        self.setGeometry(100, 100, 400, 300)

        # A "box" for our other widgets using QWidget instance
        self.central_Widget = QWidget()
        # Central widget will be main content area
        self.setCentralWidget(self.central_Widget)
        # Vboxlayout makes a vertical layout, like a column
        self.layout = QVBoxLayout()
        # Applying the Layout setting to the central widget
        self.central_Widget.setLayout(self.layout)

        ## Creating content

        # Creating a label
        self.city_label = QLabel("Enter City:")
        self.city_label.setAlignment(Qt.AlignCenter)
        # Creating a field for the user to answer the question. Single line answer
        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("e.g; London, Tokyo")
        # Creating a get weather button
        self.search_button = QPushButton("Get Weather")
        # Empty space for the result of the search to go
        self.weather_result = QLabel("Enter a city to see the weather!")
        self.weather_result.setAlignment(Qt.AlignCenter)
        # Place-Holder for the weather icon from the API
        self.weather_icon_label = QLabel()
        self.weather_icon_label.setAlignment(Qt.AlignCenter)


        ## Adding the content to the layout

        self.layout.addWidget(self.city_label)
        self.layout.addWidget(self.city_entry)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.weather_result)
        self.layout.addWidget(self.weather_icon_label)

        ## Connecting the "get weather" button to a click signal so it can start a event
        self.search_button.clicked.connect(self.get_weather)

    def resizeEvent(self, event):
        # Called when window is resized
        # Get new window size
        new_width = event.size().width()

        # Calc a new font size based on window size
        new_font_size = max(16, int(new_width / 16))
        self.weather_result.setStyleSheet(f"font-size: {new_font_size}px; font-weight: bold;")

        # call parents class to make it behave properly
        super().resizeEvent(event)



    # Defining the function that calls the API's info
    def get_weather(self):

        #Setting button and result lable to "loading" state
        self.search_button.setEnabled(False)
        self.search_button.setText("Loading...")
        self.weather_result.setText("Fetching Weather Data...")
        self.weather_icon_label.clear()


        # Setting the API info im using
        base_url = "http://api.weatherapi.com/v1/current.json"
        city = self.city_entry.text()

        # If button is clicked with nothing inside it
        if not city:
            self.weather_result.setText("Please enter a city name.")
            self.search_button.setEnabled(True)
            self.search_button.setText("Get Weather")
            return

        # Complete version of the URL that is going to be called
        complete_url = f'{base_url}?key={api_key}&q={city}'

        # The request and response to and from the API
        try:
            response = requests.get(complete_url)
            data = response.json()

            # If 404 is given as a code in the json it will prompt the else statement otherwise itll pull the data
            if "error" not in data:
                main_data = data["current"]
                weather_desc = main_data["condition"]["text"]
                temp = main_data["temp_c"]
                humidity = main_data["humidity"]
                weather_icon_url = f'http:{data["current"]["condition"]["icon"]}'

                #Download icon and set it
                image_data = requests.get(weather_icon_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.weather_icon_label.setPixmap(pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation))

                #Condensing to one f string
                weather_info = f"Temperature: {temp}c\nHumidity:{humidity}\nDescription:{weather_desc.capitalize()}"
                self.weather_result.setText(weather_info)

            else:
                self.weather_result.setText("City not Found.")
                self.weather_icon_label.clear()
        #In case there is a connection issue
        except requests.exceptions.RequestException:
            self.weather_result.setText("Error connecting to API. Check your internet connection")
            self.weather_icon_label.clear()
        finally:
            self.search_button.setEnabled(True)
            self.search_button.setText("Get Weather")

## Running the application
if __name__ == "__main__":
    # Creates Q-app instance
    app = QApplication(sys.argv)
    #Open and read style sheet
    with open("style.css", "r") as f:
        app.setStyleSheet(f.read())
    # Points at the weather app class as the info to be inside the Qap
    window = WeatherApp()
    window.show()
    #Program shuts down on use shutdown of the window
    sys.exit(app.exec_())

