"""
Ultra-minimal test - Direct OpenAI API call only
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from cryptography.fernet import Fernet

# Load environment variables
load_dotenv()


def get_decrypted_api_key():
    """Decrypt the OpenAI API key"""
    value = os.getenv("OPENAI_API_KEY")
    if not value:
        raise ValueError("OPENAI_API_KEY not found")
    
    if not value.startswith("encrypted:"):
        return value
    
    # Decrypt manually
    encrypted_value = value[10:]
    key_file = ".encryption.key"
    
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
    else:
        raise ValueError("Encryption key file not found")
    
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_value.encode())
    return decrypted.decode()


def generate_post(topic: str) -> str:
    """Generate a LinkedIn post"""
    api_key = get_decrypted_api_key()
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Write a detailed and engaging LinkedIn post about: {topic}

The post should:
1. Start with a compelling hook
2. Provide 3-5 key insights
3. Include practical advice
4. Be professional yet conversational
5. Include 3-5 relevant hashtags
6. End with a call-to-action or question
7. Be 300-500 words

Return only the post content."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced LinkedIn content strategist.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    
    return response.choices[0].message.content


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🧪 Ultra-Minimal LinkedIn Agent Test")
    print("="*60 + "\n")
    
    topic = input("Enter topic for LinkedIn post: ").strip()
    if not topic:
        print("❌ No topic provided")
        return
    
    print(f"\n⏳ Generating post for: {topic}\n")
    
    try:
        post = generate_post(topic)
        print("="*60)
        print("📝 Generated Post:")
        print("="*60)
        print(post)
        print("="*60)
        print("\n✅ Agent is working correctly!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
