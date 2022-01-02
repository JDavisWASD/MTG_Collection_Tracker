## MTG Collection Tracker
A MVP of a website that allows users to catalog their collection of Magic: The Gathering cards, search a database of cards, and view the daily prices of cards. The project was built using Python, Flask, MySQL, and the Scryfall.com API.

Landing Page:
- Login and Register Buttons
- Individual card search w/o login

Search Result:
- Individual card search w/o login
- Display card result:
    - Image of card
    - Card name
    - Card description
    - Prices

Login Page:
- Username and password input with validations

Registration Page:
- Username, email, password, and password confirmation with validations

Collection Page:
- Display total quantity of cards
- Display number of unique cards
- Table of cards in collection
    - Add cards
    - Remove cards
    - Edit quantity
    - Clicking card name uses the search result page to display full card info

Data Plan:
- Bulid a table of users as they register
- Search for cards against Scryfall API
- Build a table of cards as users add them to a collection
- Connect both tables in a many to many relationship based on user input
