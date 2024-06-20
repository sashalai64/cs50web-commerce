# CS50's Web Programming with Python and JavaScript

# Project 2 - Commerce
[Project Description](https://cs50.harvard.edu/web/2020/projects/2/commerce/)

## Overview
This project is an eBay-like e-commerce auction platform that enables users to post auction listings, place bids on items, comment on listings, and manage a personalized watchlist. 

## Features
- **User Authentication**
  - Secure user registration and login system.
     
- **Create Listings**
  - Users can create auction listings with a title, description, starting bid, category, and optional image.
 
- **Listing Page**
  - Detailed view of a specific listing including all its details and current price.
  - Signed-in users who are not the owners of the listing can place bids.
  - Signed-in users can add or remove the item from their “Watchlist.”
  - Signed-in users can comment on listings, and view all comments.
  - Listing creators can close auctions.
 
- **Categories**
  - Displays a list of all listing categories.
  - Clicking on a category shows all active listings within that category.

- **Watchlist**
  - Signed-in users can visit a Watchlist page to view all listings they have added.
  - Clicking on any watchlisted item takes the user to that listing’s page.

## Requirements
  - Python 3.x
  - Django

## How to Run
1. **Clone the Repository**
      ```
      git clone https://github.com/sashalai64/cs50web-commerce.git
      ```
      
2. **Apply migrations**
    ```
    python manage.py makemigrations
    ```
    ```
    python manage.py migrate
    ```

4. **Create a superuser**
    ```
    python manage.py createsuperuser
    ```
   
4. **Run the Server**
      ```
      python manage.py runserver
      ```
3. **Access the Application**
   
    Visit `http://127.0.0.1:8000/` in your browser.
    
