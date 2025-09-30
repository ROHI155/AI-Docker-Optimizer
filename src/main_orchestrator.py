from analysis.dockerfile_parser import DockerfileParser
from analysis.ai_suggestor import GroqAISuggestor
from analysis.suggestion_parser import SuggestionParser
import os

def main():
    # Check if Dockerfile exists
    if not os.path.exists('Dockerfile'):
        print("❌ Error: Dockerfile not found in current directory")
        print("   Please make sure you're running this from a directory with a Dockerfile")
        return
    
    parser = DockerfileParser('Dockerfile')
    
    print("🔍 Analyzing Dockerfile...")
    commands = parser.parse()
    
    # Try to create suggestor, handle missing API key
    try:
        suggestor = GroqAISuggestor()
    except ValueError as e:
        print(f"❌ {e}")
        print("\n💡 Get FREE Groq API Key:")
        print("   1. Go to: https://console.groq.com/keys")
        print("   2. Sign up and create API key")
        print("   3. Set environment variable:")
        print("      PowerShell: $env:GROQ_API_KEY = 'your-key-here'")
        print("      CMD: set GROQ_API_KEY=your-key-here")
        print("   4. Or enter your API key now (will not be saved):")
        
        api_key = input("Enter your Groq API key: ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting.")
            return
            
        suggestor = GroqAISuggestor(api_key=api_key)
    
    print("🤖 Getting AI suggestions from Groq Cloud...")
    result = suggestor.get_suggestions('Dockerfile')
    
    # FIXED: Removed the early return statement
    if "error" in result:
        print(f"Error: {result['error']}")
        return  # This should be the only return on error

    # DEBUG: Show raw AI response
    print("\n📋 RAW AI RESPONSE (for debugging):")
    print("=" * 60)
    print(result['suggestions'])
    print("=" * 60)
    print("📊 Parsing suggestions...")

    structured_suggestions = SuggestionParser.parse_ai_response(result['suggestions'])
    SuggestionParser.print_structured_suggestions(structured_suggestions)
    
    print(f"\n🎯 Optimization complete! Source: {result.get('source', 'Groq Cloud')}")

if __name__ == "__main__":
    main()