# Developed by Joshua Jenkins
# RHVD - Horizon Forensics CLI Tool
# TOOL NAME: RHVD REAPER

A command-line interface tool for VMware Horizon forensics operations, including user hold management and VM archiving.

## Features

- User Hold Management: Put Active Directory users on forensic hold and release them
- VM Archiving: Archive virtual machines by VM ID
- User Listing: List all currently held users
- Machine Listing: List all currently held machines
- Mark Archival Datastore: Designate datastores for archival for a given vCenter
- Interactive Mode: User-friendly interactive menu interface (with friendly exit on Ctrl+C or Exit)
- Secure Authentication: Basic authentication with Horizon API credentials
- Flexible Configuration: Horizon API base URL can be provided via command line, environment variable, or interactive prompt
- Displays currently logged-in OS user at startup
- Consistent color scheme for CLI output (banner, success, error, etc.)

## User Experience Improvements

- The CLI now displays the currently logged-in OS user at startup.
- The interactive menu can be exited gracefully by selecting 'Exit' or pressing Ctrl+C, with a friendly message.
- All CLI output uses a consistent color scheme:
  - Banner: gray
  - Welcome/program name: cyan
  - Prompts: white (plain, no color codes in questionary)
  - Section headers: cyan
  - Success: green
  - Warning/tip: yellow
  - Error: red
  - General info: white
- The '?' at the start of interactive prompts is normal and indicates the CLI is waiting for input.

## How It Works

### Architecture Overview

The RHVD tool is a command-line interface application written in Python that interacts directly with the VMware Horizon API to perform forensics operations.

### Core Components

#### Configuration Management
The tool supports multiple ways to provide the Horizon API base URL:

1. Command Line Option: `-b, --base-url <url>`
2. Environment Variable: `HORIZON_API_BASE` in `.env` file
3. Interactive Prompt: If not provided via other methods

#### Authentication System
The tool uses Basic Authentication with Base64 encoding to authenticate with the Horizon API. Credentials are:
- Prompted interactively if not provided via command line (prompts are plain white text)
- Stored only in memory during the session
- Never logged or persisted

#### API Endpoints

The tool interacts with these VMware Horizon API endpoints:

| Operation | Endpoint | Method | Purpose |
|-----------|----------|--------|---------|
| User Hold | `/external/v1/ad-users-or-groups/action/hold` | POST | Put AD user on forensic hold |
| User Release | `/external/v1/ad-users-or-groups/action/release-hold` | POST | Release user from forensic hold |
| VM Archive | `/inventory/v1/machines/action/archive` | POST | Archive virtual machine |
| List Held Users | `/external/v1/ad-users-or-groups/held-users-or-groups` | GET | Retrieve list of held users |
| List Held Machines | `/inventory/v3/machines` | GET | Retrieve all machines (filter for held) |
| Mark Archival Datastore | `/config/v1/virtual-center/{id}/action/mark-datastores-for-archival` | POST | Designate datastores for archival |

#### Request/Response Format

**User Hold Request:**
```json
{
  "securityIdentifiers": ["S-1-5-21-1234567890-1234567890-1234567890-1234"]
}
```

**VM Archive Request:**
```json
{
  "ids": ["vm-12345"]
}
```

**Response Format:**
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": { ... }
}
```

### CLI Implementation Details

#### Command Structure
The CLI uses Python's `argparse` library to create a structured command interface. Each command is implemented as a subparser:

- `archive-vm [vmId]`: Archive a virtual machine by VM ID
- `hold-user [userSid]`: Put an Active Directory user on forensic hold
- `list-held-users`: List all currently held users
- `list-held-machines`: List all currently held machines
- `release-hold [userSid]`: Release a user from forensic hold
- `mark-archival-datastore`: Mark one or more datastores for archival for a given vCenter
- `interactive`: Run in interactive mode with menu options
- `help`: Show comprehensive help information

#### Interactive Prompts
Uses the `questionary` library for user-friendly prompts. Prompts are plain white text (no color codes). The interactive menu order is:

1. Archive VM
2. Put User on Hold
3. List Held Users
4. List Held Machines
5. Release User from Hold
6. Mark Archival Datastore
7. Help
8. Exit

You can exit the interactive session at any time by selecting 'Exit' or pressing Ctrl+C.

#### Error Handling
Comprehensive error handling with user-friendly messages. Errors are displayed in the terminal with clear descriptions and in red font.

### Data Flow

#### CLI Operation Flow
1. Command Parsing: Parse command line arguments and options
2. Base URL Resolution: Get base URL from command line, environment, or prompt
3. Input Validation: Validate required parameters
4. Credential Collection: Prompt for credentials if not provided
5. API Request: Make authenticated request to Horizon API
6. Response Processing: Handle success/error responses
7. Output Display: Format and display results to user

### Error Handling Strategy

- Network Errors: Connection timeout handling, clear error messages for network issues
- API Errors: HTTP status code interpretation, error message extraction from API responses
- Validation Errors: Input format validation, required field checking, SID format validation, URL format validation

### Performance Considerations

- Minimal memory footprint
- Fast startup time
- Efficient command parsing

### Extensibility

The modular design allows for easy extension:

1. Add command definition to CLI
2. Implement command action function
3. Update documentation

## Installation

1. Clone or download this repository
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Create a `.env` file in the backend directory with your Horizon API configuration:
   ```
   HORIZON_API_BASE=https://your-horizon-server.com
   ```

## Usage

### Interactive Mode (Recommended for beginners)

Run the CLI in interactive mode for a guided experience:

```bash
python cli.py interactive
```

- The CLI will display the currently logged-in OS user at startup.
- The interactive menu order is:
  1. Archive VM
  2. Put User on Hold
  3. List Held Users
  4. List Held Machines
  5. Release User from Hold
  6. Mark Archival Datastore
  7. Help
  8. Exit
- You can exit the interactive session at any time by selecting 'Exit' or pressing Ctrl+C (a friendly message will be shown).
- The '?' at the start of prompts is normal and indicates the CLI is waiting for input.

### Command Line Mode

#### Archive Virtual Machine
```bash
# Interactive prompts for base URL, VM ID, and credentials
python cli.py archive-vm

# With VM ID provided (default port 443)
python cli.py archive-vm vm-12345

# With custom port and credentials
python cli.py archive-vm vm-12345 -b https://horizon-server.com:9443 -u username -p password
```

#### Put User on Hold
```bash
# Interactive prompts for base URL, user SID, and credentials
python cli.py hold-user

# With user SID provided (default port 443)
python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234

# With custom port and credentials
python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234 -b https://horizon-server.com:8443 -u username -p password
```

#### List Held Users
```bash
# Interactive prompts for base URL and credentials
python cli.py list-held-users

# With custom port and credentials
python cli.py list-held-users -b https://horizon-server.com:9443 -u username -p password
```

#### List Held Machines
```bash
# Interactive prompts for base URL and credentials
python cli.py list-held-machines

# With custom port and credentials
python cli.py list-held-machines -b https://horizon-server.com:9443 -u username -p password
```

#### Release User from Hold
```bash
# Interactive prompts for base URL, user SID, and credentials
python cli.py release-hold

# With user SID provided (default port 443)
python cli.py release-hold S-1-5-21-1234567890-1234567890-1234567890-1234

# With custom port and credentials
python cli.py release-hold S-1-5-21-1234567890-1234567890-1234567890-1234 -b https://horizon-server.com:8443 -u username -p password
```

#### Mark Archival Datastore
```bash
# Interactive prompts for base URL, vCenter ID, datastore IDs, username, and password
python cli.py mark-archival-datastore

# With vCenter ID and datastore IDs provided
python cli.py mark-archival-datastore --vcenter-id vcenter-123 --datastore-ids ds-001,ds-002
```

### Command Options

All commands support the following options:
- `-u, --username <username>`: Horizon API Username
- `-p, --password <password>`: Horizon API Password
- `-b, --base-url <url>`: Horizon API Base URL

If credentials or base URL are not provided via command line options, the CLI will prompt for them interactively.

### Help

Get help for any command:
```bash
python cli.py --help
python cli.py help
python cli.py hold-user --help
python cli.py archive-vm --help
python cli.py release-hold --help
python cli.py list-held-users --help
python cli.py list-held-machines --help
python cli.py mark-archival-datastore --help
python cli.py interactive --help
```

The `help` command provides comprehensive information including:
- Available commands and their descriptions
- Command options and usage
- Horizon API Base URL configuration and port information
- Usage examples for different scenarios
- Security notes and error handling information

## Examples

### Example 1: Interactive Mode
```bash
$ python cli.py interactive

Horizon API Base URL Guidelines:
• Default HTTPS (port 443): https://horizon-server.com
• Custom HTTPS port: https://horizon-server.com:8443
• HTTP (not recommended): http://horizon-server.com:8080
• Common VMware Horizon ports: 443, 8443, 9443
Tip: Start without a port, add :8443 or :9443 if connection fails

Enter Horizon API Base URL (e.g., https://horizon-server.com or https://horizon-server.com:8443): https://horizon.company.com
Enter Horizon API Username: admin
Enter Horizon API Password: ********
Credentials set successfully!

What would you like to do? (Use arrow keys)
> Archive VM
  Put User on Hold
  List Held Users
  List Held Machines
  Release User from Hold
  Mark Archival Datastore
  Help
  Exit
```

**Note**: The interactive mode includes a "Help" option that displays comprehensive help information including port configuration, usage examples, and troubleshooting tips. The '?' at the start of prompts is normal and indicates the CLI is waiting for input.

### Example 2: Direct Command with Base URL
```bash
$ python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234 -b https://horizon.company.com
Enter Horizon API Username: admin
Enter Horizon API Password: ********

Putting user S-1-5-21-1234567890-1234567890-1234567890-1234 on forensic hold...

User Hold completed successfully!
Response:
{
  "status": "success",
  "message": "User placed on forensic hold"
}
```

### Example 3: Using Environment Variable
```bash
# Set environment variable
export HORIZON_API_BASE=https://horizon.company.com

# Run command (no base URL prompt needed)
$ python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234
Enter Horizon API Username: admin
Enter Horizon API Password: ********
```

### Example 4: Using Custom Port
```bash
$ python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234 -b https://horizon.company.com:8443
Enter Horizon API Username: admin
Enter Horizon API Password: ********

Putting user S-1-5-21-1234567890-1234567890-1234567890-1234 on forensic hold...

User Hold completed successfully!
Response:
{
  "status": "success",
  "message": "User placed on forensic hold"
}
```

### Example 5: Getting Comprehensive Help
```bash
$ python cli.py help

RHVD - Horizon Forensics CLI Tool
A command-line interface tool for VMware Horizon forensics operations

Available Commands:
  hold-user [userSid]     Put an Active Directory user on forensic hold
  archive-vm [vmId]       Archive a virtual machine by VM ID
  release-hold [userSid]  Release a user from forensic hold
  list-held-users         List all currently held users
  list-held-machines      List all machines currently on forensic hold
  mark-archival-datastore Mark one or more datastores for archival for a given vCenter
  interactive             Run in interactive mode with menu options
  help                    Show this comprehensive help information

Command Options:
  -u, --username <username>  Horizon API Username
  -p, --password <password>  Horizon API Password
  -b, --base-url <url>       Horizon API Base URL
  -h, --help                 Show command-specific help

Horizon API Base URL Configuration:
The Horizon API Base URL may require a specific port depending on your VMware Horizon server configuration.

Default HTTPS (Port 443):
  If your Horizon server uses the default HTTPS port, you typically don't need to specify the port:
  https://horizon.company.com

Custom HTTPS Port:
  If your Horizon server uses a custom HTTPS port, you must specify it:
  https://horizon.company.com:8443
  https://horizon.company.com:9443

Common VMware Horizon Ports:
  | Service                    | Default Port | Protocol |
  |----------------------------|--------------|----------|
  | Horizon Connection Server | 443          | HTTPS    |
  | Horizon Connection Server | 8443, 9443   | HTTPS    |
  | Horizon UAG               | 443          | HTTPS    |
  | Horizon UAG (custom)      | 8443, 9443   | HTTPS    |

Port Usage Tips:
  1. Start without a port (e.g., https://horizon.company.com)
  2. If you get connection errors, try adding common ports like :8443 or :9443
  3. Check with your VMware administrator for the correct port configuration
  4. Use HTTPS whenever possible for security

Usage Examples:
Interactive Mode (Recommended for beginners):
  python cli.py interactive

Command Line Mode:
  # Interactive prompts for base URL, user SID, and credentials
  python cli.py hold-user

  # With user SID provided (default port 443)
  python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234

  # With custom port and credentials
  python cli.py hold-user S-1-5-21-1234567890-1234567890-1234567890-1234 -b https://horizon-server.com:8443 -u username -p password

Environment Variables:
  Create a .env file in the backend directory (optional):
  HORIZON_API_BASE=https://your-horizon-server.com

Security Notes:
  - Credentials are only stored in memory during the session
  - Passwords are hidden when entered interactively
  - Base URL is validated for proper format
  - Consider using environment variables for credentials in production
  - The .env file should not be committed to version control

Error Handling:
  The CLI provides clear error messages for:
  - Missing credentials
  - Invalid API responses
  - Network connectivity issues
  - Invalid user SIDs or VM IDs
  - Invalid base URL format

Getting Help:
  python cli.py --help                    # Show general help
  python cli.py help                      # Show this comprehensive help
  python cli.py hold-user --help          # Show command-specific help
  python cli.py archive-vm --help         # Show command-specific help
  python cli.py release-hold --help       # Show command-specific help
  python cli.py list-held-users --help    # Show command-specific help
  python cli.py list-held-machines --help # Show command-specific help
  python cli.py mark-archival-datastore --help # Show command-specific help
  python cli.py interactive --help        # Show command-specific help

For more information, visit the project documentation or contact your VMware administrator.

## Environment Variables

Create a `.env` file in the backend directory (optional):

```
HORIZON_API_BASE=https://your-horizon-server.com
```

## Port Configuration

The Horizon API Base URL may require a specific port depending on your VMware Horizon server configuration:

### Default HTTPS (Port 443)
If your Horizon server uses the default HTTPS port, you typically don't need to specify the port:
```bash
https://horizon.company.com
```

### Custom HTTPS Port
If your Horizon server uses a custom HTTPS port, you must specify it:
```bash
https://horizon.company.com:8443
https://horizon.company.com:9443
```

### Common VMware Horizon Ports
| Service | Default Port | Protocol |
|---------|-------------|----------|
| Horizon Connection Server | 443 | HTTPS |
| Horizon Connection Server (custom) | 8443, 9443 | HTTPS |
| Horizon UAG (Unified Access Gateway) | 443 | HTTPS |
| Horizon UAG (custom) | 8443, 9443 | HTTPS |

### Port Usage Tips
1. Start without a port (e.g., `https://horizon.company.com`)
2. If you get connection errors, try adding common ports like `:8443` or `:9443`
3. Check with your VMware administrator for the correct port configuration
4. Use HTTPS whenever possible for security

The CLI will display helpful port guidance when prompting for the base URL.

## Security Notes

- Credentials are only stored in memory during the session
- Passwords are hidden when entered interactively
- Base URL is validated for proper format
- Consider using environment variables for credentials in production environments
- The `.env` file should not be committed to version control

## Error Handling

The CLI provides clear error messages for:
- Missing credentials
- Invalid API responses
- Network connectivity issues
- Invalid user SIDs or VM IDs
- Invalid base URL format

## Development

To run the CLI:
```bash
python cli.py <command>
```

## Dependencies

- `argparse`: Command-line argument parsing (Python standard library)
- `requests`: HTTP client for API requests
- `colorama`: Terminal color output
- `questionary`: Interactive prompts for CLI
- `python-dotenv`: Environment variable management

### Mark Archival Datastore

Mark one or more datastores for archival for a given vCenter. This is required for Horizon to know where to store archived VM data.

#### Usage
```bash
python cli.py mark-archival-datastore --vcenter-id <VCENTER_ID> --datastore-ids <DS_ID1>,<DS_ID2> -u <username> -p <password> -b <base_url>
```
If you omit the vCenter ID or datastore IDs, the CLI will prompt you interactively.

#### Example
```bash
python cli.py mark-archival-datastore --vcenter-id vcenter-123 --datastore-ids ds-001,ds-002
```

This will mark the datastores `ds-001` and `ds-002` for archival on the vCenter with ID `vcenter-123`.

