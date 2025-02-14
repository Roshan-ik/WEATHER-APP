import sys
import requests
from PyQt5.QtWidgets import (QApplication,QMainWindow,
                             QLayout,QWidget,QVBoxLayout,QLineEdit,
                             QPushButton,QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from requests import HTTPError, RequestException


class Weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("ENTER CITY NAME",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button=QPushButton("GET WEATHER",self)
        self.temperature_label=QLabel(self)
        self.emoji_label = QLabel("🌞",self)
        self.description_label =QLabel(self)
        self.init()



    def init(self):
        self.setWindowTitle("WEATHER APP")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)





        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.city_input.setFont(QFont("Arial", 30))

        self.setStyleSheet("""
        QLabel,QPushButton{
        font-family:calibri;
        
        }
        QLabel#city_label{
        font-size:40px;
        
        font-weight:bold;
        }
        QLabelEdit#city_input{
        font-size:50px;
        height: 60px;      
        width: 400px;        
        }
        QPushButton#get_weather_button{
        font-size:30px;
        font-weight:bold;
        }
        QLabel#temperature_label{
        font-size:70px;
        
        }
        QLabel#emoji_label{
        font-size:100px;
        font-family: Segoe UI emoji
        }
        QLabel#description_label{
        font-size:50px;
        }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)




    def get_weather(self):
        api_key = "cee03ae3d0e70e8bc69ded9d8714ad9a"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()            #use to raise an exception for status code cause our try method usually dont do thay so we have to do it manually
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:                    #status code which is 400 or 500 which means error
            match response.status_code:
                case 400:
                    self.display_error("INVALID REQUEST\n PLEASE CHECK YOUR INPUT")
                case 401:
                    self.display_error("UNAUTHORIZED \n INVALID IP")
                case 403:
                    self.display_error("FORBIDDEN\n ACCESS IS DENIED")
                case 404:
                    self.display_error("NOT FOUND\n CITY NOT FOUND")
                case 500:
                    self.display_error("INTERNAL SERVER ERROR\n PLEASE TRY AGAIN LATER")
                case 502:
                    self.display_error("BAD GATEWAY\n INVALID RESPONSE FROM THE SERVER")
                case 503:
                    self.display_error("SERVICE UNAVAILABLE\n SERVER IS DOWN")
                case 504:
                    self.display_error("GATEWAY TIMEOUT\n PLEASE CHECK YOUR INPUT")
                case _:
                    self.display_error(f"HTTP ERROR OCCURRED\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("CONNECTION ERRROR:\nPLEASE CHECK YOUR INTERNET CONNECTION")
        except requests.exceptions.Timeout:
            self.display_error("TIMEOUT ERROR:\n THE REQUEST TIME OUT")
        except requests.exceptions.TooManyRedirects:
            self.display_error("TOO MANY REDIRECTS:\n CHECK THE URL")
        except requests.exceptions.RequestException  as req_error:
            self.display_error(f"REQUEST ERROR:\n {req_error}")




    def display_error(self,message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.emoji_label.clear()
        self.description_label.clear()


    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temperature_K = data["main"]["temp"]
        temperature_C = temperature_K - 273.15
        temperature_F = (temperature_K * 9/5) - 459.6
        weather_id = data["weather"][0]["id"]
        weather_discription = data["weather"][0]["description"]
        self.temperature_label.setText(f"{temperature_F:.0f}°F")
        self.emoji_label.setText(self.weather_emoji(weather_id))
        self.description_label.setText(weather_discription)



    @staticmethod                                          #static method belongs to a class that doesnt required any instance specific data from previous dataa
    def weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return  "🌋"
        elif weather_id == 721:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return"☁️"


if __name__ == "__main__":
    app =QApplication(sys.argv)
    weather_app= Weatherapp()
    weather_app.show()
    sys.exit(app.exec_())