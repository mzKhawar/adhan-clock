# need to check if bluetooth is connected.
#
# open command line,
# type 'bluetoothctl'
# type 'connect 6C:21:A2:80:53:71'
# type 'quit'

import subprocess
import sys


def communicate_with_bluetoothctl(process, command):
    # Send command to the process
    process.stdin.write(command + "\n")
    process.stdin.flush()

    # Read the output until "Connection successful" is found or the process is finished
    while True:
        output = process.stdout.readline().strip()
        if output:
            print(output)
        if "Connection successful" in output:
            process.stdin.write("quit\n")  # Send the 'quit' command
            process.stdin.flush()
            break
        if process.poll() is not None:
            break

    # Terminate the process if it's still running
    if process.poll() is None:
        process.terminate()

    # Wait for the process to finish and read any remaining output
    process.wait()
    remaining_output = process.stdout.read().strip()
    if remaining_output:
        print(remaining_output)


# Start the 'bluetoothctl' process
process = subprocess.Popen(
    ["bluetoothctl"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
)

# Send the 'connect' command
command = "connect 6C:21:A2:80:53:71"  # Replace [device_address] with the address of the Bluetooth device
communicate_with_bluetoothctl(process, command)

# Close the process
process.stdin.close()
process.stdout.close()

sys.exit()
