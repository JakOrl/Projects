# Author: Jakub Orlowski

# Sys import so we can exit the app well
import sys
# Import requests to pull from API
import requests
# PyQt5 is the GUI of choice im learning now
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QLabel, QWidget

# Creating weather app class
class WeatherApp(QMainWindow):
    def __init__(self):
        # Creating the app window
        super().__init__()
        # Setting window title
        self.setWindowTitle("Weather App Project")
        # Setting size of window
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
        # Creating a field for the user to answer the question. Single line answer
        self.city_entry = QLineEdit()
        # Creating a get weather button
        self.search_button = QPushButton("Get Weather")
        # Empty space for the result of the search to go
        self.weather_result = QLabel("")

        ## Adding the content to the layout

        self.layout.addWidget(self.city_label)
        self.layout.addWidget(self.city_entry)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.weather_result)

        ## Connecting the "get weather" button to a click signal so it can start a event
        self.search_button.clicked.connect(self.get_weather)

    # Defining the function that calls the API's info
    def get_weather(self):
        # Setting the API info im using
        api_key = "a504042bd0c84addbc9203608252208"
        base_url = "http://api.weatherapi.com/v1/current.json"
        city = self.city_entry.text()

        # If button is clicked with nothing inside it
        if not city:
            self.weather_result.setText("Please enter a city name.")
            return

        # Complete version of the URL that is going to be called
        complete_url = f'{base_url}?key={api_key}&q={city}'

        # The request and response to and from the API
        try:
            response = requests.get(complete_url)
            data = response.json()
            print(data)

            # If 404 is given as a code in the json it will prompt the else statement otherwise itll pull the data
            if "error" not in data:
                main_data = data["current"]
                weather_desc = main_data["condition"]["text"]
                temp = main_data["temp_c"]
                humidity = main_data["humidity"]
                #Condensing to one f string
                weather_info = f"Temperature: {temp}c\nHumidity:{humidity}\nDescription:{weather_desc.capitalize()}"
                self.weather_result.setText(weather_info)

            else:
                self.weather_result.setText("City not Found.")
        #In case there is a connection issue
        except requests.exceptions.RequestException:
            self.weather_result.setText("Error connecting to API. Check your internet connection")

## Running the application
if __name__ == "__main__":
    # Creates Qapp instance
    app = QApplication(sys.argv)
    # Points at the weather app class as the info to be inside the Qap
    window = WeatherApp()
    window.show()
    #Program shuts down on use shutdown of the window
    sys.exit(app.exec_())

