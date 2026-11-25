
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

MODEL = "openai/gpt-oss-20b"

# Model pricing per 1 million tokens
INPUT_PRICE = 0.075
OUTPUT_PRICE = 0.30

system_prompt = """
You are a helpful AI assistant.
Explain things simply and clearly.
"""

messages = [
    {"role": "system", "content": system_prompt}
]

json_mode = False

# Overall usage tracking
total_input_tokens = 0
total_output_tokens = 0
total_cost = 0.0


def show_usage(usage):
    global total_input_tokens, total_output_tokens, total_cost

    if usage is None:
        print("\nUsage information was not received.")
        return

    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    all_tokens = usage.total_tokens

    # Calculate message cost
    cost = (
        input_tokens * INPUT_PRICE +
        output_tokens * OUTPUT_PRICE
    ) / 1_000_000

    # Update session totals
    total_input_tokens += input_tokens
    total_output_tokens += output_tokens
    total_cost += cost

    print("\n\n----- MESSAGE USAGE -----")
    print(f"Input tokens:  {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens:  {all_tokens}")
    print(f"Message cost:  ${cost:.8f}")

    print("\n----- SESSION TOTAL -----")
    print(f"Input tokens:  {total_input_tokens}")
    print(f"Output tokens: {total_output_tokens}")
    print(f"Total tokens:  {total_input_tokens + total_output_tokens}")
    print(f"Total cost:    ${total_cost:.8f}")
    print("-------------------------")


print("Chatbot started! Type exit to quit.")
print("Type /json to toggle JSON mode.")

while True:

    user_input = input("\nYou: ").strip()

    if not user_input:
        continue

    # Quit commands
    if user_input.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    # Toggle JSON mode
    if user_input.lower() == "/json":
        json_mode = not json_mode
        print("JSON mode:", "ON" if json_mode else "OFF")
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    # JSON MODE
    if json_mode:

        request_messages = messages.copy()

        request_messages[0] = {
            "role": "system",
            "content": system_prompt +
            "\nReturn your answer in valid JSON format."
        }

        response = client.chat.completions.create(
            model=MODEL,
            messages=request_messages,
            response_format={"type": "json_object"},
            reasoning_format="hidden"
        )

        assistant_reply = response.choices[0].message.content

        data = json.loads(assistant_reply)

        print("\nAssistant:")
        print(json.dumps(data, indent=4))

        # Get usage from API response
        show_usage(response.usage)

    # NORMAL STREAMING MODE
    else:

        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

        print("\nAssistant: ", end="", flush=True)

        assistant_reply = ""
        usage = None

        for chunk in stream:

            # Get usage from Groq's final chunk
            groq_data = getattr(chunk, "x_groq", None)

            if groq_data is not None:
                usage = getattr(groq_data, "usage", None)

            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                print(content, end="", flush=True)
                assistant_reply += content

        print()

        # Display token usage and cost
        show_usage(usage)

    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })
