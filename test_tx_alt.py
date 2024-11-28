import numpy as np
# from pyhackrftx.libhackrf import *

from pyhackrftx import HackRF
import time

def generate_alternating_tones(freq1, freq2, sample_rate, duration=1.0, switch_interval=0.01):
    """
    Generate a complex baseband signal that alternates between two frequencies.

    :param freq1: Frequency of the first tone in Hz.
    :param freq2: Frequency of the second tone in Hz.
    :param sample_rate: Sampling rate in samples per second.
    :param duration: Total duration of the signal in seconds.
    :param switch_interval: Interval to switch frequencies in seconds.
    :return: NumPy array of complex64 samples.
    """
    total_samples = int(duration * sample_rate)
    switch_samples = int(switch_interval * sample_rate)
    num_switches = int(duration / switch_interval)
    
    # Time vector for one switch interval
    t_switch = np.arange(switch_samples) / sample_rate

    # Precompute tone segments
    tone1 = np.exp(2j * np.pi * freq1 * t_switch).astype(np.complex64)
    tone2 = np.exp(2j * np.pi * freq2 * t_switch).astype(np.complex64)

    # Initialize signal array
    signal = np.empty(total_samples, dtype=np.complex64)

    # Fill the signal array by repeating tone segments
    for i in range(num_switches):
        start_idx = i * switch_samples
        end_idx = start_idx + switch_samples
        if end_idx > total_samples:
            end_idx = total_samples
        if i % 2 == 0:
            signal[start_idx:end_idx] = tone1[:end_idx - start_idx]
        else:
            signal[start_idx:end_idx] = tone2[:end_idx - start_idx]

    # Handle any remaining samples
    remaining_samples = total_samples - num_switches * switch_samples
    if remaining_samples > 0:
        if num_switches % 2 == 0:
            signal[-remaining_samples:] = tone1[:remaining_samples]
        else:
            signal[-remaining_samples:] = tone2[:remaining_samples]

    return signal





# Define the frequencies and parameters
freq1 = 1e6    # Frequency offset +1 MHz
freq2 = -1e6   # Frequency offset -1 MHz
center_freq = 3.425e9  # Center frequency 2.4 GHz
sample_rate = 5e6   # 10 MS/s
duration = 1.0       # 1 second
switch_interval = 0.01  # Switch every 10 ms

# Generate the 1-second alternating tones waveform
samples = generate_alternating_tones(freq1, freq2, sample_rate, duration, switch_interval)

# Use the HackRF to transmit the signal
try:
    with HackRF() as hackrf:
        # Set parameters
        hackrf.center_freq = center_freq
        hackrf.sample_rate = sample_rate
        hackrf.txvga_gain = 46  # Adjust as needed

        # Start transmitting
        print("Starting TX")
        hackrf.start_tx(samples, repeat=True)  # Repeat the 1-second waveform

        # Transmit for 30 seconds
        time.sleep(30)

        # Stop transmitting
        hackrf.stop_tx()
        print("Stopping TX")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the device is closed properly
    if 'hackrf' in locals() and hackrf.device_opened:
        hackrf.stop_tx()
        hackrf.close()