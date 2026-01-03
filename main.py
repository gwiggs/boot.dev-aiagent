import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.call_function import available_functions, call_function

from prompts import system_prompt

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
    function_responses = []
    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions])
    )
    if response.usage_metadata is None:
        raise RuntimeError(
            "API request failed. Check internet connection, and API key.")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls is not None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if function_call_result.parts is None:
                raise Exception("Function call returned no parts.")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Function call returned no response.")
            if args.verbose:
                print(f"Function call result: {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
    else:
        print("Response:")
        print(response.text)
    #print("I'M JUST A ROBOT")


if __name__ == "__main__":
    main()
