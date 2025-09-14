from analysis.dockerfile_parser import DockerfileParser
from analysis.suggestion_parser import SuggestionParser
from analysis.ai_suggestor import GroqAISuggestor
import os

def main():
    # Check if Dockerfile exists
    if not os.path.exists('Dockerfile'):
        print("❌ Error: Dockerfile not found in current directory")
        print("   Please make sure you're running this from a directory with a Dockerfile")
        return
    
    parser = DockerfileParser('Dockerfile')
    suggestor = GroqAISuggestor()
    
    print("🔍 Analyzing Dockerfile...")
    commands = parser.parse()
    
    print("🤖 Getting AI suggestions from Groq Cloud...")
    result = suggestor.get_suggestions('Dockerfile')
    
    if "error" in result:
        print(f"Error: {result['error']}")
        print("\n💡 Get FREE Groq API Key:")
        print("   1. Go to: https://console.groq.com/keys")
        print("   2. Sign up and create API key")
        print("   3. Set environment variable:")
        print("      $env:GROQ_API_KEY = 'your-key-here'")
        return
    
    print("📊 Parsing suggestions...")
    structured_suggestions = SuggestionParser.parse_ai_response(result['suggestions'])
    SuggestionParser.print_structured_suggestions(structured_suggestions)
    
    print(f"\n🎯 Optimization complete! Source: {result.get('source', 'Groq Cloud')}")

if __name__ == "__main__":
    main()