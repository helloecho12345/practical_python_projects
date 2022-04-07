import requests
import lxml.html

html = requests.get("https://store.steampowered.com/explore/new/")   # website url where data you want is
doc = lxml.html.fromstring(html.content)   # provides object with xpath method to query HTML document

new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]   # "//" tell lxml that we want to search for all tags in the HTML document which match our requirements/filters
# div tells lxml that we are searching for div tags in the HTML page
# [@id="tab_newreleases_content"] tells lxml that we are only interested in those divs which have an id of tab_newreleases_content

titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')   # gives titles of all the games in the Popular New Releases tab
# . tells lxml that we are only interested in the tags which are the children of the new_releases tag
# [@class="tab_item_name"] means we are filtering based on class name
# "/text()" tells lxml that we want the text contained within the tag we just extracted nad it returns the title contained in the div with the tab_item_name class name

prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()') # same as titles except class name changed to prices


tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = []

tags = [tag.text_content() for tag in
        new_releases.xpath('.//div[@class="tab_item_top_tags"]')]

    
# extracting divs containing the tags for the games
# then loop over the list of extracted tags and extract the text from those tags using the text_content() method
# text_content() returns the text contained within an HTML tag without the HTML markup

# alternate code:
# for div in tags_divs:
#   tags.append(div.text_content())
# for tag in tags:
    # total_tags.append(tag.text_content())
    
tags = [tag.split(', ') for tag in tags]

platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')   # extract the tab_item_details div
total_platforms = []

for game in platforms_div:
  temp = game.xpath('.//span[contains(@class, "platform_img")]')   # 
  platforms = [t.get('class').split(' ')[-1] for t in temp]
  if 'hmd_separator' in platforms:
    platforms.remove('hmd_separator')
  total_platforms.append(platforms)
  
  output = []
  for info in zip(titles, prices, tags, total_platforms):   # uses zip function to iterate over all of those lists in parallel & assigns title, price, tags, and platforms as a separate key in that dictionary
    resp = {}   # creates dictionary for each game
    resp['title'] = info[0]
    resp['price'] = info[1]
    resp['tags'] = info[2]
    resp['platforms'] = info[3]
    output.append(resp)   # appends dictionary to output list