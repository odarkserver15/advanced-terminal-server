import os
import pty
import subprocess
import time
from threading import Thread

class TerminalManager:
    def __init__(self):
        self.pty = None
        self.process = None

    def start_session(self, command):
        # Start a new pseudo-terminal and the specified command
        self.pty, self.process = pty.fork()
        if self.pty == 0:  # Child process
            os.execlp(command[0], *command)

    def read_output(self):
        if self.pty:
            while True:
                output = os.read(self.pty, 1024).decode()
                print(output, end='')

    def write_input(self, input_string):
        if self.pty:
            os.write(self.pty, input_string.encode())

    def stop_session(self):
        if self.process:
            os.kill(self.process, 15)  # Sending SIGTERM
            self.process = None
            self.pty = None

    def run(self, command):
        self.start_session(command)
        output_thread = Thread(target=self.read_output)
        output_thread.start()  # Start reading output in a separate thread

        return self

# Example Usage
if __name__ == '__main__':
    terminal = TerminalManager()
    terminal.run(['bash'])  # Start a bash session
    time.sleep(10)  # Keep the session alive for demonstration
    terminal.stop_session()  # Stop the session
