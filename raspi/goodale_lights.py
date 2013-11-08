import RPi.GPIO as GPIO
import time

red = [255, 0, 0]
blue = [0, 0, 255] 

# Boilerplate junk
dev = "/dev/spidev0.0"
spidev = file(dev, "wb")

# These might be changed if we expand
num_leds = 396
pixel_size = 3

# For WS2801
gamma = bytearray(256)
for i in range(256):
    gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)

output = bytearray(num_leds * pixel_size + 3)

def filter_pixel(input_pixel, brightness):
    input_pixel[0] = brightness * input_pixel[0]
    input_pixel[1] = brightness * input_pixel[1]
    input_pixel[2] = brightness * input_pixel[2]

    output_pixel = bytearray(pixel_size)
    output_pixel[0] = gamma[input_pixel[0]]
    output_pixel[1] = gamma[input_pixel[1]]
    output_pixel[2] = gamma[input_pixel[2]]
    return output_pixel

color = red
while True:
    for led in range(num_leds):
        output[led * pixel_size:] = filter_pixel(color, 1)
    if color == red:
        color = blue
    else:
        color = red
    spidev.write(output)
    spidev.flush()
    #time.sleep(0.1)

