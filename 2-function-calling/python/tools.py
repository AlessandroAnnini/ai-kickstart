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


def get_author_by_name(author_name):
    """Fetch author by name.
    making a call to the Open Library Books API.
    GET https://openlibrary.org/search.json?author={author_name}

    Args:
        author_name (string): The author name to search for.
    """

    url = f"https://openlibrary.org/search.json?author={author_name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_book_info_by_key(olid):
    """Fetch book info by key.
    making a call to the Open Library Books API.
    GET https://openlibrary.org/books/{olid}.json

    Args:
        olid (string): The key to search for.
    """

    url = f"https://openlibrary.org/books/{olid}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


##############
# Function definitions
##############


functions = [
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_author_by_name",
            "description": "Fetch author by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "author_name": {
                        "type": "string",
                        "description": "The author name to search for.",
                    },
                },
                "required": ["author_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_book_info_by_key",
            "description": "Fetch book info by key.",
            "parameters": {
                "type": "object",
                "properties": {
                    "olid": {
                        "type": "string",
                        "description": "The key to search for.",
                    },
                },
                "required": ["olid"],
            },
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
        model="gpt-4-1106-preview",
        temperature=0.2,
        messages=context,
        tools=functions,
        tool_choice="auto",
    )

    pprint(response.model_dump_json(indent=2))
    # continue

    print("\n")

    ##############################
    # tool_calls
    ##############################

    if response.choices[0].message.tool_calls is not None:
        print("🤖 Tool calls:")
        for tool_call in response.choices[0].message.tool_calls:
            print(f"function name: {tool_call.function.name}")
            print(f"function args: {tool_call.function.arguments}")
            print("\n")

            if tool_call.function.name == "fetch_books_by_subject":
                args = json.loads(tool_call.function.arguments)
                print(f"🤖 {args}")
                subject = args["subject"]
                book_list = fetch_books_by_subject(subject)

                for book in book_list["works"]:
                    print(
                        f"{book['first_publish_year']} - {book['key']} - {book['title']}"
                    )

                print("\n")

            if tool_call.function.name == "get_author_by_name":
                args = json.loads(tool_call.function.arguments)
                print(f"🤖 {args}")
                author_name = args["author_name"]
                author_list = get_author_by_name(author_name)

                for author in author_list["docs"]:
                    if author["type"] != "author":
                        continue
                    print(f"{author['name']} ({author['birth_date']})")

                print("\n")

            if tool_call.function.name == "get_book_info_by_key":
                args = json.loads(tool_call.function.arguments)
                print(f"🤖 {args}")
                olid = args["olid"]
                book_info = get_book_info_by_key(olid)

                print(
                    f"title: {book_info['title']}\ndescription: {book_info['description']}"
                )

                print("\n")

        continue

    ##############################
    # classic response
    ##############################

    print(f"🤖 {response.choices[0].message.content}\n\n")
