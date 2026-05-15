import FreeSimpleGUI as sg
import time
from datetime import datetime

# Optional later:
# import serial
# import serial.tools.list_ports


class ESP32Interface:
    """
    Placeholder class for future ESP32 communication.
    Later, this can use pyserial to send commands to the ESP32.
    """

    def __init__(self):
        self.connected = False
        self.port = None
        self.baudrate = 115200
        # self.serial_connection = None

    def connect(self, port: str, baudrate: int = 115200):
        """
        Future serial connection code will go here.
        """
        self.port = port
        self.baudrate = baudrate

        # Example for later:
        # self.serial_connection = serial.Serial(port, baudrate, timeout=1)
        # time.sleep(2)

        self.connected = True
        return True

    def disconnect(self):
        """
        Future serial disconnect code will go here.
        """
        # if self.serial_connection and self.serial_connection.is_open:
        #     self.serial_connection.close()

        self.connected = False
        self.port = None

    def send_command(self, command: str):
        """
        Future command sending.
        For now, this just returns a fake response.
        """
        if not self.connected:
            return "ERROR: ESP32 not connected"

        # Example for later:
        # self.serial_connection.write((command + "\n").encode())
        # response = self.serial_connection.readline().decode().strip()
        # return response

        return f"Simulated ESP32 response to: {command}"

    def read_voltage_data(self):
        """
        Placeholder for future voltage/current readings.
        Eventually this could request data from ESP32.
        """
        if not self.connected:
            return None

        # Fake data for GUI testing
        return {
            "vin": 24.0,
            "vout": 3.3,
            "input_adc": 2700,
            "output_adc": 370,
            "load_state": "OFF"
        }


def build_window():
    sg.theme("Dark")

    connection_layout = [
        [sg.Text("ESP32 Connection", font=("Arial", 14, "bold"))],
        [
            sg.Text("Port:", size=(10, 1)),
            sg.Combo(
                values=["COM3", "COM4", "COM5", "COM6", "COM8", "COM10"],
                default_value="COM3",
                key="-PORT-",
                size=(15, 1)
            ),
            sg.Text("Baud:"),
            sg.Combo(["115200",], key="-BAUD-", size=(10, 1)),
        ],
        [
            sg.Button("Connect", key="-CONNECT-"),
            sg.Button("Disconnect", key="-DISCONNECT-"),
            sg.Text("Status: Disconnected", key="-STATUS-", text_color="red")
        ]
    ]

    measurement_layout = [
        [sg.Text("Voltage Measurements", font=("Arial", 14, "bold"))],
        [
            sg.Text("Input Voltage:", size=(18, 1)),
            sg.Text("-- V", key="-VIN-", size=(12, 1))
        ],
        [
            sg.Text("Output Voltage:", size=(18, 1)),
            sg.Text("-- V", key="-VOUT-", size=(12, 1))
        ],
        [
            sg.Text("Input ADC Raw:", size=(18, 1)),
            sg.Text("--", key="-INPUT-ADC-", size=(12, 1))
        ],
        [
            sg.Text("Output ADC Raw:", size=(18, 1)),
            sg.Text("--", key="-OUTPUT-ADC-", size=(12, 1))
        ],
        [
            sg.Text("Load State:", size=(18, 1)),
            sg.Text("--", key="-LOAD-STATE-", size=(12, 1))
        ],
        [
            sg.Button("Read Once", key="-READ-ONCE-"),
            sg.Button("Start Monitoring", key="-START-MONITOR-"),
            sg.Button("Stop Monitoring", key="-STOP-MONITOR-")
        ]
    ]

    control_layout = [
        [sg.Text("Load Control", font=("Arial", 14, "bold"))],
        [
            sg.Button("Load ON", key="-LOAD-ON-"),
            sg.Button("Load OFF", key="-LOAD-OFF-")
        ],
        [
            sg.Button("Run Load Step Test", key="-LOAD-STEP-")
        ],
        [sg.HorizontalSeparator()],
        [sg.Text("Manual ESP32 Command")],
        [
            sg.Input(key="-MANUAL-COMMAND-", size=(35, 1)),
            sg.Button("Send", key="-SEND-COMMAND-")
        ]
    ]

    log_layout = [
        [sg.Text("Event Log", font=("Arial", 14, "bold"))],
        [
            sg.Multiline(
                size=(80, 15),
                key="-LOG-",
                disabled=True,
                autoscroll=True
            )
        ],
        [
            sg.Button("Clear Log", key="-CLEAR-LOG-"),
            sg.Button("Exit")
        ]
    ]

    layout = [
        [
            sg.Column(connection_layout, vertical_alignment="top"),
            sg.VerticalSeparator(),
            sg.Column(measurement_layout, vertical_alignment="top"),
            sg.VerticalSeparator(),
            sg.Column(control_layout, vertical_alignment="top"),
        ],
        [sg.HorizontalSeparator()],
        [sg.Column(log_layout)]
    ]

    return sg.Window("LM2596S DC-DC Converter Validation GUI", layout, finalize=True)


def log_message(window, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    window["-LOG-"].update(f"[{timestamp}] {message}\n", append=True)


def update_measurement_display(window, data):
    if data is None:
        return

    window["-VIN-"].update(f"{data['vin']:.2f} V")
    window["-VOUT-"].update(f"{data['vout']:.2f} V")
    window["-INPUT-ADC-"].update(str(data["input_adc"]))
    window["-OUTPUT-ADC-"].update(str(data["output_adc"]))
    window["-LOAD-STATE-"].update(data["load_state"])


def main():
    esp32 = ESP32Interface()
    window = build_window()

    monitoring_enabled = False

    while True:
        event, values = window.read(timeout=500)

        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "-CONNECT-":
            port = values["-PORT-"]

            try:
                baudrate = int(values["-BAUD-"])
                esp32.connect(port, baudrate)

                window["-STATUS-"].update(
                    f"Status: Connected to {port}",
                    text_color="lightgreen"
                )

                log_message(window, f"Connected to ESP32 on {port} at {baudrate} baud")

            except ValueError:
                log_message(window, "Invalid baudrate entered")

        elif event == "-DISCONNECT-":
            esp32.disconnect()
            monitoring_enabled = False

            window["-STATUS-"].update(
                "Status: Disconnected",
                text_color="red"
            )

            log_message(window, "Disconnected from ESP32")

        elif event == "-READ-ONCE-":
            data = esp32.read_voltage_data()

            if data is None:
                log_message(window, "Cannot read data: ESP32 not connected")
            else:
                update_measurement_display(window, data)
                log_message(window, "Read voltage data once")

        elif event == "-START-MONITOR-":
            if esp32.connected:
                monitoring_enabled = True
                log_message(window, "Started live monitoring")
            else:
                log_message(window, "Cannot start monitoring: ESP32 not connected")

        elif event == "-STOP-MONITOR-":
            monitoring_enabled = False
            log_message(window, "Stopped live monitoring")

        elif event == "-LOAD-ON-":
            response = esp32.send_command("LOAD_ON")
            log_message(window, response)

        elif event == "-LOAD-OFF-":
            response = esp32.send_command("LOAD_OFF")
            log_message(window, response)

        elif event == "-LOAD-STEP-":
            response = esp32.send_command("RUN_LOAD_STEP_TEST")
            log_message(window, response)

        elif event == "-SEND-COMMAND-":
            command = values["-MANUAL-COMMAND-"].strip()

            if command:
                response = esp32.send_command(command)
                log_message(window, response)
            else:
                log_message(window, "No command entered")

        elif event == "-CLEAR-LOG-":
            window["-LOG-"].update("")

        # Auto-monitoring loop
        if monitoring_enabled and esp32.connected:
            data = esp32.read_voltage_data()

            if data is not None:
                update_measurement_display(window, data)
                log_message(
                    window,
                    f"Vin={data['vin']:.2f} V, Vout={data['vout']:.2f} V, Load={data['load_state']}"
                )

    esp32.disconnect()
    window.close()


if __name__ == "__main__":
    main()