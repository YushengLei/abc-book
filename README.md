#### About The Project

Web console for easier management of ABC Book's users and borrowing/returning of books.
(Backend only)

### Prerequisites
Flask              2.2.2
pip                22.3.1
pymongo            4.3.3
python             3.7.4

#### Clone the repo
git clone https://github.com/YushengLei/abc-book.git

#### How to Run
python app.py to start the web application, using virtual environment if possible

CRUD of book/user objects (Can be ran using Postman or any other API access):
localhost/books
Fields: title (string), description(string), genre(string), author(string), yearPublished(string), availStatus (bool), lastBorrower(string)

localhost/users
Fields: name(string), role(int), dateJoined(string)
for Role field: 0 - admin, 1 - editor, 2 - user

#### Example
localhost/users (POST)
field: name - yu, role - 1
```
{
    "message": "user created",
    "id": "6396e64f6f1221d68f49c212"
}
```
localhost/users (GET)
```
[
    {
        "_id": "6396e64f6f1221d68f49c212",
        "name": "yu",
        "role": 1,
        "dateJoined": [
            "12/12/2022"
        ]
    }
]
```
#### Structure
Project structure is simply split into frontend and backend component for now. Since project is quite small. The templates/html files are for frontend purposes which are not involved in this project yet.

#### How I designed the APIs
APIs are written in python flash, with CRUD for both users and books. GET method is used for reading, POST method for creation of objects, PATCH method for updating, DELETE method for deleting objects.
Example: users/<idx> (DELETE) to remove user, books/<idx> (PATCH) to edit selected book

Data formats are written in json.

For borrowing and returning of books, they are written in /return<idx> and /borrow/<idx>  respectively. The boolean availStatus is set to True/False respectively when successfully borrowed/returned

Code implementation
Code is writte in python flask, using relavant libraries such as pymongo and json for backend operations.

#### Scalability

-Books are assumed to be in small numbers hence duplicates are counted as separate objects. If the same copies of books are to be in large number, new field can be added to count the book in one entry instead of separating them
-PATCH method is currently used as it is assumed borrowing/returning of books is sure to edit the current existing book. For future considerations (e.g donation of books), PUT method may be used instead for editing fields that may have been empty before.
-breaking down app.py into different packages when the code base is to be expanded (authentication added etc.)

#### License
Distributed under the XXX License. See LICENSE.txt for more information.

#### Contact
Lei Yusheng - leoleiyusheng@gmail.com

Project Link: https://github.com/YushengLei/abc-book
