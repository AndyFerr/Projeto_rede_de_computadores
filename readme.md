# Instructions for Running the Chat Program

## Prerequisites

- Python 3.x installed on your system
- pip installed on your system

## Running on Linux

1. Convert the files to Unix type:
   - Install dos2unix command: `sudo pip install dos2unix`
   - Allow the execution: `chmod +x script.py`
   - Run: `dos2unix server_3.py`
   - Run: `dos2unix client_3.py`

2. Find the local host IP address:
   - On Linux, run: `hostname -I`
   - On Windows, run: `ipconfig`

3. Set the host IP on `servers_address` in `client_3.py` file.

4. Make sure both programs are using the same port.

5. Run the server first and then run the client.

6. Set a nickname and start using the chat.

7. Configure the corresponding port on your firewall allowing the system to connect to all.

## Running on Windows

1. Make sure Python 3.x is installed on your system.

2. Set the host IP on `servers_address` in `client_3.py` file.

3. Make sure both programs are using the same port.

4. Run the server first and then run the client.

5. Set a nickname and start using the chat.

6. Configure the corresponding port on your firewall to allow the system to connect to all.

## Troubleshooting

If you encounter any issues, please check the following:

- Make sure Python and pip are installed correctly.
- Check the firewall settings to ensure the port is open.
- Verify that the host IP address is correct.
- Check the file permissions if running on Linux.

## License

This project is licensed under the [MIT License](LICENSE).