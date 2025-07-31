# created by @joshua jenkins v0.1 - 2025-06-26
#!/usr/bin/env python3

# Import standard and third-party libraries
import argparse
import os
import sys
import json
import base64
import requests
from dotenv import load_dotenv
from colorama import Fore, Style, init as colorama_init
import questionary
import getpass

# Initialize colorama for colored terminal output
def colorama_init(autoreset=True):
    pass
colorama_init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Environment variable name for Horizon API base URL
API_BASE_ENV = 'HORIZON_API_BASE'

# ASCII art and program name displayed at startup
ASCII_ART = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢿⣧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⡀⠀⠀⢀⡴⠛⠁⠀⠘⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣷⣤⡴⠋⠀⠀⠀⠀⠀⢿⣇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠈⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢏⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣷⣾⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢿⡇
⠀⠀⠀⠀⠀⠀⠀⢀⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⢠⡞⠁⢹⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⣠⠟⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣴⠋⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⢀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

PROGRAM_NAME = 'rhvd reaper'

# Print ASCII art and program name at the start of the CLI
print(Fore.LIGHTBLACK_EX + ASCII_ART)
print(Fore.CYAN + Style.BRIGHT + f'Welcome to {PROGRAM_NAME}\n')
print(Fore.LIGHTBLACK_EX + f'Logged in as: {getpass.getuser()}')

# ----------------------
# Helper and CLI functions
# ----------------------

def display_comprehensive_help():
    """Display detailed help and usage information for the CLI."""
    print(Fore.CYAN + Style.BRIGHT + '\nRHVD - Horizon Forensics CLI Tool')
    print(Fore.LIGHTBLACK_EX + 'A command-line interface tool for VMware Horizon forensics operations\n')
    print(Fore.CYAN + Style.BRIGHT + 'Available Commands:')
    print(Fore.WHITE + '  hold-user [userSid]           Put an Active Directory user on forensic hold')
    print(Fore.WHITE + '  archive-vm [vmId]             Archive a virtual machine by VM ID')
    print(Fore.WHITE + '  release-hold [userSid]        Release a user from forensic hold')
    print(Fore.WHITE + '  list-held-users               List all currently held users')
    print(Fore.WHITE + '  list-held-machines            List all machines currently on forensic hold')
    print(Fore.WHITE + '  mark-archival-datastore       Mark one or more datastores for archival for a given vCenter')
    print(Fore.WHITE + '  interactive                   Run in interactive mode with menu options')
    print(Fore.WHITE + '  help                          Show this comprehensive help information\n')
    print(Fore.CYAN + Style.BRIGHT + 'Command Options:')
    print(Fore.WHITE + '  -u, --username <username>         Horizon API Username')
    print(Fore.WHITE + '  -p, --password <password>         Horizon API Password')
    print(Fore.WHITE + '  -b, --base-url <url>              Horizon API Base URL')
    print(Fore.WHITE + '  --vcenter-id <vcenter_id>         vCenter ID (for mark-archival-datastore)')
    print(Fore.WHITE + '  --datastore-ids <ids>             Comma-separated list of datastore IDs (for mark-archival-datastore)')
    print(Fore.WHITE + '  -h, --help                        Show command-specific help\n')
    print(Fore.CYAN + Style.BRIGHT + 'Horizon API Base URL Configuration:')
    print(Fore.LIGHTBLACK_EX + 'The Horizon API Base URL may require a specific port depending on your VMware Horizon server configuration.\n')
    print(Fore.CYAN + Style.BRIGHT + 'Default HTTPS (Port 443):')
    print(Fore.WHITE + '  If your Horizon server uses the default HTTPS port, you typically don\'t need to specify the port:')
    print(Fore.LIGHTBLACK_EX + '  https://horizon.company.com\n')
    print(Fore.CYAN + Style.BRIGHT + 'Custom HTTPS Port:')
    print(Fore.WHITE + '  If your Horizon server uses a custom HTTPS port, you must specify it:')
    print(Fore.LIGHTBLACK_EX + '  https://horizon.company.com:8443')
    print(Fore.LIGHTBLACK_EX + '  https://horizon.company.com:9443\n')
    print(Fore.CYAN + Style.BRIGHT + 'Common VMware Horizon Ports:')
    print(Fore.WHITE + '  | Service                    | Default Port | Protocol |')
    print(Fore.WHITE + '  |----------------------------|--------------|----------|')
    print(Fore.WHITE + '  | Horizon Connection Server | 443          | HTTPS    |')
    print(Fore.WHITE + '  | Horizon Connection Server | 8443, 9443   | HTTPS    |')
    print(Fore.WHITE + '  | Horizon UAG               | 443          | HTTPS    |')
    print(Fore.WHITE + '  | Horizon UAG (custom)      | 8443, 9443   | HTTPS    |')
    print('')
    print(Fore.YELLOW + ' Tip: Start without a port, add :8443 or :9443 if connection fails\n')
    print(Fore.CYAN + Style.BRIGHT + 'Usage Examples:')
    print(Fore.CYAN + Style.BRIGHT + 'Interactive Mode (Recommended for beginners):')
    print(Fore.LIGHTBLACK_EX + '  python cli.py interactive\n')
    print(Fore.CYAN + Style.BRIGHT + 'Command Line Mode:')
    print(Fore.LIGHTBLACK_EX + '  # Interactive prompts for base URL, user SID, and credentials')
    print(Fore.WHITE + '  python cli.py hold-user\n')
    print(Fore.LIGHTBLACK_EX + '  # With user SID provided (default port 443)')
    print(Fore.WHITE + '  python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234\n')
    print(Fore.LIGHTBLACK_EX + '  # With custom port and credentials')
    print(Fore.WHITE + '  python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234 -b https://horizon-server.com:8443 -u username -p password\n')
    print(Fore.LIGHTBLACK_EX + '  # List all currently held users')
    print(Fore.WHITE + '  python cli.py list-held-users\n')
    print(Fore.LIGHTBLACK_EX + '  # List all machines currently on forensic hold')
    print(Fore.WHITE + '  python cli.py list-held-machines\n')
    print(Fore.LIGHTBLACK_EX + '  # Mark datastores for archival for a given vCenter')
    print(Fore.WHITE + '  python cli.py mark-archival-datastore --vcenter-id vcenter-123 --datastore-ids ds-1,ds-2\n')
    print(Fore.CYAN + Style.BRIGHT + 'Environment Variables:')
    print(Fore.LIGHTBLACK_EX + '  Create a .env file in the backend directory (optional):')
    print(Fore.WHITE + '  HORIZON_API_BASE=https://your-horizon-server.com\n')
    print(Fore.CYAN + Style.BRIGHT + 'Security Notes:')
    print(Fore.WHITE + '  - Credentials are only stored in memory during the session')
    print(Fore.WHITE + '  - Passwords are hidden when entered interactively')
    print(Fore.WHITE + '  - Base URL is validated for proper format')
    print(Fore.WHITE + '  - Consider using environment variables for credentials in production')
    print(Fore.WHITE + '  - The .env file should not be committed to version control\n')
    print(Fore.CYAN + Style.BRIGHT + 'Error Handling:')
    print(Fore.WHITE + '  The CLI provides clear error messages for:')
    print(Fore.WHITE + '  - Missing credentials')
    print(Fore.WHITE + '  - Invalid API responses')
    print(Fore.WHITE + '  - Network connectivity issues')
    print(Fore.WHITE + '  - Invalid user SIDs or VM IDs')
    print(Fore.WHITE + '  - Invalid base URL format\n')
    print(Fore.CYAN + Style.BRIGHT + 'Getting Help:')
    print(Fore.WHITE + '  python cli.py --help                         # Show general help')
    print(Fore.WHITE + '  python cli.py help                           # Show this comprehensive help')
    print(Fore.WHITE + '  python cli.py interactive                    # Interactive mode with help option')
    print(Fore.WHITE + '  python cli.py hold-user --help               # Show command-specific help')
    print(Fore.WHITE + '  python cli.py archive-vm --help              # Show command-specific help')
    print(Fore.WHITE + '  python cli.py release-hold --help            # Show command-specific help')
    print(Fore.WHITE + '  python cli.py list-held-users --help         # Show command-specific help')
    print(Fore.WHITE + '  python cli.py list-held-machines --help      # Show command-specific help')
    print(Fore.WHITE + '  python cli.py mark-archival-datastore --help # Show command-specific help')
    print(Fore.WHITE + '  python cli.py interactive --help             # Show command-specific help\n')
    print(Fore.LIGHTBLACK_EX + 'For more information, visit the project documentation or contact your VMware administrator.')

def get_base_url(cli_base_url=None):
    """Get the Horizon API base URL from CLI, environment, or prompt. Enforces HTTPS for security."""
    base_url = cli_base_url or os.getenv(API_BASE_ENV)
    if not base_url:
        print(Fore.CYAN + '\n Horizon API Base URL Guidelines:')
        print(Fore.LIGHTBLACK_EX + '• Default HTTPS (port 443): https://horizon-server.com')
        print(Fore.LIGHTBLACK_EX + '• Custom HTTPS port: https://horizon-server.com:8443')
        print(Fore.LIGHTBLACK_EX + '• HTTP (not recommended): http://horizon-server.com:8080')
        print(Fore.LIGHTBLACK_EX + '• Common VMware Horizon ports: 443, 8443, 9443')
        print(Fore.WHITE + ' Tip: Start without a port, add :8443 or :9443 if connection fails\n')
        base_url = questionary.text('Enter Horizon API Base URL (e.g., https://horizon-server.com or https://horizon-server.com:8443):').ask()
    base_url = base_url.strip()
    if not base_url.lower().startswith('https://'):
        print(Fore.RED + 'ERROR: Insecure base URL detected. Please use HTTPS to protect your credentials in transit.')
        sys.exit(1)
    return base_url

def get_credentials(cli_user=None, cli_pass=None):
    """Prompt for API username and password if not provided."""
    api_user = cli_user or questionary.text('Enter Horizon API Username:').ask()
    api_pass = cli_pass or questionary.password('Enter Horizon API Password:').ask()
    return api_user, api_pass

def create_auth_header(api_user, api_pass):
    """Create HTTP Basic Auth header for API requests."""
    token = base64.b64encode(f"{api_user}:{api_pass}".encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

def display_result(data, operation):
    """Display the result of a successful operation."""
    print(Fore.GREEN + f"\n {operation} completed successfully!")
    print(Fore.CYAN + 'Response:')
    print(json.dumps(data, indent=2))

def display_error(error, operation):
    """Display error details for failed operations."""
    print(Fore.RED + f"\n {operation} failed!")
    if hasattr(error, 'response') and error.response is not None:
        print(Fore.RED + f"Status: {error.response.status_code}")
        try:
            print(Fore.RED + f"Error: {error.response.json().get('error', error.response.text)}")
        except Exception:
            print(Fore.RED + f"Error: {error.response.text}")
    else:
        print(Fore.RED + f"Error: {str(error)}")

def hold_user(args):
    """Command: Put an Active Directory user on forensic hold."""
    try:
        base_url = get_base_url(args.base_url)
        user_sid = args.userSid or questionary.text('Enter User Security Identifier (SID):').ask()
        api_user, api_pass = get_credentials(args.username, args.password)
        print(Fore.WHITE + f"\n Putting user {user_sid} on forensic hold...")
        headers = create_auth_header(api_user, api_pass)
        resp = requests.post(f"{base_url}/external/v1/ad-users-or-groups/action/hold", json={"securityIdentifiers": [user_sid]}, headers=headers)
        resp.raise_for_status()
        display_result(resp.json(), 'User Hold')
    except Exception as e:
        display_error(e, 'User Hold')
        sys.exit(1)

def archive_vm(args):
    """Command: Archive a virtual machine by VM ID."""
    try:
        base_url = get_base_url(args.base_url)
        vm_id = args.vmId or questionary.text('Enter VM ID:').ask()
        api_user, api_pass = get_credentials(args.username, args.password)
        print(Fore.WHITE + f"\n Archiving VM {vm_id}...")
        headers = create_auth_header(api_user, api_pass)
        resp = requests.post(f"{base_url}/inventory/v1/machines/action/archive", json={"ids": [vm_id]}, headers=headers)
        resp.raise_for_status()
        display_result(resp.json(), 'VM Archive')
    except Exception as e:
        display_error(e, 'VM Archive')
        sys.exit(1)

def release_hold(args):
    """Command: Release a user from forensic hold."""
    try:
        base_url = get_base_url(args.base_url)
        user_sid = args.userSid or questionary.text('Enter User Security Identifier (SID):').ask()
        api_user, api_pass = get_credentials(args.username, args.password)
        print(Fore.WHITE + f"\n Releasing user {user_sid} from forensic hold...")
        headers = create_auth_header(api_user, api_pass)
        resp = requests.post(f"{base_url}/external/v1/ad-users-or-groups/action/release-hold", json={"securityIdentifiers": [user_sid]}, headers=headers)
        resp.raise_for_status()
        display_result(resp.json(), 'User Release')
    except Exception as e:
        display_error(e, 'User Release')
        sys.exit(1)

def list_held_users(args):
    """Command: List all currently held users."""
    try:
        base_url = get_base_url(args.base_url)
        api_user, api_pass = get_credentials(args.username, args.password)
        print(Fore.WHITE + '\n Fetching list of held users...')
        headers = create_auth_header(api_user, api_pass)
        resp = requests.get(f"{base_url}/external/v1/ad-users-or-groups/held-users-or-groups", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data and len(data) > 0:
            print(Fore.GREEN + f"\n Found {len(data)} held user(s):")
            for idx, user in enumerate(data, 1):
                print(Fore.CYAN + f"\n{idx}. User Details:")
                print(json.dumps(user, indent=2))
        else:
            print(Fore.GREEN + '\n No users are currently on forensic hold.')
    except Exception as e:
        display_error(e, 'List Held Users')
        sys.exit(1)

def interactive_menu(args):
    """Command: Run the CLI in interactive menu mode."""
    try:
        base_url = get_base_url(args.base_url)
        api_user, api_pass = get_credentials(args.username, args.password)
        print(Fore.GREEN + ' Credentials set successfully!')
        while True:
            action = questionary.select(
                'What would you like to do?',
                choices=[
                    'Archive VM',
                    'Put User on Hold',
                    'List Held Users',
                    'List Held Machines',
                    'Release User from Hold',
                    'Mark Archival Datastore',
                    'Help',
                    'Exit'
                ]
            ).ask()
            if action is None or action == 'Exit':
                print(Fore.WHITE + "\nSession closed by user (Exit command or Ctrl+C). Goodbye! Thanks for using the Horizon Forensics CLI Tool!")
                sys.exit(0)
            elif action == 'Help':
                display_comprehensive_help()
                continue
            try:
                if action == 'Put User on Hold':
                    user_sid = questionary.text('Enter User Security Identifier (SID):').ask()
                    print(Fore.WHITE + f"\n Putting user {user_sid} on forensic hold...")
                    headers = create_auth_header(api_user, api_pass)
                    resp = requests.post(f"{base_url}/external/v1/ad-users-or-groups/action/hold", json={"securityIdentifiers": [user_sid]}, headers=headers)
                    resp.raise_for_status()
                    display_result(resp.json(), 'User Hold')
                elif action == 'Archive VM':
                    vm_id = questionary.text('Enter VM ID:').ask()
                    print(Fore.WHITE + f"\n Archiving VM {vm_id}...")
                    headers = create_auth_header(api_user, api_pass)
                    resp = requests.post(f"{base_url}/inventory/v1/machines/action/archive", json={"ids": [vm_id]}, headers=headers)
                    resp.raise_for_status()
                    display_result(resp.json(), 'VM Archive')
                elif action == 'Release User from Hold':
                    user_sid = questionary.text('Enter User Security Identifier (SID):').ask()
                    print(Fore.WHITE + f"\n Releasing user {user_sid} from forensic hold...")
                    headers = create_auth_header(api_user, api_pass)
                    resp = requests.post(f"{base_url}/external/v1/ad-users-or-groups/action/release-hold", json={"securityIdentifiers": [user_sid]}, headers=headers)
                    resp.raise_for_status()
                    display_result(resp.json(), 'User Release')
                elif action == 'List Held Users':
                    print(Fore.WHITE + '\n Fetching list of held users...')
                    headers = create_auth_header(api_user, api_pass)
                    resp = requests.get(f"{base_url}/external/v1/ad-users-or-groups/held-users-or-groups", headers=headers)
                    resp.raise_for_status()
                    data = resp.json()
                    if data and len(data) > 0:
                        print(Fore.GREEN + f"\n Found {len(data)} held user(s):")
                        for idx, user in enumerate(data, 1):
                            print(Fore.CYAN + f"\n{idx}. User Details:")
                            print(json.dumps(user, indent=2))
                    else:
                        print(Fore.GREEN + '\n No users are currently on forensic hold.')
                elif action == 'List Held Machines':
                    list_held_machines(args)
                elif action == 'Mark Archival Datastore':
                    # Ensure args has vcenter_id and datastore_ids attributes for interactive mode
                    if not hasattr(args, 'vcenter_id'):
                        setattr(args, 'vcenter_id', None)
                    if not hasattr(args, 'datastore_ids'):
                        setattr(args, 'datastore_ids', None)
                    args.vcenter_id = args.vcenter_id or questionary.text('Enter vCenter ID:').ask()
                    args.datastore_ids = args.datastore_ids or questionary.text('Enter datastore IDs (comma-separated):').ask()
                    mark_archival_datastore(args)
            except Exception as e:
                display_error(e, 'Operation')
            print(Fore.LIGHTBLACK_EX + '\n' + '='*50 + '\n')
    except Exception as e:
        display_error(e, 'Interactive Mode')
        sys.exit(1)

def list_held_machines(args):
    """Command: List all machines currently on hold."""
    try:
        base_url = get_base_url(args.base_url)
        api_user, api_pass = get_credentials(args.username, args.password)
        print(Fore.WHITE + '\n Fetching list of held machines...')
        headers = create_auth_header(api_user, api_pass)
        resp = requests.get(f"{base_url}/inventory/v3/machines", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # Filter for held machines
        held_machines = [m for m in data if m.get('held_machine') is True]
        if held_machines:
            print(Fore.GREEN + f"\n Found {len(held_machines)} held machine(s):")
            for idx, machine in enumerate(held_machines, 1):
                print(Fore.CYAN + f"\n{idx}. Machine Details:")
                print(json.dumps(machine, indent=2))
        else:
            print(Fore.GREEN + '\n No machines are currently on forensic hold.')
    except Exception as e:
        display_error(e, 'List Held Machines')
        sys.exit(1)

def mark_archival_datastore(args):
    """Command: Mark one or more datastores for archival for a given vCenter."""
    try:
        base_url = get_base_url(args.base_url)
        api_user, api_pass = get_credentials(args.username, args.password)
        vcenter_id = args.vcenter_id or questionary.text('Enter vCenter ID:').ask()
        # Prompt for one or more datastore IDs (comma-separated)
        ds_input = args.datastore_ids or questionary.text('Enter datastore IDs (comma-separated):').ask()
        datastore_ids = [ds.strip() for ds in ds_input.split(',') if ds.strip()]
        if not datastore_ids:
            print(Fore.RED + 'No datastore IDs provided. Exiting.')
            sys.exit(1)
        print(Fore.WHITE + f'\n Marking datastores {datastore_ids} for archival on vCenter {vcenter_id}...')
        headers = create_auth_header(api_user, api_pass)
        payload = {"datastoreIds": datastore_ids}
        url = f"{base_url}/config/v1/virtual-center/{vcenter_id}/action/mark-datastores-for-archival"
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        display_result(resp.json(), 'Mark Archival Datastore')
    except Exception as e:
        display_error(e, 'Mark Archival Datastore')
        sys.exit(1)

def main():
    """Main entry point: parse arguments and dispatch commands."""
    parser = argparse.ArgumentParser(description='Horizon Forensics CLI Tool')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # hold-user
    hold_parser = subparsers.add_parser('hold-user', help='Put an Active Directory user on forensic hold')
    hold_parser.add_argument('userSid', nargs='?', help='User Security Identifier (SID)')
    hold_parser.add_argument('-u', '--username', help='Horizon API Username')
    hold_parser.add_argument('-p', '--password', help='Horizon API Password')
    hold_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    hold_parser.set_defaults(func=hold_user)

    # archive-vm
    archive_parser = subparsers.add_parser('archive-vm', help='Archive a virtual machine by VM ID')
    archive_parser.add_argument('vmId', nargs='?', help='Virtual Machine ID')
    archive_parser.add_argument('-u', '--username', help='Horizon API Username')
    archive_parser.add_argument('-p', '--password', help='Horizon API Password')
    archive_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    archive_parser.set_defaults(func=archive_vm)

    # release-hold
    release_parser = subparsers.add_parser('release-hold', help='Release a user from forensic hold')
    release_parser.add_argument('userSid', nargs='?', help='User Security Identifier (SID)')
    release_parser.add_argument('-u', '--username', help='Horizon API Username')
    release_parser.add_argument('-p', '--password', help='Horizon API Password')
    release_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    release_parser.set_defaults(func=release_hold)

    # list-held-users
    list_parser = subparsers.add_parser('list-held-users', help='List all currently held users')
    list_parser.add_argument('-u', '--username', help='Horizon API Username')
    list_parser.add_argument('-p', '--password', help='Horizon API Password')
    list_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    list_parser.set_defaults(func=list_held_users)

    # interactive
    interactive_parser = subparsers.add_parser('interactive', help='Run in interactive mode with menu options')
    interactive_parser.add_argument('-u', '--username', help='Horizon API Username')
    interactive_parser.add_argument('-p', '--password', help='Horizon API Password')
    interactive_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    interactive_parser.set_defaults(func=interactive_menu)

    # list-held-machines
    machines_parser = subparsers.add_parser('list-held-machines', help='List all machines currently on forensic hold')
    machines_parser.add_argument('-u', '--username', help='Horizon API Username')
    machines_parser.add_argument('-p', '--password', help='Horizon API Password')
    machines_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    machines_parser.set_defaults(func=list_held_machines)

    # mark-archival-datastore
    mark_parser = subparsers.add_parser('mark-archival-datastore', help='Mark one or more datastores for archival for a given vCenter')
    mark_parser.add_argument('-u', '--username', help='Horizon API Username')
    mark_parser.add_argument('-p', '--password', help='Horizon API Password')
    mark_parser.add_argument('-b', '--base-url', help='Horizon API Base URL')
    mark_parser.add_argument('--vcenter-id', help='vCenter ID')
    mark_parser.add_argument('--datastore-ids', help='Comma-separated list of datastore IDs')
    mark_parser.set_defaults(func=mark_archival_datastore)

    # help
    help_parser = subparsers.add_parser('help', help='Show comprehensive help information')
    help_parser.set_defaults(func=lambda args: display_comprehensive_help())

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main() 