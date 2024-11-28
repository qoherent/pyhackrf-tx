import numpy as np
# from pyhackrftx.libhackrf import *

from pyhackrftx import HackRF
import time

# Generate a test signal (e.g., a sine wave)
def generate_tone(freq, sample_rate, duration):
    t = np.arange(0, duration, 1 / sample_rate)
    tone = np.exp(2j * np.pi * freq * t)
    return tone.astype(np.complex64)
# Create an instance of the HackRF class

with HackRF() as hackrf:
    # Set parameters
    hackrf.center_freq = 2.4e9  # 2.4 GHz
    hackrf.sample_rate = 10e6   # 10 MS/s
    hackrf.txvga_gain = 30      # 30 dB gain

    # Generate a 1 MHz tone
    samples = generate_tone(1e6, hackrf.sample_rate, duration=1)

    # Start transmitting
    print("Starting TX")
    hackrf.start_tx(samples, repeat=True)

    # Transmit for 5 seconds
    time.sleep(5)

    # Stop transmitting
    hackrf.stop_tx()
    print("TX complete")

