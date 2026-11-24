import ipaddress
import socket


def main():
    try:
        target = ipaddress.ip_address(input("Target IP (127.0.0.1 or ::1): ").strip())
        if not target.is_loopback:
            raise ValueError("This utility is limited to loopback addresses.")

        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
        timeout = float(input("Timeout in seconds (e.g. 1): "))

        if not (1 <= start_port <= end_port <= 65535):
            raise ValueError("Enter a valid port range from 1 to 65535.")
        if end_port - start_port + 1 > 1024:
            raise ValueError("Please scan no more than 1,024 ports per run.")
        if timeout <= 0:
            raise ValueError("Timeout must be greater than zero.")

    except ValueError as error:
        print(f"Input error: {error}")
        return

    family = socket.AF_INET6 if target.version == 6 else socket.AF_INET
    print(f"\n{'PORT':<10}STATUS")
    print("-" * 24)

    for port in range(start_port, end_port + 1):
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect((str(target), port))
                status = "Open"
            except ConnectionRefusedError:
                status = "Closed"
            except (TimeoutError, socket.timeout):
                status = "Filtered / no response"
            except OSError as error:
                status = f"Error: {error}"

        print(f"{port:<10}{status}")


if __name__ == "__main__":
    main()