import requests
import os
import numpy as np
import logging

# This function is entirely courtesy of our ChatGPT overlords
# (it can probably be done more efficient, but it works)
def encode_bit_array(bits):
    # Define the mapping from 4-bit strings to characters
    char_map = {
        '0000': 'a',
        '0001': 'b',
        '0010': 'c',
        '0011': 'd',
        '0100': 'e',
        '0101': 'f',
        '0110': 'g',
        '0111': 'h',
        '1000': 'i',
        '1001': 'j',
        '1010': 'k',
        '1011': 'l',
        '1100': 'm',
        '1101': 'n',
        '1110': 'o',
        '1111': 'p'
    }

    # Convert the numpy array of bits to a binary string
    bin_str = ''.join(['1' if bit else '0' for bit in bits])

    # Break the binary string into groups of four characters each
    groups = [bin_str[i:i+4] for i in range(0, len(bin_str), 4)]

    # Map each group of four characters to the corresponding character
    result = ''.join([char_map[group] for group in groups])

    # Swap the position of every two characters
    result = ''.join([result[i:i+2][::-1] for i in range(0, len(result), 2)])

    return result

def make_request(path):
    # The "server" running on the ESP32 will not respond with a proper status code,
    # but will terminate the connection on every call, even when the command is
    # successful. We do want to impose and catch a timeout however.
    try:
        requests.get(path, timeout=5)
        return True
    except requests.exceptions.Timeout as e:
        logging.error("ESP32 request timed out")
        return False  # Server not available
    except requests.exceptions.RequestException as e:
        return True   # We expect this

def send_image(img):
    host = os.environ['HKDASH_ESP32_HOST']
    # The server on the ESP32 expects commands and data in the path of the request
    
    # Begin write
    success = make_request(f"{host}/EPDw_")
    if not success:
        return  # Don't bother to continue
    
    # Write 1000 characters per request
    bits = np.asarray(img).reshape(-1)
    for i in range(0, bits.shape[0], 4000):
        # Data is sent in chunks of 1000 characters, representing 4000 bits
        line = encode_bit_array(bits[i:(i+4000)])
        success = make_request(f"{host}/{line}iodaLOAD_")
        if not success:
            return  # Don't bother to continue

    # Finalize
    make_request(f"{host}/SHOW_")
