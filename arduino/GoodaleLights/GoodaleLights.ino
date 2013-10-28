#include "Arduino.h"
#include "Adafruit_WS2801.h"
#include <Ethernet.h>
#include <SPI.h>

int dataPin  = 2;    // Yellow wire on Adafruit Pixels
int clockPin = 3;    // Green wire on Adafruit Pixels

// Set the first variable to the NUMBER of pixels
Adafruit_WS2801 strip = Adafruit_WS2801(396, dataPin, clockPin);

// Pattern state
String state = "off";

// Mac address of the Arduino board
byte mac[] = {0x90, 0xA2, 0xDA, 0x00, 0x74, 0x34};

// IP address of the disco server
IPAddress server(18, 189, 16, 206); 

EthernetClient client;

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac);

  // give the Ethernet shield a second to initialize:
  delay(3000);

  // if you get a connection, report back via serial:
  if (client.connect(server, 8123)) {
    Serial.println("connected");
  } 
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
  
  // Begin the light strips
  strip.begin();
  strip.show();
}

void loop() {
  if (client.available()) {
    state = readMessage();
    state.trim();
    Serial.println(state);
  }
  
  // Display pattern based on set state
  int stdel = 5; 
  if (state.equals("cycle")) {
    runPatternCycle();
  } else if (state.equals("rainbowStripes")) {
    rainbowStripes(stdel/5, 5, 1000);
  } else if (state.equals("interpolateMatrix")) {
    interpolate_matrix(255, 0, 0, 0, 255, 0, 192, 50);
    interpolate_matrix(0, 255, 0, 0, 0, 255, 192, 50);
    interpolate_matrix(0, 0, 255, 255, 0, 0, 192, 50);
  } else if (state.equals("rainbow")) {
    rainbow(stdel/2);
  } else if (state.equals("matrix")) {
    matrix(Color(0, 255, 0), 128, 50);
  } else if (state.equals("rainbowCycle")) {
    rainbowCycle(stdel/2);
  } else {
    wipe();
  }

  if (!client.connected()) {
    client.stop();
    state = "cycle";
  }
}

String readMessage() {
  String inMessage = "";
  while (client.available()) {
    char c = client.read();
    inMessage += c;
  }
  return inMessage;
}

void runPatternCycle() {
  int stdel = 5; 
  rainbowStripes(stdel/5,5,1000);
  wipe();
   
  int i;
  for (i=0;i<5;i++) {
    disperse(stdel/5, strip.numPixels() / 2);
  }

  rainbow(stdel/2);
  interpolate_matrix(255, 0, 0, 0, 255, 0, 192, 50);
  interpolate_matrix(0, 255, 0, 0, 0, 255, 192, 50);
  interpolate_matrix(0, 0, 255, 255, 0, 0, 192, 50);
  
  matrix(Color(0, 255, 0), 128, 50);
  matrix(Color(255, 0, 0), 192, 50);
  colorWipe(Color(255, 0, 0), 10);
  colorWipe(Color(0, 255, 0), 10);
  colorWipe(Color(0, 0, 255), 10);
  rainbowCycle(stdel/2);
}

void wipe() {
  int i;
  for (i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i,Color(0,0,0));
  }
  strip.show();
}

void rainbowStripes(uint8_t wait, int width, int duration) {
  int i;
  for (i=0; i<duration; i++) {
    makeStripes(i,width, Wheel(i % 255), Wheel((i+85) % 255), Wheel((i+170) % 255));
    delay(wait);
  }
}

void betterStripes(uint32_t color1, uint32_t color2, uint32_t color3, uint8_t wait, int width, int duration) {
  int i;
  for (i=0; i<duration; i++) {
    makeStripes(i,width, color1, color2, color3);
    delay(wait);
  }
}

void makeStripes(int start, int width, uint32_t color1, uint32_t color2, uint32_t color3) {
  int i,j,pixloc;
  for (i=0; i<strip.numPixels(); i+=3*width) {
    for (j=0; j<width; j++) {
      pixloc = (start + i + j) % strip.numPixels();
      strip.setPixelColor(pixloc,color1);
    }
    for (j=width; j<2*width; j++) {
      pixloc = (start + i + j) % strip.numPixels();
      strip.setPixelColor(pixloc,color2);
    }
    for (j=2*width; j<3*width; j++) {
      pixloc = (start + i + j) % strip.numPixels();
      strip.setPixelColor(pixloc,color3);
    }      
  }
  strip.show();
}

void stripes(uint8_t wait, int n) {
  //initial setup
  int i,j;
  for (i=0; i<strip.numPixels(); i++) {
    if (i % (3*n) < n) {
     strip.setPixelColor(i,Color(255,0,0));
    }
    else if (i % (3*n) < (2*n)) {
     strip.setPixelColor(i,Color(0,255,0));
    }
    else {
     strip.setPixelColor(i,Color(0,0,255));
    }
  }
  strip.show();
  delay(wait);
  
  // move
  for (i=0; i<strip.numPixels(); i++) {
    for (j=n; j<strip.numPixels(); j+=3*n) {
      strip.setPixelColor(i-j,Color(0,0,255));
      strip.setPixelColor(i-2*j,Color(0,255,0));
      strip.setPixelColor(i-3*j,Color(255,0,0));
      strip.setPixelColor(i+j,Color(255,0,0));
      strip.setPixelColor(i+2*j,Color(0,255,0));
      strip.setPixelColor(i+3*j,Color(0,0,255));
    }
    strip.show();
    delay(wait);
  }
  
  // clean up
  for (i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i,Color(0,0,0));
    strip.show();
    delay(wait);
  }
}


void disperse(uint8_t wait, int s) {
  int center, i;

  for (i=0; i<s/2; i++) {
    for (center=s-1; center < strip.numPixels(); center = center + s) {
      strip.setPixelColor(center+i, Wheel(center % 255));
      strip.setPixelColor(center-i, Wheel(center % 255));
    }
    
    // take care of boundary condition at beginning of strip
    strip.setPixelColor(i, Wheel(0));
    
    strip.show();
    delay(wait);
  }
  
  for (i=s/2-1; i>=0; i--) {
    for (center=s-1; center < strip.numPixels(); center = center + s) {
      strip.setPixelColor(center+i, Color(0,0,0));
      strip.setPixelColor(center-i, Color(0,0,0));
    }
    
    // take care of boundary condition at beginning of strip
    strip.setPixelColor(i, Color(0,0,0));
    
    strip.show();
    delay(wait);
  }
  
  s = s/2;
  wait = wait*2;
  if (s > 4) {
    disperse(wait, s);
  }
}

void rainbow(uint8_t wait) {
  int i, j;
   
  for (j=0; j < 256; j++) {     // 3 cycles of all 256 colors in the wheel
    for (i=0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel( (i + j) % 255));
    }  
    strip.show();   // write all the pixels out
    delay(wait);  
  }
}

// Slightly different, this one makes the rainbow wheel equally distributed 
// along the chain
void rainbowCycle(uint8_t wait) {
  int i, j;
  int corr = floor(255/strip.numPixels());
  
  for (j=0; j < 256 * 5; j++) {     // 5 cycles of all 25 colors in the wheel
    for (i=0; i < strip.numPixels(); i++) {
      // tricky math! we use each pixel as a fraction of the full 96-color wheel
      // (thats the i / strip.numPixels() part)
      // Then add in j which makes the colors go around per pixel
      // the % 96 is to make the wheel cycle around
      strip.setPixelColor(i, Wheel( ((i * 256 * corr / strip.numPixels()) + j) % 256) );
    }  
    strip.show();   // write all the pixels out
    delay(wait);
  }
}

// fill the dots one after the other with said color
// good for testing purposes
void colorWipe(uint32_t c, uint8_t wait) {
  int i;
  
  for (i=0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
  }
}

void interpolate(uint8_t r1, uint8_t g1, uint8_t b1, uint8_t r2, uint8_t g2, uint8_t b2, uint8_t wait) {
  for (int i = 0; i < 256; i++) {
     float x = (i / 255.0);
     float y = 1.0 - x;
     
     uint8_t r = x * r2 + y * r1;
     uint8_t g = x * g2 + y * g1;
     uint8_t b = x * b2 + y * b1;
     
     for (int j = 0; j < strip.numPixels(); j++) {
       strip.setPixelColor(j, r, g, b);
     }
     strip.show();
     delay(wait);
  }
}

void matrix(uint32_t color, uint8_t sparsity, uint8_t wait) {
  for (int f = 0; f < 256; f++) {
    for (int i = 0; i < strip.numPixels(); i++) {
      if (random(0, 256) > sparsity) {
        strip.setPixelColor(i, color);
      } else {
        strip.setPixelColor(i, 0, 0, 0);
      }
    }
    strip.show();
    delay(wait);
  }
}

void interpolate_matrix(uint8_t r1, uint8_t g1, uint8_t b1, uint8_t r2, uint8_t g2, uint8_t b2, uint8_t sparsity, uint8_t wait) {
  for (int i = 0; i < 256; i++) {
     float x = (i / 255.0);
     float y = 1.0 - x;
     
     uint8_t r = x * r2 + y * r1;
     uint8_t g = x * g2 + y * g1;
     uint8_t b = x * b2 + y * b1;
     
     for (int j = 0; j < strip.numPixels(); j++) {
       if (random(0, 256) > sparsity) {
         strip.setPixelColor(j, r, g, b);
       } else {
         strip.setPixelColor(j, 0, 0, 0);
       }
     }
     strip.show();
     delay(wait);
  }
}

/* Helper functions */

// Create a 24 bit color value from R,G,B
uint32_t Color(byte r, byte g, byte b)
{
  uint32_t c;
  c = r;
  c <<= 8;
  c |= g;
  c <<= 8;
  c |= b;
  return c;
}

//Input a value 0 to 255 to get a color value.
//The colours are a transition r - g -b - back to r
uint32_t Wheel(byte WheelPos)
{
  if (WheelPos < 85) {
   return Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if (WheelPos < 170) {
   WheelPos -= 85;
   return Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170; 
   return Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

uint32_t randColor() {
  int r,g,b;
  r = random(0,255);
  g = random(0,255);
  b = random(0,255);
  return Color(r,g,b);
}
