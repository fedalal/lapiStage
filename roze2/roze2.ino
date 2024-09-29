#include "TroykaProximity.h"
#include <Adafruit_NeoPixel.h>
TroykaProximity sensor;

#define PIN        7 // On Trinket or Gemma, suggest changing this to 1
#define NUMPIXELS 105 // Popular NeoPixel ring size
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 20 // Time (in milliseconds) to pause between pixels
int STEP = -5;
int LIGHT = 255;

void setup() {
  sensor.begin();
  Serial.begin(115200);

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear(); // Set all pixel colors to 'off'

  for(int i=0; i<= NUMPIXELS ; i++) { // For each pixel...
    pixels.setPixelColor(i, pixels.Color(0, 255, 0));
  }
  pixels.show();   // Send the updated pixel colors to the hardware.
      
  delay(5000);
  for(int i=0; i<= NUMPIXELS ; i++) { // For each pixel...
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
  }
  
  pixels.show();   // Send the updated pixel colors to the hardware.
      
  delay(1000);
  
}

void loop() {
    int range = sensor.readRange();
  if (range == 255) {
    Serial.println("Out of range");
  }
  else {
    Serial.println(range);
    if(range<100 && range >50)
  {

for(int i=0; i<= NUMPIXELS ; i++) { // For each pixel...
    pixels.setPixelColor(i, pixels.Color(0, 255, 0));
  }
  pixels.show();   // Send the updated pixel colors to the hardware.
      
  delay(500);
  for(int i=0; i<= NUMPIXELS ; i++) { // For each pixel...
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
  }
  
     delay(8000);
    while (true)
    {
      LIGHT = LIGHT + STEP;
      Serial.println(LIGHT);
      if (LIGHT < 10 || LIGHT > 250)
      {
        STEP = STEP * -1;
      }
      for(int i=0; i< NUMPIXELS ; i++) { // For each pixel...
        pixels.setPixelColor(i, pixels.Color(LIGHT, 0, 0));
        
      }

      pixels.show();   // Send the updated pixel colors to the hardware.
      delay(DELAYVAL);

    }
  }

  
  }

  
  
  delay(200);
}
