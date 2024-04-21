# DAH-Report-Remote-Sensing-System-2022
The suplimentry material for the remote sensing system. 

A University of Edinburgh 4th year course in finished Dec 2022

Last updated 1st Dec 2022

## Pupose of the Project
  This project uses an Arduino to receive data from three sensors, a humidity, temperature and water level sensor. Using an Adafruit HUZZAH ESP8266 WiFi micro-controller breakout, the sensors' data is uploaded to the local server that can be accessed by anyone connected to it with the correct IP. This data is then interpreted and analysed by python, which outputs visual representations of the data in graph forms. This data taken by the sensors is also complimented with data from weather stations in Edinburgh, comparing the data taken from the past month - or any month the user chooses.

#### File: project.py
  This file is the most important; it brings all the data together and visualises it in the form of graphs for the user to interpret. There are specifics on how you can edit the code in the file's comments, such as changing the IP or directory to save the data if your hotspot or device changes, respectively. To retrieve the data on the local server, this file calls a function named get_tempNhum in our_sensor_data.py. The function returns the three measurements made by the three sensors mentioned above.

#### File: our_sensor_data.py
  The file used to retrieve the data from the local server contains the principle function for this project, get_tempNhum, with only the input of an IP address. When experimenting with the readings, we found that the measurements would jump around, especially for the water level sensor. The code collects ten measurements with gaps of 0.25s and returns each sensor's average values. This function is called in project.py.

#### File: weatherstation arduino.cpp
  The C++ code must be uploaded to the Adafruit HUZZAH ESP8266 WiFi micro-controller breakout using the CP2102 USB-TTL UART Module. It contains the code to read the sensors' data and upload it to the local server. The code can be uploaded using the Arduino app on a windows PC.
  
#### Files with .png or .jpg
  These are just for example purposes, to show what was done in the project. Not necessary to be able to repicate the project but aids it.
