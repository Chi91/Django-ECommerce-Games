# Online Shop for Games - README

## Project Description

This online shop for games provides users with a platform to browse and purchase a variety of games. The key features include:

### Product Catalog
- **Free Selection of Products:** Users can browse and select from a variety of games.
- **Product Details:** Each game is displayed with a name, a text description, images, and a price.
- **Product Info PDF:** Each game has an additional PDF file with more information available for download.

### User Profile
- **Profile Picture:** Users can upload and display their profile picture.

### Search Functionality
- **Advanced Search:** Users can search by product name, product description, and review stars.

### Customer Service Portal
- **Additional to Django Admin Portal:** A special portal for customer service.
- **Product Management:** Customer service staff can add games with images and PDFs and edit product details.
- **Review Management:** Customer service staff can deactivate or delete reviews, either via a separate page or through additional buttons on the main page.

### Product Reviews
- **Submit Reviews:** Users can submit one review per game, consisting of text and stars (1 to 5).
- **Mark Reviews:** Reviews can be marked as helpful or not helpful. Users can report inappropriate reviews.
- **Edit/Delete Reviews:** Users can edit or delete their own reviews.

### Shopping Cart
- **Save Products:** Users can save games and their quantities in a shopping cart.
- **Payment Functionality:** The functionality for payment is not implemented.

### Deployment
- **Hosting:** The web application is hosted on an online platform like PythonAnywhere, making it available on the internet and not just locally on a laptop.

## Installation and Usage
   git clone [<repository-url>](https://github.com/Chi91/Django-ECommerce-Games.git)

   pip install -r requirements.txt

   python manage.py migrate

   python manage.py runserver

### Hosting on PythonAnywhere
Create an account on PythonAnywhere.
Follow the documentation for deploying a Django app on PythonAnywhere.

### Contributors
 - Chi Thien Pham
 - Jakob Raabe 
 - Maurice Schembecker

