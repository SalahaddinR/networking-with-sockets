from collections import namedtuple

EXAMPLE_STINGS = [ 
    "type:client:register:name=John|email=john@email.com|pword=343453|",
    "type:client:verify:email=Jay|email=jay@email.com|pword=3534235dfsds|",
    "type:order:register:name=Burger|amount=5|id=3"
]

class find_next_occurence:

    def __init__(self, element: str, string: str):
        self.encounters = 0
        self.element = element
        self.string = string

    def get_next_encounter(self):
        current_encoutners = 0 
        for index, symbol in enumerate(self.string):
            if symbol == self.element:
                current_encoutners += 1
                if current_encoutners > self.encounters:
                    self.encounters += 1
                    return index
        return -1

def _identify_command(command: str, commands: list) -> str | None:
    for cur_command in commands:
        result = command.find(cur_command)
        if result != -1:
            return cur_command
    return -1

def analyze_type(org_command: str):
    result = _identify_command(org_command[org_command.find('type')+1:], ['client', 'order'])
    return (org_command[org_command.find(':')+1:], result)

def client_instruction(org_command: str) -> tuple:
    result = _identify_command(org_command, ['register', 'verify'])
    if result == -1:
        raise TypeError("Command is not <instruction> command")
    elif result == 'register':
        return (org_command[org_command.find(':')+ 1: ], 'register')
    elif result == 'verify':
        return (org_command[org_command.find(':')+ 1: ], 'verify')

def order_instruction(org_command: str) -> tuple:
    result = _identify_command(org_command, ['register'])
    if result == 'register':
        return (org_command[org_command.find(':')+ 1: ], 'register')

def extract_field(string: str, substring: str, end_index: int):
    return string[string.find(substring) + len(substring) + 1: end_index]
    
def client_data_handle(org_command: tuple):
    dividors = find_next_occurence('|', org_command[0])
    if org_command[1] == 'register':
        data_template = namedtuple('RegistrationData', ['name', 'email', 'password'])
        collected_data = {
            'name': extract_field(org_command[0], 'name', dividors.get_next_encounter()),
            'email': extract_field(org_command[0], 'email', dividors.get_next_encounter()),
            'pword': extract_field(org_command[0], 'pword', dividors.get_next_encounter())
        }
        return data_template._make([collected_data['name'], collected_data['email'], collected_data['pword']])
    elif org_command[1] == 'verify':
        data_template = namedtuple('VerificationData', ['email', 'password'])
        collected_data = {
            'email': extract_field(org_command[0], 'email', dividors.get_next_encounter()),
            'pword': extract_field(org_command[0], 'pword', dividors.get_next_encounter())
        }
        return data_template._make([collected_data['email'], collected_data['pword']])
        
def order_data_handle(org_command: tuple):
    dividors = find_next_occurence('|', org_command[0])
    data_template = namedtuple('OrderData', ['name', 'amount', 'client_id'])
    collected_data = {
        'name': extract_field(org_command[0], 'name', dividors.get_next_encounter()),
        'amount': extract_field(org_command[0], 'amount', dividors.get_next_encounter()),
        'client_id':extract_field(org_command[0], 'id', dividors.get_next_encounter())
    }
    return data_template._make([collected_data['name'], collected_data['amount'], collected_data['client_id']])

def dispatch_command(org_command: str):
    org_command, command_type = analyze_type(org_command)
    if command_type == 'client':
        next_step = client_instruction(org_command)
        return client_data_handle(next_step)
    elif command_type == 'order':
        next_step = order_instruction(org_command)
        return order_data_handle(next_step)





