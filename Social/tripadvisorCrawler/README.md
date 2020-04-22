The program reads in sites to crawl from a text file ``sites.txt``, an example of which is given as ``sites-all.txt``, containing some of the sites relevant to the CUTLER project.

Note that the crawler only crawls reviews of destination pages, since hotel pages have a different format and would require a different crawler.

Also, the crawler requires Selenium WebDriver to be properly set up, a link to the relevant documentation is included in the Python script itself. By default the script looks for the Firefox driver and runs Firefox in headless mode for crawling. Both Chrome and Firefox supports headless modes, although the script can run without setting the headless option.
Sometimes, an error will happen stating that the HTML element HEADING cannot be found, as far as we know this error occurs when the crawler request the element before the page can finish loading the relevant parts, and will go away after a few retries.

The format of the output is CSV.
