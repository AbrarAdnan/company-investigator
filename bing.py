import asyncio
import sys
from EdgeGPT import Chatbot, ConversationStyle

async def main(prompt):
    bot = await Chatbot.create()  # Passing cookies is optional

    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.balanced)

    # Get the response message
    messages = response['item']['messages']
    response_message = messages[1]['text']  # Assuming the response is at index 1

    await bot.close()

    return response_message

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument.")
    else:
        prompt = sys.argv[1]
        result = asyncio.run(main(prompt))
        print("Response:", result)
