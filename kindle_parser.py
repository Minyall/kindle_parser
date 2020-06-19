#!/usr/bin/env python
# coding: utf-8

import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='The location of the HTML output from Kindle Reader')
parser.add_argument('-dg', '--double_guitar', action='store_true',  help='By popular demand...')

args = parser.parse_args()

if args.filename is None:
    raise Exception('Please provide HTML filename')


def extract_highlight(text):
    start = text.find('(')
    end = text.find(')')
    return text[start + 1:end]


def extract_page(text):
    if '> Page ' in text:
        start = text.rfind('> Page')
        end = text.rfind(' · ')
        substring = text[start + 1:end]
        result = int(''.join((char for char in substring if char.isdigit())))
    elif ' - Page' in text:
        start = text.find(' - Page')
        end = text.find(' · ')
        substring = text[start + 1:end]
        result = int(''.join((char for char in substring if char.isdigit())))
    else:
        result = None
    return result


def extract_location(text):
    result = None
    if ' · Location ' in text:
        start = text.rfind(' · Location ')
        substring = text[start:]
        result = int(''.join((char for char in substring if char.isdigit())))
    elif '- Location ' in text:
        start = text.rfind('- Location ')
        substring = text[start:]
        result = int(''.join((char for char in substring if char.isdigit())))
    return result


def extract_chapter(text):
    start = text.find(') - ')
    end = text.rfind(' > ')
    substring = text[start + 4:end].strip()
    return substring


# Load Kindle Export and parse with BS4

with open(args.filename, 'rb') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

# Determine filename

authors = soup.find('div', class_='authors').text.strip()
first_surname = authors.split(',')[0]
title = soup.find('div', class_='bookTitle').text.strip()
filename = f"{first_surname}_{title}.txt"

# Data structures to retain extracted information
sections = []
highlight_colour = []
pages = []
locations = []
chapters = []
quotes = []

# Parsing the highlight line
for x in soup.find_all('h3', class_='noteHeading'):
    text = x.text
    highlight_colour.append(extract_highlight(text))
    pages.append(extract_page(text))
    locations.append(extract_location(text))
    section = x.find_previous('h2', class_='sectionHeading').text
    sections.append(section)

    if ' > ' in text:
        chapter = extract_chapter(text)

    else:
        chapter = None
    chapters.append(chapter)
    x.decompose()  # remove highlight lines so they don't get caught in later text extraction

# Remove all section headings now we don't need to refer to them, again to avoid being caught in text extraction
[x.decompose() for x in soup.find_all('h2', class_='sectionHeading')]

# Extract quotes, and format with page and location info
for i, x in enumerate(soup.find_all('div', class_='noteText')):
    quote = x.text.strip()
    page_loc = f'Page:{pages[i]} - ' if pages[i] is not None else ''
    quote = f"* {quote}\n{page_loc}Loc:{locations[i]}\n\n"

    quotes.append(quote)

# Check all lists are equal length
assert len(sections) == len(highlight_colour) == len(pages) == len(locations) == len(chapters) == len(
    quotes), "Data lengths are misaligned - dunno!"

# Set memories to keep track of when heading need to be written
prior_section = 0
prior_chapter = 0
prior_highlight = 0

# Write file
with open(filename, 'w') as f:
    for section, chapter, highlight, quote in zip(sections, chapters, highlight_colour, quotes):
        if section is not None and section != prior_section:
            f.write(f"# {section}\n\n")
            prior_section = section
            prior_chapter = 0
            prior_highlight = 0
        if chapter is not None and chapter != prior_chapter:
            f.write(f"## {chapter}\n\n")
            prior_chapter = chapter
            prior_highlight = 0
        if highlight is not None and highlight != prior_highlight:
            f.write(f"### {highlight}\n\n")
            prior_highlight = highlight
        f.write(quote)

if args.double_guitar:
    from double_guitar import a
    print(a)
