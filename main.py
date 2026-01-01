import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError(
        "API key not found. Ensure API Key is set in the Environment Variables.")


def main():
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")

    args = parser.parse_args()
    # prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages)

    if response.usage_metadata is None:
        raise RuntimeError(
            "API request failed. Check internet connection, and API key.")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
