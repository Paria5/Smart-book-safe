#include <DHT11.h>
#include "LedControl.h"
#define RelayPin  7  // Connect to IN1 on L9110
#define Buzzer_pin 3

LedControl lc=LedControl(10,8,9,1);

DHT11 dht11(2);
int result = 0;


void setup() {
  lc.shutdown(0, false); // Wake up the display
  lc.setIntensity(0, 8); // Set brightness level
  lc.clearDisplay(0); // Clear the display
    Serial.begin(9600);
    pinMode(RelayPin, OUTPUT);
    Serial1.begin(9600);

}

void loop() {
    int temperature = 0;
    int humidity = 0;
    int sensorValue=analogRead(A0);
    int LDR=analogRead(A1);
    result=dht11.readTemperatureHumidity(temperature, humidity);

    if (result == 0) {
        //Serial.print("Temperature: ");
        //Serial.print(temperature);
        //Serial.print(" °C\tHumidity: ");
        //Serial.print(humidity);
        //Serial.println(" %");

        if (temperature > 20) {
            digitalWrite(RelayPin, LOW);
            //Serial.println("Turning fan on");
            
        } else {
            digitalWrite(RelayPin, HIGH);
            //Serial.println("Turning fan off");

        }
    } else {
        Serial.println(DHT11::getErrorString(result));
    }
        if (Serial1.available()) {
        
        char command = Serial1.read();
        Serial.print(command);
        if (command == '1')
        {
            // Send sensor data to the server
            Serial1.print("Temperature: ");
            Serial1.print(temperature);
            Serial1.print(" °C, Humidity: ");
            Serial1.print(humidity);
            Serial1.print(" %,Gas intensity: ");
            Serial1.print(sensorValue);
            Serial1.print(" , Light internsity: ");
            Serial1.print(LDR);
        }
    }
    if (sensorValue>500){
      analogWrite(Buzzer_pin,50);
    }
    else{
      analogWrite(Buzzer_pin,0);
    }
    if (LDR < 5) {
    // Turn on all LEDs
    for (int row = 0; row < 8; row++) {
      lc.setRow(0, row, B11111111); // Turn on all LEDs in the row
    }
  } else {
    // Turn off all LEDs
    for (int row = 0; row < 8; row++) {
      lc.setRow(0, row, B00000000); // Turn off all LEDs in the row
    }
  }
 

}
