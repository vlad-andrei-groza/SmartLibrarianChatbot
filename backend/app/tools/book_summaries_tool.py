from data.book_dict import book_summaries_dict


def get_summary_by_title(title: str) -> str:
    """
    Retrieves the summary of a book by its title.
    :param title: The title of the book to search for.
    :return: The summary of the book or an error message if not found.
    """
    return book_summaries_dict.get(title, "Book summary not found.")


tools = [{
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