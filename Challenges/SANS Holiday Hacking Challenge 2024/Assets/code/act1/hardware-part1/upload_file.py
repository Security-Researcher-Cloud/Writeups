import urllib.request
import urllib.error
import urllib.parse
import json
import os
import time
import sys
import argparse
from typing import Optional, List, Dict, Union
from dataclasses import dataclass


@dataclass
class Server:
    name: str
    zone: str


class GoFileClient:
    """A client for interacting with the Gofile API."""

    BASE_URL = "https://api.gofile.io"

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the GoFile client.

        Args:
            api_token: Optional API token for authenticated requests
        """
        self.api_token = api_token or os.getenv('GOFILE_TOKEN')
        self._last_server_fetch = 0
        self._cached_servers = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {}
        if self.api_token:
            headers['Authorization'] = f'Bearer {self.api_token}'
        return headers

    def _make_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None,
                      files: Optional[Dict] = None) -> Dict:
        """Make an HTTP request and return JSON response."""
        headers = self._get_headers()

        if files:
            # Handle multipart/form-data for file uploads
            boundary = 'boundary123456789'
            headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'

            body = []
            # Add regular form fields
            if data:
                for key, value in data.items():
                    body.append(f'--{boundary}'.encode())
                    body.append(f'Content-Disposition: form-data; name="{key}"'.encode())
                    body.append(b'')
                    body.append(str(value).encode())

            # Add file data
            for key, filepath in files.items():
                filename = os.path.basename(filepath)
                body.append(f'--{boundary}'.encode())
                body.append(
                    f'Content-Disposition: form-data; name="{key}"; filename="{filename}"'.encode()
                )
                body.append(b'Content-Type: application/octet-stream')
                body.append(b'')
                with open(filepath, 'rb') as f:
                    body.append(f.read())

            body.append(f'--{boundary}--'.encode())
            body.append(b'')
            body = b'\r\n'.join(body)
        else:
            # Handle JSON requests
            if data:
                body = json.dumps(data).encode('utf-8')
                headers['Content-Type'] = 'application/json'
            else:
                body = None

        request = urllib.request.Request(
            url,
            data=body,
            headers=headers,
            method=method
        )

        try:
            with urllib.request.urlopen(request) as response:
                response_data = response.read()
                return json.loads(response_data)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                raise Exception(f"API Error: {error_json}")
            except json.JSONDecodeError:
                raise Exception(f"HTTP Error: {e.code} - {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Connection Error: {str(e)}")

    def get_servers(self, zone: Optional[str] = None) -> List[Server]:
        """Get available servers for upload."""
        current_time = time.time()

        if self._cached_servers and (current_time - self._last_server_fetch) < 10:
            servers = self._cached_servers
        else:
            data = self._make_request(f"{self.BASE_URL}/servers")

            if data['status'] != 'ok':
                raise Exception(f"Failed to get servers: {data}")

            servers = [Server(**server) for server in data['data']['servers']]
            self._cached_servers = servers
            self._last_server_fetch = current_time

        if zone:
            servers = [s for s in servers if s.zone == zone]

        return servers

    def upload_file(
            self,
            file_path: str,
            folder_id: Optional[str] = None,
            server: Optional[Server] = None
    ) -> Dict:
        """Upload a file to Gofile."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not server:
            servers = self.get_servers()
            if not servers:
                raise Exception("No servers available")
            server = servers[0]

        data = {}
        if folder_id:
            data['folderId'] = folder_id

        url = f"https://{server.name}.gofile.io/contents/uploadfile"
        result = self._make_request(
            url,
            method='POST',
            data=data,
            files={'file': file_path}
        )

        if result['status'] != 'ok':
            raise Exception(f"Upload failed: {result}")

        return result['data']

    def create_folder(
            self,
            parent_folder_id: str,
            folder_name: Optional[str] = None
    ) -> Dict:
        """Create a new folder."""
        if not self.api_token:
            raise ValueError("API token required for folder creation")

        data = {'parentFolderId': parent_folder_id}
        if folder_name:
            data['folderName'] = folder_name

        result = self._make_request(
            f"{self.BASE_URL}/contents/createFolder",
            method='POST',
            data=data
        )

        if result['status'] != 'ok':
            raise Exception(f"Folder creation failed: {result}")

        return result['data']

    def update_content(
            self,
            content_id: str,
            attribute: str,
            value: Union[str, bool, int]
    ) -> Dict:
        """Update content attributes."""
        if not self.api_token:
            raise ValueError("API token required for content updates")

        valid_attributes = {"name", "description", "tags", "public", "expiry", "password"}
        if attribute not in valid_attributes:
            raise ValueError(f"Invalid attribute. Must be one of: {valid_attributes}")

        data = {
            'attribute': attribute,
            'attributeValue': str(value)
        }

        result = self._make_request(
            f"{self.BASE_URL}/contents/{content_id}/update",
            method='PUT',
            data=data
        )

        if result['status'] != 'ok':
            raise Exception(f"Update failed: {result}")

        return result['data']

    def delete_contents(self, content_ids: List[str]) -> Dict:
        """Delete multiple contents (files or folders)."""
        if not self.api_token:
            raise ValueError("API token required for content deletion")

        data = {'contentsId': ','.join(content_ids)}

        result = self._make_request(
            f"{self.BASE_URL}/contents",
            method='DELETE',
            data=data
        )

        if result['status'] != 'ok':
            raise Exception(f"Deletion failed: {result}")

        return result['data']


def main():
    parser = argparse.ArgumentParser(description='Gofile API Client')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload a file')
    upload_parser.add_argument('file', help='File to upload')
    upload_parser.add_argument('--folder', help='Folder ID to upload to')
    upload_parser.add_argument('--zone', choices=['eu', 'na'], help='Preferred server zone')

    # Create folder command
    folder_parser = subparsers.add_parser('create-folder', help='Create a new folder')
    folder_parser.add_argument('parent', help='Parent folder ID')
    folder_parser.add_argument('--name', help='Folder name')

    # Update content command
    update_parser = subparsers.add_parser('update', help='Update content attributes')
    update_parser.add_argument('content_id', help='Content ID to update')
    update_parser.add_argument('attribute',
                               choices=['name', 'description', 'tags', 'public', 'expiry', 'password'],
                               help='Attribute to modify')
    update_parser.add_argument('value', help='New value for the attribute')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete contents')
    delete_parser.add_argument('content_ids', nargs='+', help='Content IDs to delete')

    # Server list command
    server_parser = subparsers.add_parser('servers', help='List available servers')
    server_parser.add_argument('--zone', choices=['eu', 'na'], help='Filter by zone')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    client = GoFileClient()

    try:
        if args.command == 'upload':
            server = None
            if args.zone:
                servers = client.get_servers(zone=args.zone)
                if servers:
                    server = servers[0]

            result = client.upload_file(args.file, folder_id=args.folder, server=server)
            print(f"File uploaded successfully!")
            print(f"Download page: {result['downloadPage']}")
            print(f"File ID: {result['fileId']}")

        elif args.command == 'create-folder':
            result = client.create_folder(args.parent, args.name)
            print(f"Folder created successfully!")
            print(f"Folder ID: {result['folderId']}")
            print(f"Folder code: {result['code']}")

        elif args.command == 'update':
            result = client.update_content(args.content_id, args.attribute, args.value)
            print("Content updated successfully!")

        elif args.command == 'delete':
            result = client.delete_contents(args.content_ids)
            print("Contents deleted successfully!")

        elif args.command == 'servers':
            servers = client.get_servers(zone=args.zone)
            print("\nAvailable servers:")
            for server in servers:
                print(f"- {server.name} (Zone: {server.zone})")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()