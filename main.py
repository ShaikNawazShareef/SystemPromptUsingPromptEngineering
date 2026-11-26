import os
import sys
import time
import random

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


# ==========================================
# 1. CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

PRIMARY_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-3.8-flash-lite"
)

MAX_RETRIES = 4

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing in .env")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)


# ==========================================
# 2. GEMINI API WITH RETRY
# ==========================================

def generate_with_retry(prompt, system_instruction, temperature=0.7):

    models = [PRIMARY_MODEL]

    if FALLBACK_MODEL and FALLBACK_MODEL != PRIMARY_MODEL:
        models.append(FALLBACK_MODEL)

    last_error = None

    for model in models:

        print(f"\nUsing model: {model}")

        for attempt in range(MAX_RETRIES):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature,
                        max_output_tokens=4096
                    )
                )

                if not response.candidates or not response.text:
                    reason = (
                        response.candidates[0].finish_reason
                        if response.candidates else "UNKNOWN"
                    )
                    raise ValueError(
                        f"Gemini returned an empty response (finish_reason: {reason})."
                    )

                return response.text

            except errors.APIError as error:

                last_error = error
                status_code = error.code

                # Skip retries on 404 (model deprecated/unavailable) and try fallback.
                if status_code == 404:
                    print(f"Model {model} not found (404). Switching to fallback...")
                    break

                # Retry temporary server errors and rate limits.
                if status_code in (408, 429, 500, 502, 503, 504):

                    if attempt < MAX_RETRIES - 1:

                        wait_time = min(
                            2 ** attempt + random.uniform(0, 1),
                            30
                        )

                        print(
                            f"Temporary Gemini error: {status_code}"
                        )

                        print(
                            f"Retrying in {wait_time:.1f} seconds..."
                        )

                        time.sleep(wait_time)

                        continue

                    print(
                        f"{model} failed after {MAX_RETRIES} attempts."
                    )

                    break

                # Authentication, permission, or invalid request errors.
                raise RuntimeError(
                    f"Gemini API error ({status_code}): {error}"
                ) from error

            except Exception as error:

                last_error = error

                print(f"Unexpected error: {error}")
                break

        print("Trying the next model if available...")

    raise RuntimeError(
        "All configured Gemini models failed. "
        f"Last error: {last_error}"
    )


# ==========================================
# 3. IMPROVE ORIGINAL PROMPT
# ==========================================

def improve_prompt(
    user_prompt,
    role,
    context,
    output_format
):

    instructions = """
You are an expert Prompt Engineer.

Your job is to transform rough user prompts
into professional and effective AI prompts.

Include these six components:

1. Role
2. Context
3. Task
4. Specific Instructions
5. Constraints
6. Expected Output Format

Important rules:

- Understand the user's original intention.
- Improve clarity and structure.
- Use simple and professional language.
- Do not answer the original question.
- Only generate the improved prompt.
"""

    input_text = f"""
ORIGINAL PROMPT:
{user_prompt}

AI ROLE:
{role}

CONTEXT:
{context}

EXPECTED OUTPUT FORMAT:
{output_format}

Create a complete and professional improved prompt.
"""

    print("\nImproving your prompt...")

    return generate_with_retry(
        input_text,
        instructions,
        temperature=0.3
    )


# ==========================================
# 4. GENERATE FINAL ANSWER
# ==========================================

def generate_answer(improved_prompt, role):

    instructions = f"""
You are acting in the following role: {role}.

Follow the improved prompt carefully.

Rules:

- Use simple English.
- Give clear explanations.
- Provide practical examples.
- Include Python code when requested.
- Use headings and bullet points where useful.
- Avoid unnecessary information.
"""

    print("\nGenerating final answer...")

    return generate_with_retry(
        improved_prompt,
        instructions,
        temperature=0.7
    )


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

def display_results(improved_prompt, answer):

    print("\n")
    print("=" * 60)
    print("             IMPROVED PROMPT")
    print("=" * 60)

    print(improved_prompt)

    print("\n")
    print("=" * 60)
    print("                AI RESPONSE")
    print("=" * 60)

    print(answer)

    print("\n")
    print("=" * 60)


# ==========================================
# 6. MAIN APPLICATION
# ==========================================

def main():

    print("\n")
    print("=" * 60)
    print("          PROMPTFORGE AI")
    print("       GEMINI PROMPT ENGINEER")
    print("=" * 60)

    print(f"\nPrimary model: {PRIMARY_MODEL}")
    print(f"Fallback model: {FALLBACK_MODEL}")

    while True:

        print("\nEnter your original prompt:")

        user_prompt = input("You: ").strip()

        if not user_prompt:

            print("Please enter a valid prompt.")
            continue

        if user_prompt.lower() in ("exit", "quit"):

            print("Thank you for using PromptForge AI!")
            break

        role = input(
            "\nEnter AI role: "
        ).strip()

        if not role:
            role = "Helpful AI Assistant"

        context = input(
            "\nEnter context: "
        ).strip()

        if not context:
            context = "No additional context"

        output_format = input(
            "\nEnter expected output format: "
        ).strip()

        if not output_format:
            output_format = "Structured explanation with examples"

        try:

            # Stage 1: Improve prompt

            improved_prompt = improve_prompt(
                user_prompt,
                role,
                context,
                output_format
            )

            # Stage 2: Generate answer

            answer = generate_answer(
                improved_prompt,
                role
            )

            # Display both results

            display_results(
                improved_prompt,
                answer
            )

        except KeyboardInterrupt:

            print("\nApplication interrupted.")
            break

        except Exception as error:

            print("\nAPPLICATION ERROR")
            print("-" * 40)
            print(error)

            print(
                "\nPlease check your API key, model availability, "
                "quota and internet connection."
            )

        choice = input(
            "\nDo you want to continue? (yes/no): "
        ).strip().lower()

        if choice not in ("yes", "y"):

            print("\nThank you for using PromptForge AI!")
            break


# ==========================================
# 7. APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()