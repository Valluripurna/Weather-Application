import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

class WeatherApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # API key for OpenWeatherMap (sign up at openweathermap.org to get your free API key)
        self.api_key = "YOUR_API_KEY_HERE"  # Replace with your API key
        
        # Create and set style
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))
        self.style.configure('Info.TLabel', font=('Helvetica', 12))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self.root, padding="20 20 20 0")
        title_frame.pack(fill=tk.X)
        
        ttk.Label(
            title_frame,
            text="Weather Forecast",
            style='Title.TLabel'
        ).pack()
        
        # Search frame
        search_frame = ttk.Frame(self.root, padding="20")
        search_frame.pack(fill=tk.X)
        
        self.city_var = tk.StringVar()
        city_entry = ttk.Entry(
            search_frame,
            textvariable=self.city_var,
            font=('Helvetica', 12),
            width=30
        )
        city_entry.pack(side=tk.LEFT, padx=(0, 10))
        city_entry.insert(0, "Enter city name...")
        city_entry.bind('<FocusIn>', lambda e: city_entry.delete(0, 'end'))
        
        ttk.Button(
            search_frame,
            text="Search",
            command=self.get_weather
        ).pack(side=tk.LEFT)
        
        # Weather info frame
        self.weather_frame = ttk.Frame(self.root, padding="20")
        self.weather_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create labels for weather information
        self.create_info_labels()
        
    def create_info_labels(self):
        # Temperature
        self.temp_label = ttk.Label(
            self.weather_frame,
            text="",
            style='Info.TLabel'
        )
        self.temp_label.pack(pady=10)
        
        # Feels like
        self.feels_like_label = ttk.Label(
            self.weather_frame,
            text="",
            style='Info.TLabel'
        )
        self.feels_like_label.pack(pady=10)
        
        # Weather description
        self.desc_label = ttk.Label(
            self.weather_frame,
            text="",
            style='Info.TLabel'
        )
        self.desc_label.pack(pady=10)
        
        # Humidity
        self.humidity_label = ttk.Label(
            self.weather_frame,
            text="",
            style='Info.TLabel'
        )
        self.humidity_label.pack(pady=10)
        
        # Wind speed
        self.wind_label = ttk.Label(
            self.weather_frame,
            text="",
            style='Info.TLabel'
        )
        self.wind_label.pack(pady=10)
        
        # Last updated
        self.update_label = ttk.Label(
            self.weather_frame,
            text="",
            style='Info.TLabel'
        )
        self.update_label.pack(pady=10)
        
    def get_weather(self):
        city = self.city_var.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showerror("Error", "Please enter a city name!")
            return
            
        try:
            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # Extract weather information
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                description = data['weather'][0]['description']
                
                # Update labels
                self.temp_label.config(
                    text=f"Temperature: {temp:.1f}°C"
                )
                self.feels_like_label.config(
                    text=f"Feels like: {feels_like:.1f}°C"
                )
                self.desc_label.config(
                    text=f"Weather: {description.capitalize()}"
                )
                self.humidity_label.config(
                    text=f"Humidity: {humidity}%"
                )
                self.wind_label.config(
                    text=f"Wind Speed: {wind_speed} m/s"
                )
                self.update_label.config(
                    text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"Error fetching weather data: {data['message']}"
                )
                
        except requests.RequestException as e:
            messagebox.showerror(
                "Error",
                f"Network error: {str(e)}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred: {str(e)}"
            )

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if _name_ == "_main_":
    main()