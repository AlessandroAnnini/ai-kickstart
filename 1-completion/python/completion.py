import os
import sys
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


context = []
context.append({"role": "system", "content": "You are a useful assistant."})


####################
# without streaming #
####################


while True:
    question = input("> ")

    if question == "bye":
        break

    context.append({"role": "user", "content": question})

    response = openai.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=context,
    )

    assistantResponse = response.choices[0].message.content

    context.append({"role": "assistant", "content": assistantResponse})

    print("\n")

    print(f"🤖 {assistantResponse}\n\n")
    # print(response.usage)


##################
# with streaming #
##################


# while True:
#     question = input("> ")

#     if question == "bye":
#         break

#     context.append({"role": "user", "content": question})

#     stream = openai.chat.completions.create(
#         model="gpt-4",
#         temperature=0.2,
#         messages=context,
#         stream=True,
#     )

#     print("\n")
#     sys.stdout.write("🤖 ")

#     for part in stream:
#         chunk_message = part.choices[0].delta
#         if chunk_message and chunk_message.content:
#             sys.stdout.write(chunk_message.content)
#             sys.stdout.flush()

#     print("\n\n")
