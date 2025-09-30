import requests
import os
import json
from dotenv import load_dotenv
from .dockerfile_parser import DockerfileParser

# Load environment variables from .env file
load_dotenv()

class GroqAISuggestor:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.demo_mode = False
        
        if not self.api_key:
            print("⚠️  GROQ_API_KEY not found. Running in demo mode with sample suggestions.")
            self.demo_mode = True
            return
        
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def get_suggestions(self, dockerfile_path):
        if self.demo_mode:
            return self._get_demo_suggestions(dockerfile_path)
            
        parser = DockerfileParser(dockerfile_path)
        commands = parser.parse()
        
        if not commands:
            return {"error": "No commands found in Dockerfile"}
        
        commands_text = "\n".join([cmd['original'] for cmd in commands])
        
        prompt = f"""
        You are an expert Docker optimization specialist. Analyze this Dockerfile and provide specific optimization suggestions:

        DOCKERFILE:
        {commands_text}

        Provide recommendations for smaller image size, faster build times, and better security.
        Be specific and provide exact commands.
        """
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": "llama-3.1-8b-instant",  
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 800
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"suggestions": result['choices'][0]['message']['content'], "source": "Groq Cloud"}
            else:
                return {"error": f"Groq API error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def _get_demo_suggestions(self, dockerfile_path):
        """Return sample suggestions for demo purposes"""
        sample_suggestions = """
BASE IMAGE OPTIMIZATION:
- Consider using a smaller base image like alpine or slim variants
- Use multi-stage builds to reduce final image size

LAYER OPTIMIZATION:
- Combine RUN commands to reduce layer count
- Clean up package manager cache in the same layer

DEPENDENCIES:
- Remove unnecessary packages and dependencies
- Use specific version tags instead of 'latest'

SECURITY:
- Run as non-root user when possible
- Regularly update base images for security patches
"""
        return {"suggestions": sample_suggestions, "source": "Demo Mode"}

    def print_suggestions(self, result):
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print("=" * 60)
        if self.demo_mode:
            print("🤖 DEMO SUGGESTIONS (Get API key for real AI analysis)")
        else:
            print(f"🤖 AI SUGGESTIONS FROM: {result.get('source', 'Groq Cloud')}")
        print("=" * 60)
        print(result['suggestions'])
        print("=" * 60)