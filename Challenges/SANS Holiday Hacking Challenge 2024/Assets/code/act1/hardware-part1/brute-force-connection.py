import requests
import json
import itertools
import time
from datetime import datetime


def try_uart_combinations():
    # API endpoint
    url = 'https://hhc24-hardwarehacking.holidayhackchallenge.com/api/v1/complete'

    # Define all possible values for each parameter
    ports = list(range(4))  # [0,1,2,3] for ["COM1", "COM2", "COM3", "USB0"]
    baud_rates = list(range(10))  # [0-9] for [300, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200]
    parity = list(range(3))  # [0,1,2] for ["None", "odd", "even"]
    data_bits = list(range(4))  # [0,1,2,3] for [5, 6, 7, 8]
    stop_bits = list(range(2))  # [0,1] for [1, 2]
    flow_control = list(range(4))  # [0,1,2,3] for ["None", "RTS/CTS", "Xon/Xoff", "RTS"]

    # Headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    # Value mappings for logging
    baud_map = [300, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200]
    parity_map = ["None", "odd", "even"]
    data_map = [5, 6, 7, 8]
    stop_map = [1, 2]
    flow_map = ["None", "RTS/CTS", "Xon/Xoff", "RTS"]
    port_map = ["COM1", "COM2", "COM3", "USB0"]

    # Create log file
    log_filename = f"uart_attempts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # Counter for attempts
    attempt_count = 0

    print("Starting UART parameter bruteforce...")
    print(f"Logging results to: {log_filename}")

    try:
        with open(log_filename, 'w') as log_file:
            # Try all possible combinations
            for port, baud, par, data, stop, flow in itertools.product(
                    ports, baud_rates, parity, data_bits, stop_bits, flow_control):

                attempt_count += 1
                serial_params = [port, baud, par, data, stop, flow]

                payload = {
                    'requestID': '3931cf5e-c22e-42a0-bf52-0952ab0df1b8',
                    'serial': serial_params,
                    'voltage': 3
                }

                # Log attempt details
                log_message = (f"\nAttempt #{attempt_count}\n"
                               f"Port: {port_map[port]}, "
                               f"Baud: {baud_map[baud]}, "
                               f"Parity: {parity_map[par]}, "
                               f"Data: {data_map[data]}, "
                               f"Stop: {stop_map[stop]}, "
                               f"Flow: {flow_map[flow]}")

                print(log_message)
                log_file.write(log_message + '\n')

                try:
                    response = requests.post(url, json=payload, headers=headers)
                    result = response.text

                    log_message = f"Response: {result}\n"
                    print(log_message)
                    log_file.write(log_message)

                    # If we get a successful response, save the working combination
                    if response.status_code == 200 and 'true' in result.lower():
                        success_message = f"\nSUCCESS! Working combination found:\n{json.dumps(payload, indent=2)}"
                        print(success_message)
                        log_file.write(success_message)
                        return payload  # Return the working combination

                    # Add a small delay to avoid overwhelming the server
                    time.sleep(0.5)

                except requests.exceptions.RequestException as e:
                    error_message = f"Error occurred: {e}\n"
                    print(error_message)
                    log_file.write(error_message)
                    time.sleep(1)  # Longer delay after an error
                    continue

    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        return None

    print("\nAll combinations tried without success")
    return None


if __name__ == "__main__":
    print("UART Parameter Bruteforce Script")
    print("-------------------------------")
    working_combo = try_uart_combinations()

    if working_combo:
        print("\nSuccessful combination found!")
        print(json.dumps(working_combo, indent=2))
    else:
        print("\nNo working combination found")