from data.book_dict import book_summaries_dict


def get_summary_by_title(title: str) -> str:
    """
    Retrieves the summary of a book by its title.
    :param title: The title of the book to search for.
    :return: The summary of the book or an error message if not found.
    """
    return book_summaries_dict.get(title, "Book summary not found.")


TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_summary_by_title",
        "description": "Return the summary of a known book by its title.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the book to get the summary for."
                }
            },
            "required": ["title"],
            "additionalProperties": False
        }
    }
}]


SYSTEM_PROMPT = """
You are a helpful assistant that recommends books based on user requests.
You will receive a user query and a list of retrieved books (title + summary).
Pick exactly one book that best matches the user's interests.
Then, you must call the function `get_summary_by_title` with that exact title to retrieve the full summary.
Keep the final message concise: recommend the book and explain briefly your choice.
If the user prompt is not related to books, respond with "Your request is outside my scope.
I can only help with book recommendations."
"""