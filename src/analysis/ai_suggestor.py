import requests
import os
import json
from .dockerfile_parser import DockerfileParser  # Fixed relative import

class GroqAISuggestor:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Please set environment variable.")
        
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def get_suggestions(self, dockerfile_path):
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

    def print_suggestions(self, result):
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print("=" * 60)
        print(f"🤖 AI SUGGESTIONS FROM: {result.get('source', 'Groq Cloud')}")
        print("=" * 60)
        print(result['suggestions'])
        print("=" * 60)

if __name__ == "__main__":
    suggestor = GroqAISuggestor()
    result = suggestor.get_suggestions('Dockerfile')
    suggestor.print_suggestions(result)