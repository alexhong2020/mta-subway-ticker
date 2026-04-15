import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Import subway functions
try:
    from mta import get_arrivals_for_display
except ImportError:
    print("Error: mta.py not found. Ensure it is in the same folder.")
    sys.exit(1)

def main():
    # --- 1. CONFIGURATION (Tuned for Pi 3 Stability) ---
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat' 
    
    options.disable_hardware_pulsing = True 
    options.gpio_slowdown = 4      
    options.pwm_bits = 2           # Essential to stop "seismic" noise & white gradients
    options.brightness = 95        
    options.limit_refresh_rate_hz = 60 
    options.drop_privileges = False 

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    # --- 2. FONT LOADING ---
    font_6x10 = graphics.Font()
    font_6x10.LoadFont("6x10.bdf") 

    font_4x6 = graphics.Font()
    font_4x6.LoadFont("4x6.bdf")

    # --- 3. COLORS ---
    white = graphics.Color(255, 255, 255)
    # f_orange = graphics.Color(255, 99, 25)
    f_orange = graphics.Color(255, 128, 0)
    black = graphics.Color(0, 0, 0)

    # --- 4. STATE VARIABLES ---
    pos = 64           # Position for train times
    header_pos = 64    # Position for Roosevelt Island text
    last_update = 0
    arrivals_q, arrivals_m = [], []

    # clipping/gap configuration
    clearance_zone = 16 # Text vanishes 4 pixels before hitting the F box

    try:
        while True:
            # Update data every 30 seconds (~3 full header scrolls)
            if time.time() - last_update > 30:
                arrivals_q, arrivals_m = get_arrivals_for_display()
                last_update = time.time()

            canvas.Clear()

            # --- 1. DRAW SCROLLING HEADER (With Clipping Math) ---
            visible_text = "ROOSEVELT ISLAND"
            char_width = 4 

            if header_pos > clearance_zone:
                graphics.DrawText(canvas, font_4x6, header_pos, 7, f_orange, visible_text)
            else:
                # Calculate how many chars to hide as it passes the 'edge'
                chars_to_skip = (clearance_zone - header_pos) // char_width
                if chars_to_skip < len(visible_text):
                    graphics.DrawText(canvas, font_4x6, clearance_zone, 7, f_orange, visible_text[chars_to_skip:])

            # --- 2. DRAW CIRCULAR F LOGO (Drawn over text) ---
            center_x, center_y = 6, 6
            radius_sq = 5.5**2
            for x in range(0, 13):
                for y in range(0, 13):
                    if (x - center_x)**2 + (y - center_y)**2 <= radius_sq:
                        canvas.SetPixel(x, y, 255, 99, 25)
            
            # Small F (4x6) centered in the 12x12 circle
            # x=5, y=9 is usually the "sweet spot" for centering a 4-wide char in a 12-wide box
            # graphics.DrawText(canvas, font_4x6, 5, 9, black, "F")
            
            # Big F centered in circle
            graphics.DrawText(canvas, font_6x10, 4, 10, black, "F")

            # --- 3. DRAW SCROLLING TIMES ---
            q_str = "QUEENS: " + " • ".join([f"{m}m" for m in arrivals_q])
            m_str = "MANHATTAN: " + " • ".join([f"{m}m" for m in arrivals_m])
            
            graphics.DrawText(canvas, font_4x6, pos, 20, white, q_str)
            graphics.DrawText(canvas, font_4x6, pos, 31, white, m_str)

            # --- 4. MOTION LOGIC ---
            pos -= 1
            header_pos -= 1

            # Resets
            if pos < -600: # Longer limit for more train times
                pos = 64
            if header_pos < -150:
                header_pos = 64

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.08) 

    except KeyboardInterrupt:
        canvas.Clear()
        print("\nStopping subway tracker...")

if __name__ == "__main__":
    main()