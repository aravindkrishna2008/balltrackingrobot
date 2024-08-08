import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


class LEDMatrix():
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=4, block_orientation=-90,
                     rotate=0, blocks_arranged_in_reverse_order=False, intensity=3)
    
    def show_verticle_message(self, msg):
        words = msg.split()
        virtual = viewport(self.device, width=self.device.width, height=len(words) * 8)
        with canvas(virtual) as draw:
            for i, word in enumerate(words):
                text(draw, (0, i * 8), word, fill="white", font=proportional(SINCLAIR_FONT))
        for i in range(virtual.height - self.device.height):
            virtual.set_position((0, i))
            time.sleep(0.20)
    
    def show_welcome(self, msg):
        show_message(self.device, msg, fill="white", font=proportional(CP437_FONT))
        time.sleep(1)
        

if __name__ == '__main__':
    matrix = LEDMatrix()
    matrix.show_welcome("Hello World! Ball Tracking Robot")
    while True:
        matrix.show_verticle_message("U1 5cm U2 5cm")