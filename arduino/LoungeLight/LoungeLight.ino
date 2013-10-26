#include "SPI.h"
#include "Adafruit_WS2801.h"

/*****************************************************************************
Example sketch for driving Adafruit WS2801 pixels!


  Designed specifically to work with the Adafruit RGB Pixels!
  12mm Bullet shape ----> https://www.adafruit.com/products/322
  12mm Flat shape   ----> https://www.adafruit.com/products/738
  36mm Square shape ----> https://www.adafruit.com/products/683

  These pixels use SPI to transmit the color data, and have built in
  high speed PWM drivers for 24 bit color per pixel
  2 pins are required to interface

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution

*****************************************************************************/

// Choose which 2 pins you will use for output.
// Can be any valid output pins.
// The colors of the wires may be totally different so
// BE SURE TO CHECK YOUR PIXELS TO SEE WHICH WIRES TO USE!
int dataPin  = 2;    // Yellow wire on Adafruit Pixels
int clockPin = 3;    // Green wire on Adafruit Pixels

// Don't forget to connect the ground wire to Arduino ground,
// and the +5V wire to a +5V supply

// Set the first variable to the NUMBER of pixels. 25 = 25 pixels in a row
Adafruit_WS2801 strip = Adafruit_WS2801(396);

// Optional: leave off pin numbers to use hardware SPI
// (pinout is then specific to each board and can't be changed)
//Adafruit_WS2801 strip = Adafruit_WS2801(25);

// For 36mm LED pixels: these pixels internally represent color in a
// different format.  Either of the above constructors can accept an
// optional extra parameter: WS2801_RGB is 'conventional' RGB order
// WS2801_GRB is the GRB order required by the 36mm pixels.  Other
// than this parameter, your code does not need to do anything different;
// the library will handle the format change.  Examples:
//Adafruit_WS2801 strip = Adafruit_WS2801(25, dataPin, clockPin, WS2801_GRB);
//Adafruit_WS2801 strip = Adafruit_WS2801(25, WS2801_GRB);

void setup() {
    
  strip.begin();

  // Update LED contents, to start they are all 'off'
  strip.show();
  
  Serial.begin(9600);
}

void loop() {
  // Some example procedures showing how to display to the pixels
  
  //rgb_explode(10);
  //betterStripes(Color(50,200,0),Color(0,50,200),Color(200,0,50),05,5,1000);
  
  int stdel = 05; 
  
  rainbowStripes(stdel/5,5,1000);
   
  wipe();
   
  int i;
  for (i=0;i<5;i++) {
    disperse(stdel/5, strip.numPixels() / 2);
  }
  
  //pulseBounce(05);
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

/*

void asplode(uint8_t wait) {
  int i, k;
  float cscale;
  // scale factor (so pixels always go blue -> red)
  cscale = 85 / (2*strip.numPixels());
  
  for (i=0; i < strip.numPixels() / 2; i++) {
    for (k=0; k < 5; k++) {
      strip.setPixelColor(i+k, Wheel(i*cscale + 170));
      strip.setPixelColor(strip.numPixels()-i-k-1, Wheel(i*cscale + 170));
      strip.setPixelColor(i+k-5, Color(0,0,0));
      strip.setPixelColor(strip.numPixels()-i-k+4, Color(0,0,0));
    }
    strip.show();
    delay(wait/(1 + i/20));
  }
}  

*/

void wipe() {
  int i;
  for (i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i,Color(0,0,0));
  }
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

/* fireworks needs more work / is mostly replaced by disperse

void fireworks(uint8_t wait, int s) {
  int center;

  for (center=s; center < strip.numPixels() - s + 1; center = center + s) {
    stretch(wait, center, s);
    shrink(wait, center, s);
  }
  s = s / 2;
  if (s > 2) {
    fireworks(wait, s);
  }
}

void stretch(uint8_t wait, int center, int dist) {
  // light "stretches" dist pixels in both directions
  int i;
  
  for (i=0; i<dist; i++) {
    strip.setPixelColor(center+i, Wheel(center % 255));
    strip.setPixelColor(center-i, Wheel(center % 255));
    strip.show();
    delay(wait);
  }
}

void shrink(uint8_t wait, int center, int dist) {
  int i;
  
  for (i=dist-1; i>=0; i--) {
    strip.setPixelColor(center+i, Color(0,0,0));
    strip.setPixelColor(center-i, Color(0,0,0));
    strip.show();
    delay(wait);
  }
}

*/

void pulse(uint8_t wait, int n) {
  // sends a pulse of width n forwards
  int i, j, k;
  
  for (i=0; i<strip.numPixels() - n; i++) {
    for (j=0; j < n + 1; j++) {
      if (i+j < strip.numPixels()) {
        strip.setPixelColor(i+j, Wheel((i + j) % 255));
      }
      strip.setPixelColor(i+j-n, Color(0,0,0));
    }
    strip.show();
    delay(wait);
  }
}

void eslup(uint8_t wait, int n) {
  // sends a pulse of width n backwards
  int i, j, k;
  
  for (i=strip.numPixels(); i>n; i-=1) {
    for (j=0; j < n + 1; j++) {
      if (i-j > 0) {
        strip.setPixelColor(i-j, Wheel((i + j) % 255));
      }
      strip.setPixelColor(i-j+n, Color(0,0,0));
    }
    strip.show();
    delay(wait);
  }
}

void pulseLoop(uint8_t wait) {
  int n;
  
  for (n=5; n < strip.numPixels() / 4; n+=5) {
    pulse(wait, n);
  }
}

void pulseBounce(uint8_t wait) {
  int n;
  
  for (n=5; n < strip.numPixels() / 4; n+=10) {
    pulse(wait, n);
    eslup(wait, n+5);
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

void rgb_explode(uint8_t wait) {
  struct bomb {
    uint16_t center;
    uint16_t age;
    uint32_t color;
    
    struct bomb *next;
    struct bomb *prev;
  };
  
  struct bomb *bomb_head = 0;
  struct bomb *bomb_tail = 0;
 
  for (int f = 0; f < 256; f++) {
    
    if (random(0, 256) > 192 || bomb_head == 0) {
      struct bomb *b = (struct bomb *)malloc(sizeof(struct bomb));
      b->center = random(10, strip.numPixels()-10);
      b->age = 0;
      
      int color = random(0, 3);
      if (color == 0) {
        b->color = Color(128, 0, 0);
      } else if (color == 1) {
        b->color = Color(0, 128, 0);
      } else {
        b->color = Color(0, 0, 128);
      }
      
      b->next = 0;
      b->prev = bomb_tail;
      
      if (!bomb_head) bomb_head = b;
      if (bomb_tail) bomb_tail->next = b;
      bomb_tail = b;
    }
    
    for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, 0);
    }
    
    struct bomb *b = bomb_head;
    while (b) {
      int radius;
      if (b->age++ < 10) {
        radius = b->age;
      } else {
        radius = 20 - b->age;  
      }
      
      if (b->age > 20) {
        struct bomb *dead = b;
        if (dead->prev) dead->prev->next = dead->next;
        if (dead->next) dead->next->prev = dead->prev;
        
        if (dead == bomb_head) bomb_head = dead->next;
        if (dead == bomb_tail) bomb_tail = dead->prev;
        
        b = dead->next;
        free(dead);
        continue;
      }
            
      for (int i = -radius; i < radius; i++) {
        int j = b->center+i;
        if (j < 0 || j >= strip.numPixels()) continue;
        
        //float scale = b->age / 40.0;
        strip.setPixelColor(j, b->color + strip.getPixelColor(j));
      }
            
      b = b->next;
    }
        
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
