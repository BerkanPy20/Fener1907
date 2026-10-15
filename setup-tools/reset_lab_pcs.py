#!/usr/bin/env python3
import argparse
import paramiko
import socket

# Configuration
REPO_PATH = "/home/johbaum8/build-your-own-chatbot-stud"
RESET_CMD = "git reset --hard origin/main"
SUCCESS_INDICATOR = "Your branch is up to date with 'origin/main'"

def process_ip(ip, username, password):
    """
    Connects via SSH to the given IP, resets the git repository,
    and checks if the reset was successful.
    
    Returns:
        (success_flag, details) tuple.
    """
    try:
        # Set up the SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, timeout=10)
        
        # Execute the git reset command
        reset_full_cmd = f"cd {REPO_PATH} && {RESET_CMD}"
        _, stdout_reset, stderr_reset = ssh.exec_command(reset_full_cmd)
        reset_output = stdout_reset.read().decode() + stderr_reset.read().decode()
        
        # Execute the git status command to verify the reset
        status_full_cmd = f"cd {REPO_PATH} && git status"
        _, stdout_status, stderr_status = ssh.exec_command(status_full_cmd)
        status_output = stdout_status.read().decode() + stderr_status.read().decode()
        
        # Determine if the reset was successful based on the status output
        if SUCCESS_INDICATOR in status_output:
            result = (True, "Reset successful")
        else:
            result = (False, f"Unexpected git status output:\n{status_output}")
        
        ssh.close()
        return result

    except (socket.timeout, paramiko.AuthenticationException, paramiko.SSHException) as e:
        return (False, f"SSH error: {e}")
    except Exception as e:
        return (False, f"General error: {e}")

def generate_ip_list(single_ip=None, ip_range=None):
    """
    Generates a list of IP addresses.
    
    Parameters:
        single_ip (str): A single IP address to target.
        ip_range (tuple): A tuple of (start_ip, end_ip).
    
    Returns:
        List of IP addresses.
    """
    if single_ip:
        return [single_ip]
    elif ip_range:
        start_ip, end_ip = ip_range
        # Assuming the first three octets are identical and only the last octet varies
        base = ".".join(start_ip.split(".")[:-1]) + "."
        start_octet = int(start_ip.split(".")[-1])
        end_octet = int(end_ip.split(".")[-1])
        return [base + str(i) for i in range(start_octet, end_octet + 1)]
    else:
        # Default range: 192.168.4.101 to 192.168.4.125
        
        return [""]

def main():
    parser = argparse.ArgumentParser(
        description="Automate the reset of Git repositories on remote PCs via SSH."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--ip", help="Target a single IP address (e.g., 192.168.4.105)."
    )
    group.add_argument(
        "--range", nargs=2, metavar=("START_IP", "END_IP"),
        help="Target a range of IP addresses (e.g., 192.168.4.101 192.168.4.125)."
     )
    parser.add_argument(
        "--user", default="johbaum8", help="SSH username (default: johbaum8)."
    )
    parser.add_argument(
        "--passwd", help="SSH password."
    )
    args = parser.parse_args()

    # Generate the list of IPs based on provided arguments
    if args.ip:
        ip_list = generate_ip_list(single_ip=args.ip)
    elif args.range:
        ip_list = generate_ip_list(ip_range=(args.range[0], args.range[1]))
    else:
        ip_list = generate_ip_list()
        parser.print_help()
        return


    status_report = {}

    print("Starting Git repository reset on target PCs...\n")
    for ip in ip_list:
        print(f"Processing {ip} ...")
        success, details = process_ip(ip, username=args.user, password=args.passwd)
        status_report[ip] = {"success": success, "details": details}
        print(f"Status for {ip}: {'SUCCESS' if success else 'FAILED'}\n")

    print("\nFinal Status Report:")
    for ip, report in status_report.items():
        print(f"{ip}: {'SUCCESS' if report['success'] else 'FAILED'}")
        if not report["success"]:
            print(f"    Details: {report['details']}")

if __name__ == "__main__":
    main()