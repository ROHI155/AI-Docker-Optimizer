import re

class SuggestionParser:
    @staticmethod
    def parse_ai_response(ai_text):
        """
        Parses the AI's text response into structured categories.
        """
        sections = {
            'base_image': [],
            'layer_optimization': [],
            'dependencies': [],
            'security': [],
            'general': []
        }
        
        # Simple parsing logic - you can enhance this later
        current_section = 'general'
        
        for line in ai_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if 'BASE IMAGE' in line.upper():
                current_section = 'base_image'
            elif 'LAYER OPTIMIZATION' in line.upper():
                current_section = 'layer_optimization'
            elif 'DEPENDENCY' in line.upper():
                current_section = 'dependencies'
            elif 'SECURITY' in line.upper():
                current_section = 'security'
            elif line.startswith('-') or line.startswith('*'):
                # This is a bullet point - add to current section
                sections[current_section].append(line)
                
        return sections

    @staticmethod
    def print_structured_suggestions(parsed_suggestions):
        """Pretty print the parsed suggestions."""
        print("🔧 OPTIMIZATION SUGGESTIONS")
        print("=" * 50)
        
        for category, items in parsed_suggestions.items():
            if items:
                print(f"\n{category.upper().replace('_', ' ')}:")
                for item in items:
                    print(f"  • {item}")