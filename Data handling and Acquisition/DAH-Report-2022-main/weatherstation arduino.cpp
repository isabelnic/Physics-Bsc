/* DHTServer - ESP8266 Webserver with a DHT sensor and water level sensor as an input

   Based on ESP8266Webserver, DHTexample, and BlinkWithoutDelay (thank you)

   Version 1.0  5/3/2014  Version 1.0   Mike Barela for Adafruit Industries

   Supplemented with code by Elian Ruijter and Hannah Nicholson
*/
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DHT.h>
#define DHTTYPE DHT22
#define DHTPIN  2

// Input for the water level sensor
// The power pin is the input power (chosen for digital input) rather 
// than continuous 3.3V.
// The signal pin is the analog pin, as the water level sensor has an analog output.
// Sensor min and max is found through calibration process to convert the 
// output to millimeter.
#define POWER_PIN  12
#define SIGNAL_PIN A0
#define SENSOR_MIN 0
#define SENSOR_MAX 550

int water_value = 0; // variable to store the sensor value
int water_level = 0; // variable to store the water level

// Set wifi ssid and password
const char* ssid     = "DAH-local-wifi";
const char* password = "AbbeyRoadAlbum";

ESP8266WebServer server(80);
 
// Initialize DHT sensor 
// NOTE: For working with a faster than ATmega328p 16 MHz Arduino chip, like an ESP8266,
// you need to increase the threshold for cycle counts considered a 1 or 0.
// You can do this by passing a 3rd parameter for this threshold.  It's a bit
// of fiddling to find the right value, but in general the faster the CPU the
// higher the value.  The default for a 16mhz AVR is a value of 6.  For an
// Arduino Due that runs at 84mhz a value of 30 works.
// This is for the ESP8266 processor on ESP-01 
DHT dht(DHTPIN, DHTTYPE, 11); // 11 works fine for ESP8266
 
float humidity, temp_f;  // Values read from sensor
String webString="";     // String to display
// Generally, you should use "unsigned long" for variables that hold time
unsigned long previousMillis = 0;        // will store last temp was read
const long interval = 2000;              // interval at which to read sensor
 
void handle_root() {
  server.send(200, "text/plain", "Hello from the weather esp8266, read from /water_level /temp or /humidity");
  delay(100);
}
 
void setup(void)
{
  // You can open the Arduino IDE Serial Monitor window to see what the code is doing
  Serial.begin(115200);  // Serial connection from ESP-01 via 3.3v console cable
  dht.begin();           // initialize temperature sensor

  Serial.begin(9600);
  pinMode(POWER_PIN, OUTPUT);   // configure D12 pin as an OUTPUT
  digitalWrite(POWER_PIN, LOW); // turn the sensor OFF

  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("DHT Weather Reading Server");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
   
  server.on("/", handle_root);
  
  server.on("/temp", [](){  // if you add this subdirectory to your webserver call, you get text below :)
    gettemperature();       // read sensors
    webString="Temperature: "+String((int)temp_f)+" F";   // Arduino has a hard time with float to string, read in Fahrenheit
    server.send(200, "text/plain", webString);            // send to someones browser when asked
  });

  server.on("/humidity", [](){  // if you add this subdirectory to your webserver call, you get text below :)
    gettemperature();           // read sensors
    webString="Humidity: "+String((int)humidity)+"%";	     // humidity is returned as relative humidity in %
    server.send(200, "text/plain", webString);               // send to someones browser when asked
  });

  server.on("/water_level", [](){
    gettemperature();		// read sensors
    webString="Water level: "+String((int)water_level) +" mm"; // Get the water level (converted to millimeter)
    server.send(200, "text/plain", webString);
  });
  
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void)
{
  server.handleClient();
} 

// Function to read the water level sensor, the power pin is only turned on 
// when the sensor is read.
int readwater_level() {
  digitalWrite(POWER_PIN, HIGH);  // turn the sensor ON
  delay(10);                      // wait 10 milliseconds
  water_value = analogRead(SIGNAL_PIN); // read the analog value from sensor
  digitalWrite(POWER_PIN, LOW);   // turn the sensor OFF
  
  // Convert the analog value to millimeter, the sensor is 4 cm long
  water_level = map(water_value, SENSOR_MIN, SENSOR_MAX, 0, 4); // 4 levels
  Serial.print("Water level: ");
  Serial.println(water_level);

  delay(1000);
  return water_level * 10;
}

void gettemperature() {
  // Wait at least 2 seconds seconds between measurements.
  // if the difference between the current time and last time you read
  // the sensor is bigger than the interval you set, read the sensor
  // Works better than delay for things happening elsewhere also
  unsigned long currentMillis = millis();
 
  if(currentMillis - previousMillis >= interval) {
    // save the last time you read the sensor 
    previousMillis = currentMillis;   

    // Reading temperature for humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
    humidity = dht.readHumidity();          // Read humidity (percent)
    temp_f = dht.readTemperature(true);     // Read temperature as Fahrenheit
    water_level = readwater_level();	    // Get water level in mm from the equation above

    // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temp_f)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
  }
}















