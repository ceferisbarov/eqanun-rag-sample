import re  # Regex library
from sentence_tokenizer_aze.regex_patterns import EMAIL_REGEX, URL_REGEX, NUMBER_WITH_DOT, EXCEPTIONS, FILE_NAMES


def dot_separation(text: str) -> list:
    """
    This function separates the text due tu dot in the given text.

    Args:
        text: The text that will be separated into sentences according to dot pattern.

    Returns:
        The separated sentences from the given text in a list format.

    """
    # Initial version of the sentence
    sentence = ""
    # List for the sentences
    sentences = []
    not_separation_pattern = "(?:" + EMAIL_REGEX + "|" + URL_REGEX + "|" + \
                              NUMBER_WITH_DOT + "|" + EXCEPTIONS + "|" + FILE_NAMES + ")"
    first_separation = list(filter(None, re.split(not_separation_pattern, text)))
    exceptions = sum([list(filter(None, i)) for i in re.findall(not_separation_pattern, text)], [])
    for part in first_separation:
        if part in exceptions:
            sentence += part
        else:
            # Separate the text into sentences there is no capital letter before it.
            dot_pattern = "((?<!(?:\s|\.)[ABCÇDEƏFGĞHXIİJKQLMNÖPRSŞTUÜVYZabcçdeəfgğhxıijkqlmnöprsştuüvyz])\.)"
            separated_text = list(filter(None, re.split(dot_pattern, part)))
            for index in range(len(separated_text)):
                # If the separated part is dot that means the previous part is sentence
                if separated_text[index] == ".":
                    # sentence != "" means if there is a dot at the beginning of the sentence do not separate it
                    sentence += "."  # Make it sentence
                    if index != len(separated_text) - 1 and sentences == []:
                        if len(sentence.strip('. ')) == 1 or sentence == ".":
                            continue
                    if len(sentence.strip()) > 2 or sentences == []:
                        sentences.append(sentence)
                    elif len(sentence.strip()) == 2 and sentence.strip('. ').isnumeric() and index != len(
                            separated_text) - 1:
                        continue
                    else:
                        sentences[-1] += sentence
                    sentence = ""
                    continue
                sentence += separated_text[index]

    if sentence != "": sentences.append(sentence)
    return sentences


def question_exclamation(sentence_list: list) -> list:
    """
    This function separates output of the "dot_separation()" into sentences due to question(?,??), exclamation(!,!!) or
    combination of both(?!,!?).
    Args:
        sentence_list: The output of the "dot_separation()" function in a list format.

    Returns:
        The new extracted sentences from the "space_after_dot()" function's output  due to question(?,??),
        exclamation(!,!!) or combination of both(?!,!?) in a list format.

    """
    sentences = []  # List for the sentences

    for snt in sentence_list:
        sentence = ""  # Initial version of the sentence
        # Separating due to '?', '!' or both, if a capital letter comes after them (»"'” - is excluded)
        separated_snt = list(filter(None, re.split('([?!]+[»"”]?)', snt)))
        for index in range(len(separated_snt)):
            if "!" in separated_snt[index] or "?" in separated_snt[index]:
                if sentence == "":
                    sentence += separated_snt[index]
                    continue
                sentence += separated_snt[index]
                if len(separated_snt) != 1 and index != len(separated_snt) - 1:
                    raw_word = re.sub(r'[^a-zA-ZƏİŞĞÖÜIÇəi̇şğöüçı]', '', separated_snt[index + 1])
                    if len(raw_word) != 0 and raw_word[0].isalpha() and raw_word[0].islower():
                        continue
                if len(sentence.strip()) > 2 or sentences == []:
                    sentences.append(sentence)
                else:
                    sentences[-1] += sentence
                sentence = ""
                continue
            sentence += separated_snt[index]
        if sentence != "": sentences.append(sentence)
    return sentences
