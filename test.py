import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def run_test():
    # 1. Hardware Configuration
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat' 

    # 2. Pi 3 Stability & Ratio Fixes
    # disable_hardware_pulsing allows the matrix to run without disabling audio in /boot/config.txt
    options.disable_hardware_pulsing = True 
    options.gpio_slowdown = 2     
    options.multiplexing = 0      
    options.row_address_type = 0  
    options.drop_privileges = False

    # 3. Initialize Matrix
    try:
        matrix = RGBMatrix(options=options)
    except Exception as e:
        print(f"Error: {e}")
        return

    canvas = matrix.CreateFrameCanvas()

    # --- PHASE 1: FULL GREEN ---
    print("Step 1: Filling screen with Green...")
    canvas.Fill(0, 255, 0)
    canvas = matrix.SwapOnVSync(canvas)
    time.sleep(3)

    # --- PHASE 2: WHITE BORDER ---
    print("Step 2: Drawing White Perimeter...")
    canvas.Clear()
    
    # Draw Top and Bottom lines
    for x in range(64):
        canvas.SetPixel(x, 0, 255, 255, 255)    # Top edge
        canvas.SetPixel(x, 31, 255, 255, 255)   # Bottom edge
        
    # Draw Left and Right lines
    for y in range(32):
        canvas.SetPixel(0, y, 255, 255, 255)    # Left edge
        canvas.SetPixel(63, y, 255, 255, 255)   # Right edge

    matrix.SwapOnVSync(canvas)
    
    print("\n--- TEST COMPLETE ---")
    print("1. If you don't see all 4 white edges, change 'row_address_type' to 2.")
    print("2. If the lines are flickering badly, increase 'gpio_slowdown' to 3.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    run_test()