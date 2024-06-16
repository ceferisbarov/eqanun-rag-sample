from sentence_tokenizer_aze.utils import dot_separation, question_exclamation


def sent_tokenize_aze(text: str) -> list:
    """
    Args:
        text: The given text that will be tokenized into sentences.

    Returns:
         The sentences that are extracted from the text in the list format
    """
    if type(text) != str:
        raise TypeError("Input type has to be string")

    return question_exclamation(dot_separation(text))