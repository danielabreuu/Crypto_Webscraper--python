from bs4 import BeautifulSoup #parsing library
import requests #url request library

def infofinder(choice): #info finding function
  answered = False #a variable to know if the info has been retrieved ('answered') yet
  while not answered: 
    if choice in tickerlist: #if the choice is in the list of tickers

      coinname = namelist[tickerlist.index(choice)] #finding the name of the currency by looking for it's index equivalent in the namelist

      infopage = BeautifulSoup(requests.get('https://www.coinmarketcap.com/currencies/' + coinname.lower().replace(' ', '-') + '/').text, 'html.parser') #finding the infopage by looking for the currency page url + the name of the chosen coin (in lowercase and without spaces but instead dashes) and parsing through the text info from this website
      info = infopage.find_all( class_ = 'sc-1lt0cju-0 srvSa') #making a list of tags with this CSS class which is where the info is located
      for i in info: #this is used to find the 'div' tag which contains info, as opposed to some other tags that may have the same CSS class
        for i in i.contents:
          if i.name == 'div':
            trueinfo = i #adding the 'div' tags into its own variable called 'trueinfo'
                            
      idcount = 0 #a counter variabel for searching for tags with IDs, which represent a change in topic of the info paragraphs I am looking for... I.e. the information about founders has an ID called "who-are-founders" and information about the coin itself has a different ID
      for child in trueinfo: #for every tag within trueinfo (referred to as a 'child' tag)
        if child.attrs: #if the tag has any attributes(ID)
          idcount += 1 #raise the counter for every tag with attributes (ID)
          if idcount > 1: #the first ID is the one I am looking for, therefore I stop after we count to one
            break
            answered = True
        if len(child.contents): #if there's 1 or more contents (within the child tag) 
          for grandchild in child: #for every content in the child, called "grandchild"
            print(grandchild.string, end = ' ') #print the grandchild's string informaton (with no new line at the end). I have to go through the grandchildren as well to make sure the entire information paragraph is printed correctly, because some of it is contained in tags within tags.
        else:
          print(child.string, end = '') #print the information of the child tag (with no new line)

    else:
      choice = input("Please enter one of the tickers correctly! ").lower().replace(' ', '') #message printed if the ticker is not found, to try again.
      print('')
      continue
      
    repeat = input("\n\nWould you like to get info on another currency? \nType in it's ticker to learn more or type \'end\' to close this program! ").lower().replace(' ', '') #recording the answer to the prompt as 'repeat' (in lowercase and with no spaces)
    print('') #newline

    if repeat == 'end':
      break #end it

    if repeat in tickerlist: #if the choice is in the list of tickers
      print('') #new line
      infofinder(repeat) #do this whole function again but with the repeat answer
      break #then end when you get back here

    else:
      lastchance = input("Please enter one of the tickers correctly! ").lower().replace(' ', '') #message printed if the ticker is not found
      print('') #newline
      infofinder(lastchance) #run this program again but with the lastchance answer
      break #then end when you get back here

#just some basic information for the user
print('~~ALL INFORMATION FOUND HERE IS SOURCED FROM COINMARKETCAP.COM~~\n')
print('The following are the top 10 cryptocurrencies at the moment...')
print('They are structured here by NAME | TICKER | PRICE:\n')

page = BeautifulSoup(requests.get('https://coinmarketcap.com/').text, 'html.parser') #requesting the HTML information from a URL of a website that lists cryptocurrency prices. 
top10 = page.findAll('tr', limit = 10) #a list variable that contains the ten first tags called 'tr' (table row)
namelist = [] #an empty list for names
tickerlist = [] #an empty list for tickers (the short abbreviation for these currencies)

for tag in top10: #for every tag in the top 10 list

  nametag =  tag.find(class_ = 'sc-1eb5slv-0 iJjGCS') #nametag variable to hold information of a tag with the CSS class related to names
  if nametag != None: #if the nametag is not empty 
    name = nametag.contents[0] #set the name to the first index of the nametag list (there's only 1 index in the list at a time)
    print(name, '|', end = ' ') #print the name as well as a | to make the output easier to read (with no new line at the end)
    namelist.append(name) #add this to the namelist 

  tickertag = tag.find(class_ = 'sc-1eb5slv-0 gGIpIK coin-item-symbol') #tickertag variable to hold the information of a tag with the CSS class related to tickers
  if tickertag != None: #if the tickertag is not empty
    ticker = tickertag.contents[0] #set the ticker to the first index of the tickertag list (there's only 1 index in the list at a time)
    print(ticker, '|', end = ' ') #print the ticker as well as a | to make the output easier to read (with no new line at the end)
    tickerlist.append(ticker.lower()) #add this to the tickerlist 

  pricetag = tag.find(class_ = 'price___3rj7O') #pricetag variable to hold the information of a tag with the CSS class related to the price 
  if pricetag != None: #if the pricetag is not empty
    if pricetag.find('a') != None: #if the tag containing the price ('a' or 'anchor' tag) is not empty
      price = pricetag.find('a').contents[0] #set the price to the first index of the pricetag list (there's only 1 index in the list at a time)
      print(price) #print the price

choice = input('\nTo learn more about one of these currenices, type in it\'s ticker! ').lower().replace(' ', '')  #the coin choice (in lowercase and without spaces)
print('') #grammar (adding a space under the text displayed)

infofinder(choice) #run the info finder function!
