import re

class DockerfileRewriter:
    def __init__(self, original_path):
        self.original_path = original_path
        
    def read_dockerfile(self):
        with open(self.original_path, 'r') as f:
            return f.readlines()
    
    def apply_optimizations(self, lines, ai_suggestions):
        """Apply common optimization patterns based on AI suggestions"""
        optimized_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                optimized_lines.append(lines[i])
                i += 1
                continue
            
            # Optimize base images
            if line.startswith('FROM'):
                optimized_line = self._optimize_base_image(line, ai_suggestions)
                optimized_lines.append(optimized_line + '\n')
            
            # Combine consecutive RUN commands
            elif line.startswith('RUN'):
                run_lines = [line]
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('RUN'):
                    run_lines.append(lines[j].strip())
                    j += 1
                
                if len(run_lines) > 1:
                    optimized_run = self._combine_run_commands(run_lines)
                    optimized_lines.append(optimized_run + '\n')
                    i = j  # Skip the processed lines
                    continue
                else:
                    optimized_lines.append(lines[i])
            
            # Remove unnecessary files
            elif line.startswith('COPY') or line.startswith('ADD'):
                optimized_line = self._optimize_copy_commands(line)
                optimized_lines.append(optimized_line + '\n')
            
            else:
                optimized_lines.append(lines[i])
            
            i += 1
        
        return optimized_lines
    
    def _optimize_base_image(self, line, ai_suggestions):
        """Replace with lighter base image"""
        # Simple optimization: replace bulky images with slim versions
        replacements = {
            'ubuntu:latest': 'ubuntu:22.04-slim',
            'node:latest': 'node:20-alpine',
            'python:latest': 'python:3.11-slim',
            'openjdk:latest': 'openjdk:17-jre-slim'
        }
        
        for bulky, slim in replacements.items():
            if bulky in line:
                return line.replace(bulky, slim)
        return line
    
    def _combine_run_commands(self, run_lines):
        """Combine multiple RUN commands into one"""
        commands = []
        for run_line in run_lines:
            # Extract the command after 'RUN'
            command = run_line[4:].strip()
            commands.append(command)
        
        # Remove duplicate commands and combine with &&
        unique_commands = []
        for cmd in commands:
            if cmd not in unique_commands:
                unique_commands.append(cmd)
        
        combined = " && ".join(unique_commands)
        return f"RUN {combined}"
    
    def _optimize_copy_commands(self, line):
        """Optimize copy commands"""
        if '.git' in line or 'node_modules' in line:
            # Add .dockerignore recommendation instead of copying
            return line + " # Consider adding to .dockerignore"
        return line
    
    def write_optimized_dockerfile(self, optimized_lines, output_path='Dockerfile.optimized'):
        with open(output_path, 'w') as f:
            f.writelines(optimized_lines)
        return output_path