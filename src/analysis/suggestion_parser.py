import re

class SuggestionParser:
    @staticmethod
    def parse_ai_response(ai_text):
        """
        Parses the AI's text response into structured categories.
        Handles numbered sections, code blocks, and markdown formatting.
        """
        sections = {
            'base_image': [],
            'layer_optimization': [],
            'dependencies': [],
            'security': [],
            'general': []
        }
        
        # Remove code blocks to avoid parsing them
        text = re.sub(r'```.*?```', '', ai_text, flags=re.DOTALL)
        
        # Define keywords for each category
        keywords = {
            'base_image': ['base image', 'alpine', 'slim', 'from', 'ubuntu', 'python', 'image'],
            'layer_optimization': ['multi-stage', 'layer', 'combine', 'run', 'cache', 'build'],
            'dependencies': ['apt-get', 'install', 'package', 'dependency', 'pip', 'requirements'],
            'security': ['security', 'user', 'root', 'permission', 'vulnerability', 'chown']
        }
        
        lines = text.split('\n')
        current_section = 'general'
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:  # Skip short lines
                continue
            
            # Skip lines that are commands or code
            if line.startswith(('```', '`', '$', 'docker', 'RUN', 'COPY', 'CMD', 'ENTRYPOINT', 'FROM', '//', '#')):
                continue
            
            # Check for section headers (numbered or bullet points)
            if re.match(r'^\d+\.', line) or re.match(r'^[*-]\s+', line):
                lower_line = line.lower()
                # Check for keywords to set current section
                for category, keys in keywords.items():
                    if any(key in lower_line for key in keys):
                        current_section = category
                        break
                # Skip adding the header itself to the suggestions
                continue
            
            # Clean the line from markdown formatting and bullets
            clean_line = re.sub(r'^[\d+\.\s*\-]+\s*', '', line)  # Remove numbering/bullets
            clean_line = re.sub(r'[*_`]', '', clean_line).strip()  # Remove markdown
            
            if not clean_line or len(clean_line) < 10:
                continue
            
            # Categorize based on keywords
            lower_clean = clean_line.lower()
            categorized = False
            for category, keys in keywords.items():
                if any(key in lower_clean for key in keys):
                    sections[category].append(clean_line)
                    categorized = True
                    break
            
            if not categorized:
                sections[current_section].append(clean_line)
                
        return sections

    @staticmethod
    def print_structured_suggestions(parsed_suggestions):
        """Pretty print the parsed suggestions."""
        print("🔧 OPTIMIZATION SUGGESTIONS")
        print("=" * 50)
        
        has_content = False
        for category, items in parsed_suggestions.items():
            if items:
                has_content = True
                print(f"\n{category.upper().replace('_', ' ')}:")
                for item in items:
                    print(f"  • {item}")
        
        if not has_content:
            print("\nNo specific optimization suggestions found.")
            print("The AI may have provided general advice in the raw output.")