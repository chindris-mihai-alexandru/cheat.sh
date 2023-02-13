"""
Markdown support.

Exports:
    format_text(text, config=None, highlighter=None):

Uses external pygments formatters for highlighting (passed as an argument).
"""

import re
import ansiwrap
import colored

def format_text(text, config=None, highlighter=None):
    """
    Renders `text` according to markdown rules.
    Uses `highlighter` for syntax highlighting.
    Returns a dictionary with "output" and "links".
    """
    return _format_section(text, config=config, highlighter=highlighter)

def _split_into_paragraphs(text):
    return re.split('\n\n+', text)

def _colorize(text):
    return \
        re.sub(
            r"`(.*?)`",
            colored.bg("dark_gray") \
                + colored.fg("white") \
                + " " + r"\1" + " " \
                + colored.attr('reset'),
            re.sub(
                r"\*\*(.*?)\*\*",
                colored.attr('bold') \
                    + colored.fg("white") \
                    + r"\1" \
                    + colored.attr('reset'),
                text))

def _format_section(section_text, config=None, highlighter=None):

    # cut code blocks
    block_number = 0
    while True:
        section_text, replacements = re.subn(
            '^```.*?^```',
            f'MULTILINE_BLOCK_{block_number}',
            section_text,
            1,
            flags=re.S | re.MULTILINE,
        )
        block_number += 1
        if not replacements:
            break

    # cut links
    links = []
    while True:
        regexp = re.compile(r'\[(.*?)\]\((.*?)\)')
        if not (match := regexp.search(section_text)):
            break


        links.append(match[0])
        text = match[1]
            # links are not yet supported
            #
        text = '\x1B]8;;%s\x1B\\\\%s\x1B]8;;\x1B\\\\' % (match[2], match[1])
        section_text, replacements = regexp.subn(
            text, # 'LINK_%s' % len(links),
            section_text,
            1)
        block_number += 1
        if not replacements:
            break

    answer = ''.join(
        "\n".join(
            ansiwrap.fill(_colorize(line)) + "\n"
            for line in paragraph.splitlines()
        )
        + "\n"
        for paragraph in _split_into_paragraphs(section_text)
    )
    return {
        'ansi': answer,
        'links': links
    }
