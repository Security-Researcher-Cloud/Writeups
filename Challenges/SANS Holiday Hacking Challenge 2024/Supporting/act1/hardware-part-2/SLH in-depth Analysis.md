## Extraction
![](../../../Assets/images/act1/hardware-part-2/Pasted%20image%2020241126224556.png)
## Identification
![](../../../Assets/images/act1/hardware-part-2/Pasted%20image%2020241126224703.png)
![](../../../Assets/images/act1/hardware-part-2/Pasted%20image%2020241126224902.png)
## Source Code
```python
import argparse
import sqlite3
import uuid
import hashlib
import hmac
import os
import requests
PASSCODE = os.getenv('SLH_PASSCODE', 'CandyCaneCrunch77')
secret_key = b'873ac9ffea4dd04fa719e8920cd6938f0c23cd678af330939cff53c3d2855f34'
expected_signature = 'e96c7dc0f25ebcbc45c9c077d4dc44adb6e4c9cb25d3cc8f88557d9b40e7dbaf'
completeArt = '\n       *   *   *   *   *   *   *   *   *   *   *\n   *                                             *\n*      ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄     *\n *  $$$$$$\\   $$$$$$\\   $$$$$$\\  $$$$$$$$\\  $$$$$$\\   $$$$$$\\  * \n  * $$  __$$\\ $$  __$$\\ $$  __$$\\ $$  _____|$$  __$$\\ $$  __$$\\ *\n   *$$ /  $$ |$$ /  \\__|$$ /  \\__|$$ |      $$ /  \\__|$$ /  \\__| *\n    $$$$$$$$ |$$ |      $$ |      $$$$$\\    \\$$$$$$\\  \\$$$$$$\\   \n   *$$  __$$ |$$ |      $$ |      $$  __|    \\____$$\\  \\____$$\\  *\n  * $$ |  $$ |$$ |  $$\\ $$ |  $$\\ $$ |      $$\\   $$ |$$\\   $$ | *\n*   $$ |  $$ |\\$$$$$$  |\\$$$$$$  |$$$$$$$$\\ \\$$$$$$  |\\$$$$$$  |   *\n *  \\__|  \\__| \\______/  \\______/ \\________| \\______/  \\______/  *\n*         *    ❄             ❄           *        ❄    ❄    ❄   *\n   *        *     *     *      *     *      *    *      *      *\n   *  $$$$$$\\  $$$$$$$\\   $$$$$$\\  $$\\   $$\\ $$$$$$$$\\ $$$$$$$$\\ $$$$$$$\\  $$\\  *\n   * $$  __$$\\ $$  __$$\\ $$  __$$\\ $$$\\  $$ |\\__$$  __|$$  _____|$$  __$$\\ $$ | *\n  *  $$ /  \\__|$$ |  $$ |$$ /  $$ |$$$$\\ $$ |   $$ |   $$ |      $$ |  $$ |$$ |*\n  *  $$ |$$$$\\ $$$$$$$  |$$$$$$$$ |$$ $$\\$$ |   $$ |   $$$$$\\    $$ |  $$ |$$ | *\n *   $$ |\\_$$ |$$  __$$< $$  __$$ |$$ \\$$$$ |   $$ |   $$  __|   $$ |  $$ |\\__|*\n  *  $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\\$$$ |   $$ |   $$ |      $$ |  $$ |   *\n*    \\$$$$$$  |$$ |  $$ |$$ |  $$ |$$ | \\$$ |   $$ |   $$$$$$$$\\ $$$$$$$  |$$\\ *\n *    \\______/ \\__|  \\__|\\__|  \\__|\\__|  \\__|   \\__|   \\________|\\_______/ \\__|  *\n  *                                                            ❄    ❄    ❄   *\n   *      *    *    *    *    *    *    *    *    *    *    *    *    *    *                                                                                                                                        \n'

class GameCLI:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Santa's Little Helper - Access Card Maintenance Tool")
        self.setup_arguments()
        self.db_file = 'access_cards'
        self.api_endpoint = os.getenv('API_ENDPOINT', '')
        self.api_port = os.getenv('API_PORT', '')
        self.resource_id = os.getenv('RESOURCE_ID', '')
        self.challenge_hash = os.getenv('CHALLENGE_HASH', '').encode('utf8')

    def setup_arguments(self):

        def access_level(value):
            ivalue = int(value)
            if ivalue not in [0, 1]:
                raise argparse.ArgumentTypeError(f'Invalid access level: {value}0. Must be 0 (No Access) or 1 (Full Access).')
            return ivalue
        arg_group = self.parser.add_mutually_exclusive_group()
        arg_group.add_argument('--view-config', action='store_true', help='View current configuration.')
        arg_group.add_argument('--view-cards', action='store_true', help='View current values of all access cards.')
        arg_group.add_argument('--view-card', type=int, metavar='ID', help='View a single access card by ID.')
        arg_group.add_argument('--set-access', type=access_level, metavar='ACCESS_LEVEL', help='Set access level of access card. Must be 0 (No Access) or 1 (Full Access).')
        self.parser.add_argument('--id', type=int, metavar='ID', help='ID of card to modify.')
        self.parser.add_argument('--passcode', type=str, metavar='PASSCODE', help='Passcode to make changes.')
        arg_group.add_argument('--new-card', action='store_true', help='Generate a new card ID.')

    def run(self):
        self.args = self.parser.parse_args()
        if self.args.view_config:
            self.view_config()
        elif self.args.view_cards:
            self.view_access_cards()
        elif self.args.view_card is not None:
            self.view_single_card(self.args.view_card)
        elif self.args.set_access is not None:
            self.set_access(self.args.set_access, self.args.id)
        elif self.args.new_card:
            self.new_card()
        else:
            print('No valid command provided. Use --help for usage information.')

    def view_config(self):
        print('Error loading config table from access_cards database.')

    def view_access_cards(self):
        print('Current values of access cards: (id, uuid, access, signature)')
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('\n            SELECT * FROM access_cards\n        ')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()

    def view_single_card(self, card_id):
        print(f'Details of card with ID: {card_id}0')
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('\n            SELECT * FROM access_cards WHERE id = ?\n        ', (card_id,))
        row = cursor.fetchone()
        conn.close()
        if card_id == 42:
            self.check_signature()
        if row:
            print(row)
        else:
            print(f'No card found with ID: {card_id}0')

    def set_access(self, access, id):
        if self.args.passcode == PASSCODE:
            if self.args.id is not None:
                card_data = self.get_card_data(id)
                sig = self.generate_signature(access=access, uuid=card_data['uuid'])
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute('\n                    UPDATE access_cards SET access = ?, sig = ? WHERE id = ?\n                ', (access, sig, id))
                conn.commit()
                conn.close()
                if self.args.id == 42:
                    self.check_signature()
                print(f'Card {id} granted access level {access}.')
            else:
                print('No card ID provided. Access not granted.')
        else:
            print('Invalid passcode. Access not granted.')

    def debug_mode(self):
        if self.args.passcode == PASSCODE:
            if self.args.id is not None:
                card_data = self.get_card_data(self.args.id)
                sig = self.generate_signature(tokens=card_data['access'], uuid=card_data['uuid'])
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute('UPDATE access_cards SET sig = ? WHERE id = ?', (sig, self.args.id))
                conn.commit()
                conn.close()
                print(f'Setting {self.args.id} to debug mode.')
                print(self.get_card_data(self.args.id))
            else:
                print('No card ID provided. Debug mode not enabled.')
        else:
            print('Invalid passcode. Debug mode not enabled.')

    def get_card_data(self, card_id):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT uuid, access, sig FROM access_cards WHERE id = ?', (card_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {'uuid': row[0], 'access': row[1], 'sig': row[2]}
            print(f'No card found with ID: {card_id}0')
        except sqlite3.Error as e:
            print(f'Database error: {e}0')

    def new_card(self):
        id = str(uuid.uuid4())
        print(f'Generate new card with uuid: {id}0')

    def generate_signature(self, access=None, uuid=None):
        data = f'{access}{uuid}'
        signature = hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()
        return signature

    def check_signature(self):
        card_data = self.get_card_data(42)
        if card_data and card_data['sig'] == expected_signature:
            self.send_hhc_success_message(self.api_endpoint, self.api_port, self.resource_id, self.challenge_hash, 'easy')
            return print(completeArt)
        return False

    def send_hhc_success_message(self, api_endpoint, api_port, resource_id, challenge_hash, action):
        url = f'{api_endpoint}:{api_port}/turnstile'
        message = f'{resource_id}:{action}0'
        h = hmac.new(challenge_hash, message.encode(), hashlib.sha256)
        hash_value = h.hexdigest()
        data = {'rid': resource_id, 'hash': hash_value, 'action': action}
        querystring = {'rid': resource_id}
        try:
            response = requests.post(url, params=querystring, json=data, timeout=5)
            response_data = response.json()
            if response_data.get('result') != 'success':
                print('There was an issue communicating with the server. Please reach out to one of the concierges for assistance.')
        except Exception as e:
            print('Error: There was an issue communicating with the server. Please reach out to one of the concierges for assistance.')
if __name__ == '__main__':
    game_cli = GameCLI()
    game_cli.run()
```

## Hard Way To Silver/Gold (Vulnerabilities)

### HMAC Signature Manipulation:
```python
def generate_signature(self, access=None, uuid=None):    
	data = f'{access}{uuid}'    
	signature = hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()
```
- The secret_key is exposed in the code: `b'873ac9ffea4dd04fa719e8920cd6938f0c23cd678af330939cff53c3d2855f34'`
- The expected_signature is known: `'e96c7dc0f25ebcbc45c9c077d4dc44adb6e4c9cb25d3cc8f88557d9b40e7dbaf'`
- Win condition checks card 42's signature against expected_signature

### Known Values:
```python
PASSCODE = os.getenv('SLH_PASSCODE', 'CandyCaneCrunch77')
```
- Default passcode is exposed in code
- Required for making changes to cards

### Critical Path to Victory:
```python
def check_signature(self):     
	card_data = self.get_card_data(42)    
	if card_data and card_data['sig'] == expected_signature:
		self.send_hhc_success_message(...)        
		return print(completeArt)
```

Attack Strategy:
1. Get card 42's data: `./slh --view-card 42`
2. Using the access level and UUID from card 42:
	- Generate the correct signature using `generate_signature()` with the exposed secret_key
	- Use `--set-access` to modify card 42 with the right access level to produce expected signature
3. Change card 42's access:
	- `./slh --set-access 1 --id 42 --passcode CandyCaneCrunch77`

The signature is generated by concatenating `access` and `uuid` values, so by manipulating the access level and knowing the UUID, you can generate a signature that matches the expected one. (GOLD Solve)
These vulnerabilities allow us to:
1. View all card data
2. Calculate required signatures
3. Modify card access levels
4. Achieve the win condition by matching signatures
The key weakness is exposing both the secret key and the signature generation algorithm in the decompiled code.