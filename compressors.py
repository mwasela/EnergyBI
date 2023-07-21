# GBHL COMPRESSOR DATA HARVESTING SCRIPT 
# COMPRESSOR TA - 001
# IP = 192.168.5.250
# Running through SERA networks on Python TESTBED SERVER


import time
import asyncio
from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer


def setup_async_client(port):
    """Run client setup."""
  
    client = ModbusTcpClient(
            host = "192.168.5.250",
            port=502,
            framer=ModbusRtuFramer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # source_address=("localhost", 0),
        )
    return client



def get_dynamic_values():
    """Test connection works."""
    client = ModbusTcpClient(
            host = "192.168.5.250",
            port=502,
            framer=ModbusRtuFramer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
    )
    client.connect()

    runningHrs = client.read_holding_registers(58, 1, slave=2)
    loadedHrs  = client.read_holding_registers(60, 1, slave=2)
    temperature  = client.read_holding_registers(42, 1, slave=2)
    client.close()
    
    print(f"Running hours -> {runningHrs.registers[0]}")
    print(f"Loaded hours -> {loadedHrs.registers[0]}")
    print(f"Temperature -> {temperature.registers[0]}")

    return runningHrs.registers[0], loadedHrs.registers[0], temperature.registers[0]


def write_to_file(file_path, data):
    with open(file_path, "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\nTime: {timestamp}")
        f.write("\nRunning Hours: {}\nLoaded Hours: {}\nTemprature: {} Deg Celsius\n\n".format(*data))

def get_file_path(file_prefix):
    current_date = time.strftime("%Y-%m-%d")
    return f"{file_prefix}_{current_date}.txt"

file_prefix = "Compressor TA001"
file_path = get_file_path(file_prefix)

while True:
    x, y, z = get_dynamic_values()
    write_to_file(file_path, (x, y, z))
    
    # Sleep for 30 minutes (1800 seconds)
    time.sleep(1800)
    
    # Check if 24 hours have passed, then create a new file
    current_file_path = get_file_path(file_prefix)
    if current_file_path != file_path:
        file_path = current_file_path
