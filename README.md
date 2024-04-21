# Physics-Bsc
My reports and notable things I have done during my degree at the University of Edinburgh.


## DAH-Report: A Remote Weather Sensing System
The supplementary material for the remote sensing system. A 3rd year physics course. A 4th year course finished in December 2022.

### Purpose of the Project
This project uses an Arduino to receive data from three sensors, a humidity, temperature and water level sensor. Using an Adafruit HUZZAH ESP8266 WiFi micro-controller breakout, the sensors' data is uploaded to the local server that can be accessed by anyone connected to it with the correct IP. This data is then interpreted and analysed by Python, which outputs visual representations of the data in graph forms. This data taken by the sensors is also complimented with data from weather stations in Edinburgh, comparing the data taken from the past month - or any month the user chooses.

##### File: project.py
This file is the most important; it brings all the data together and visualises it in the form of graphs for the user to interpret. There are specifics on how you can edit the code in the file's comments, such as changing the IP or directory to save the data if your hotspot or device changes, respectively. To retrieve the data on the local server, this file calls a function named get_tempNhum in our_sensor_data.py. The function returns the three measurements made by the three sensors mentioned above.

##### File: our_sensor_data.py
The file used to retrieve the data from the local server contains the principle function for this project, get_tempNhum, with only the input of an IP address. When experimenting with the readings, we found that the measurements would jump around, especially for the water level sensor. The code collects ten measurements with gaps of 0.25s and returns each sensor's average values. This function is called in project.py.


##### File: weather station arduino.cpp
The C++ code must be uploaded to the Adafruit HUZZAH ESP8266 WiFi micro-controller breakout using the CP2102 USB-TTL UART Module. It contains the code to read the sensors' data and upload it to the local server. The code can be uploaded using the Arduino app on a Windows PC.
  
##### Files with .png or .jpg
These are just for example purposes, to show what was done in the project. Not necessary to be able to replicate the project but aids it.

----

## Physics-Skills
A Physics course at the University of Edinburgh designed to test an undergraduate's general physics knowledge and predominantly problem-solving skills. Here is the sheet I brought into the exam that entails all of the relevant equations and statements that I have learned throughout my degree.


------

## Modelling-and-Visualisation
A 4th year course taught by Davide Marenduzzo that includes 3 pieces of coursework called checkpoints. Each checkpoint tests your visualisation, optimisation and applied physics skills.

### Checkpoint 1: The Ising model

### Checkpoint 2: Cellular automata - the game of life and the SIRS model

### Checkpoint 3: Partial differential equations -  the Cahn-Hilliard equation and Poisson’s equation


-----

## Research-Methods
A 3rd-year Physics Course. The PDF attached is the literature review, members of the group included Tanja Holc, Sandy Rome, Ben Attwood, Charles Lamb and Hannah Nicholson.

### Comets and Their Connection to the Origin of Life on Earth

#### Abstract
Comets are fascinating astronomical objects, as they provide a deep insight into
the Earth’s history. A well-studied example is 67P/Churyumov-Gerasimenko (67P),
the focus of Rosetta’s soft landing mission in 2014, in which the amino acid glycine
was unambiguously detected for the first time. Rosetta’s findings are presented here
in the broader context of cometary studies and the search for the origin of life on
Earth. Identifying organic compounds and elements essential to life suggests that
comets could have supplied the Earth with various prebiotic chemicals. Moreover,
comets contain water, although studies of hydrogen isotopes showed comets were
not a significant source of the Earth’s oceans, compared to asteroidal planetesimals.
Further research into comets is likely to reveal more about the formation of the
Solar System, with a multitude of spacecraft missions currently being planned to
investigate the beginnings of life on Earth.

------

## TFTs-and-the-Human-Eye
A literature review on how Thin Film transistors (TFTs) can be used to assist the blind or partially blind. There are promising results and only progress can be made since I did the literature review in 2020.

------

## A Ceoliacs Dream the Rise of Gluten-Free Bread
The PDF attached is a report written for a named "Group Project". Our group designed a gluten-free bread by looking for proteins that replicate best, the ones found in gluten. This was a purely theoretical project, as much as we did want to test our recipe in the lab we did not have the time.

Thank you to our supervisor who helped guide us through this project: Jean-Christophe Denis

### Authors: Pablo Sandquist, Hannah Nicholson, Alexa Hladio, Yingxuan Li, Jingyu Song.

#### Abstract:
This report provides evidence to suggest that people with coeliac disease and gluten intolerance are generally dissatisfied with the texture of current gluten free bread alternatives. It proceeds to lay out the groundwork for designing a gluten free flour that resembles the effects of wheat flour on dough and bread rheology by considering the thermodynamics of concentrated polymer doughs. We found that a polymer’s microscopic morphology plays a key role in dough rheology, which can be reduced to the ratio $\sqrt{N\nu / l^3}$ (the key ratio $\kappa$), where N is the number of monomers in a polymer, υ is the monomer volume and 𝑙 is the length of the monomer. The report continues to design a chemical recipe for a gluten free flour resembling strong wheat flour using proteins available in common grains. Finally, the economic, environmental, and nutritional suitability of the flour recipe is examined; with particular emphasis placed on the industrial challenges related to extracting these compounds from grains.



------

# Data Analysis and Machine learning
A University of Edinburgh 5th-year physics computing course aimed at particle physicists. It focuses on fitting and neural networks and machine learning applied to data collected by the LHC.




