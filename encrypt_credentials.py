"""
Helper script to encrypt credentials for use in .env file
Run this once to encrypt your sensitive data
"""
import sys
from utils.encryption import encrypt_credential


def main():
    """Interactive credential encryption tool"""
    print("\n" + "="*60)
    print("🔐 Credential Encryption Tool")
    print("="*60)
    print("\nThis tool will encrypt your credentials for the .env file.")
    print("The encryption key will be saved to '.encryption.key'")
    print("Keep that file safe!\n")

    credentials = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "LINKEDIN_EMAIL": "LinkedIn Email",
        "LINKEDIN_PASSWORD": "LinkedIn Password",
    }

    encrypted_creds = {}

    for env_var, display_name in credentials.items():
        while True:
            value = input(f"Enter {display_name}: ").strip()
            if not value:
                print("❌ Value cannot be empty. Please try again.")
                continue
            
            confirm = input(f"Confirm {display_name} (yes/no): ").strip().lower()
            if confirm == "yes":
                encrypted_creds[env_var] = encrypt_credential(value)
                print(f"✅ {display_name} encrypted successfully\n")
                break
            else:
                print("❌ Cancelled. Please re-enter.\n")

    # Display the .env format
    print("\n" + "="*60)
    print("📋 Add these lines to your .env file:")
    print("="*60 + "\n")

    for env_var, encrypted_value in encrypted_creds.items():
        print(f"{env_var}=encrypted:{encrypted_value}")

    print("\n" + "="*60)
    print("⚠️  IMPORTANT:")
    print("="*60)
    print("1. Copy the above lines into your .env file")
    print("2. Keep the '.encryption.key' file safe and private")
    print("3. Don't commit '.encryption.key' to version control")
    print("4. The agent will automatically decrypt credentials when running\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user.")
        sys.exit(0)
