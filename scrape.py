from bs4 import BeautifulSoup
import requests
import urllib.parse

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title_string = soup.find("span", attrs={"id":'productTitle'}).string.strip()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		# price = soup.find("span", attrs={'class':'a-price a-offscreen'}).string.strip()
		price = soup.select_one("span.a-price .a-offscreen").string.strip()

	except AttributeError:

		try:
			# If there is some deal price
			price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

		except:		
			price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = "Not Available"	

	return available	


if __name__ == '__main__':

	# Ask user what to scrape
	target_product = urllib.parse.quote_plus(input("Enter the target product to scrape (default is playstation 4): ").strip() or "playstation 4")

	# Headers for request
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	            'Accept-Language': 'en-US',
				'Origin': 'https://www.amazon.com'})

	# The webpage URL
	URL = f"https://www.amazon.com/s?k={target_product}"
	
	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	# Fetch links as List of Tag Objects
	links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

	# Store the links
	links_list = []

	# Loop for extracting links from Tag Objects
	for link in links:
		links_list.append(link.get('href'))


	# Loop for extracting product details from each link 
	for link in links_list:

		new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

		new_soup = BeautifulSoup(new_webpage.content, "lxml")
		
		# Function calls to display all necessary product information
		print("Product Title =", get_title(new_soup))
		print("Product Price =", get_price(new_soup))
		print("Product Rating =", get_rating(new_soup))
		print("Number of Product Reviews =", get_review_count(new_soup))
		print("Availability =", get_availability(new_soup), end="\n\n\n")
