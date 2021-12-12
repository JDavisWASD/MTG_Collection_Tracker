A website that allows users to catalog their collection of Magic: The Gathering cards and see the average prices of said cards from 1-2 external websites via APIs.

Landing Page:
- Login and Register Buttons
- Individual card search w/o login

Search Result:
- Individual card search w/o login
- Display card result:
    - Image of Card
    - Card Name
    - Card Description
    - Prices

Login Page:
- Username and password input w/ validations

Registration Page:
- Username, email, password, and confirmation w/ validations/regex

Collection Page:
- Display total quantity of cards
- Display number of unique cards
- Table of cards in collection
    - Add cards
    - Remove cards
    - Edit quantity
    - Clicking card name uses search result page to display full card info

Data Plan:
- Bulid a table of users as they register
- ~~Have a pre-built table of existing cards and their information~~ (Way to big)
- ~~Check card searches against .json from MTGJSON~~ (Still really big)
- Search for cards against Scryfall API
- Build a table of cards as users search for them
- Connect both tables in a many to many relationship based on user input

Future Features:
- Dark mode
- Export/Import via CSV
- Ability to subdivide a collection into multiple decks of cards
- Password reset
- ~~Specify printing edition of cards~~ (Done)
- Sort by table column
- Split table into pages
- Make Login and Registartion popups/overlays instead of individual pages
- Switch to pulling prices from retailers directly to get more reliable prices
- Make the error message for adding a specific card specify style in collection
- Selecting which currency to display
- Display total price of all cards
- Support split and double face cards