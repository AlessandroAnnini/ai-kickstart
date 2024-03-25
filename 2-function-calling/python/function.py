import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pprint import pprint

_ = load_dotenv(find_dotenv())

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

context = []
context.append({"role": "system", "content": "You are a useful assistant."})


##############
# Functions
# https://openlibrary.org/swagger/docs
##############


def fetch_books_by_subject(subject):
    """Fetch books by subject name.
    making a call to the Open Library Books API.
    GET https://openlibrary.org/subjects/{subject}.json?details=false

    Args:
        subject (string): The subject to search for.
    """

    url = f"https://openlibrary.org/subjects/{subject}.json?details=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


##############
# Function definitions
##############


functions = [
    {
        "name": "fetch_books_by_subject",
        "description": "Fetch books by subject name.",
        "parameters": {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "The subject to search for.",
                },
            },
            "required": ["subject"],
        },
    },
]


##############
# Chat loop
##############


while True:
    question = input("> ")

    if question == "bye":
        break

    context.append({"role": "user", "content": question})

    response = openai.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=context,
        functions=functions,
        function_call="auto",
    )

    pprint(response.model_dump_json(indent=2))

    print("\n")

    ##############################
    # function_call
    ##############################

    if response.choices[0].message.function_call is not None:
        print("🤖 Function call:")
        fc = response.choices[0].message.function_call
        print(f"function name: {fc.name}")
        print(f"function args: {fc.arguments}")
        print("\n")

        if fc.name == "fetch_books_by_subject":
            args = json.loads(fc.arguments)
            print(f"🤖 {args}")
            subject = args["subject"]
            book_list = fetch_books_by_subject(subject)

            for book in book_list["works"]:
                print(f"{book['first_publish_year']} - {book['title']}")

            print("\n")

        continue

    ##############################
    # classic response
    ##############################

    print(f"🤖 {response.choices[0].message.content}\n\n")
