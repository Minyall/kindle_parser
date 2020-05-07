# Kindle Parser
The Kindle Reader App allows you to export your highlighted text as a static HTML file. This is great and all, but
pretty useless when it comes to compatibility. This script takes the HTML export from Kindle, and produces a structured
text file, using the books' sections, chapters and the colour of your highlights as headings.
Each quote also retains page and Kindle location information, if available.
 
## Requirements
This script uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and Lxml
Install using
 ```pip install -r requirements.txt```

 or
```
pip install beautifulsoup4
pip install lxml
 ```

## Usage
`python kindle_parser.py --filename my_kindle_export_file.html
`
 
## Why?
Researchers may find this useful if they want to be able to easily export their highlighted passages from Kindle Reader,
into some qualitative analysis software such as Nvivo or MaxQDA.
 
You may have other nefarious schemes.