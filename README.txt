Contents:
  1. Libraries
  2. Internal Keyword setup
  3. Auto Whatsapp Message setup
  4. Running the script

-------------------------------------------------------------------------------------------------------------

1. Libraries Used:
  - bs4 (BeautifulSoup)
  - requests_html
  - pywhatkit
  - os
  - sys

1.1 Installing necessary libraries:

While some libraries are included in Python by default, we'll need to manually install some of the other libs 
used in the script. To install them, we'll need to go to the CMD, PowerShell, or other preferred console, and
type the following commands.
  - bs4: pip install beautifulsoup4
  - requests_html: pip install requests-html
  - pywhatkit: pip install pywhatkit

-------------------------------------------------------------------------------------------------------------

Setups:

This scripts makes use of constants, located at the start of the code, which are used in multiple of its
features. To properly make use of those features, you'll have to setup those constants.

-------------------------------------------------------------------------------------------------------------

2. Internal Keyword setup:

When using the keyword mode, the script will look for articles containing certain keywords. These keywords
can come from an external file, or from the list KEYWORDS located at the top of the script. To set up your
keywords to search for, fill in this list with string keywords as such:

KEYWORDS = ["word1", "word2", "word3"]

It's also possible to search for sub-strings in the articles, but bear in mind that the script will not look
for the elements of the substring separatedly, and will only flag exact matches for the substring. E.g.:

KEYWORDS = ["word1", "sub string 1", "word2"]

-------------------------------------------------------------------------------------------------------------

3. Auto Whatsapp Message setup:

When using the auto message mode, the script will send a whatsapp message to the specified group at an
established time. This information can be set at the WPP_GROUP_ID, AUTO_MSG_HOUR, and AUTO_MSG_MIN constants
located at the top of the script. WPP_GROUP_ID should be filled with a string group id, which can be obtained
from a whatsapp group invitation link (e.g. https://chat.whatsapp.com/etvyBn4FS4Y3OJSA793rGL, where the ID is
the final group of characters); and AUTO_MSG_HOUR and AUTO_MSG_MIN are integers for the hour and minute where
the message will be sent (hour must be set in 24 hour format). E.g.:

WPP_GROUP_ID = "etvyBn4FS4Y3OJSA793rGL"
AUTO_MSG_HOUR = 17
AUTO_MSG_MIN = 30

3.1 Other considerations:

Using the auto message mode requires an active whatsapp session already open in the default web browser, if
there isn't a previously active session, running the script in this mode will open a log-in prompt.

IMPORTANT: The auto message mode is working, but rough. When the hour set for the script to send the message,
it will take the user system's input to type in and send the message. Therefore, to avoid issues with this
feature, it is recommended to not use the system while the auto message is being typed.

Also, typing the message is done character-by-character, which means that longer messages can take a long span
of time to be typed and sent. 

-------------------------------------------------------------------------------------------------------------

4. Running the script:

From your console, navigate to the location of the script. Then, run the following command:

	python crawler.py [-k] [-f ('PATH_TO_FILE' 'SEPARATOR_CHARACTER')] [-w]

	Optional flags:
	-k: enables the keyword mode. If this flag is set alone, the internal list of keywords is used
	-f: takes keywords from an external file. If this flag is set the next two arguments must be:
		* "PATH_TO_FILE": A string path to the file from which to extract the keywords
		* "SEPARATOR_CHARACTER": A string character used in the separator file to separate keywords.
					 The new line character ('\n') is assumed by default.
	-w: enables the auto message mode.

	Output: A .txt file with the relevant articles from the website.