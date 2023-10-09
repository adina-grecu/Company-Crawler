
Company Crawler



------------------------run.py------------------------
`run.py` is the main file that runs the programs in order, and it is the only file that needs to be run. 


I chose Python because it has powerful libraries that assist in web scraping, data processing and it's easy to integrate with Elasticsearch. Afer deciding this, Flask was a natural choice for the web framework.


-----------------Company Scraper------------------------------------------------

For this part, I aimed to cover the data extraction, scraping phone numbers and social media links from the given set of websites. I used Scrapy because it's efficient and reliable for such tasks. For the phone numbers, I decided to use regex. One challenge was determining an effective regex pattern to identify them. After some tweaking, I settled on a pattern that seems to capture the majority of phone number formats. Additionally, I used CSS selectors to streamline the extraction of social media links. I decided to output the results to a JSON file, keeping in mind the need to later combine this data with the company profiles.

----------------Data Analysis----------------------------------------------------

This script is responsible for the data analysis. It reads the JSON file and calculates the coverage, phone number fill rate and social media links fill rate. The results are written to a text file. The coverage represents the number of websites we have data for, while the fill rates represent the percentage of websites for which we have found phone numbers and social media links.

-----------------Data Storage----------------------------------------------------

This program is responsible for merging the scraped data with the company profiles and storing the result in Elasticsearch. I used Pandas to merge the dataframes and Elasticsearch's Python client to store the data. I decided to use Elasticsearch because it's a powerful search engine that can be used for data analysis and visualization and it's also easy to integrate with Python.
Firstly, I load and parse the JSON file to return its contents as Python data in order to be able to work with it further. Then, I integrate the data scraped from websites earlier with the company profiles. I decided to use the domain as a key to merge the dataframes. For this, I adjusted the 'website' column to extract the domain name. Lastly, I take the merged data and store it in an Elasticsearch index. The function establishes a connection to a local Elasticsearch instance and converts the merged data to a format suitable for Elasticsearch storage.
Data is stored in chunks for efficiency and, if any insertion fails, the corresponding error message is printed. In essence, this script acts as a bridge between the scraped data and the company profiles, allowing us to store the data in a database.

-----------------API Server------------------------------------------------------

This is the API server that allows us to search for a company profile by name, phone number or Facebook link. I defined a route at the endpoint '/search' that listens for POST requests. I decided to use a POST type of request because we send a JSON object within the body of the request. For the matching algorithm, I decided to build it upon Elasticsearch's multi_match query. I chose this because it allows for text searching against multiple fields and that makes for a more robust search and seamless user experience. I also used fuzziness to allow the search to be forgiving. The code doesn't explicitly define which match is the most relevant. Instead, I used Elasticsearch's built-in scoring and ranking mechanism and return the most relevant hit (the first one in the list).


Usage:

1. Install the required packages (make sure you have Python and pip installed)

`pip install -r requirements.txt`

2. Run the program:

`python run.py`

3. You need to have Elasticsearch running on your machine. If you don't, you can download it from here: https://www.elastic.co/downloads/elasticsearch

4. Open Postman and send a POST request to the endpoint 'http://localhost:5000/search' with the following JSON object in the body:

`{
    "query": "example.com"
}`

You can include the company name, phone number or Facebook link in the query. The API will return the most relevant hit.