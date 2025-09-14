import re

class DockerfileParser:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        self.commands = []

    def parse(self):
        """Reads a Dockerfile and extracts its commands into a list of dictionaries."""
        try:
            with open(self.dockerfile_path, 'r') as f:
                content = f.read()
            
            # Handle multi-line commands by joining lines ending with \
            content = re.sub(r'\\\s*\n', ' ', content)
            
            lines = content.split('\n')
            current_command = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # Skip empty lines and comments
                
                # Check if this line continues a previous command
                if current_command and not re.match(r'^\w+', line):
                    current_command['original'] += ' ' + line
                    current_command['arguments'] += ' ' + line
                    continue
                
                # Match the instruction (like FROM, RUN, COPY) and its arguments
                match = re.match(r'^(\w+)\s+(.*)$', line)
                if match:
                    instruction = match.group(1)
                    args = match.group(2)
                    
                    current_command = {
                        'instruction': instruction,
                        'arguments': args,
                        'original': line
                    }
                    self.commands.append(current_command)
            
            return self.commands

        except FileNotFoundError:
            print(f"Error: The file {self.dockerfile_path} was not found.")
            return []