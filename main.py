from flask import Flask, jsonify, send_file
import os
import random

app = Flask(__name__)

sent_books = {}

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/getRandomBook/<category>')
def get_random_book(category):
    file_path = f'{category.lower()}.txt'

    try:
        with open(file_path, 'r') as file:
            books = file.read().split('\n')

            available_books = [book for book in books if not sent_books.get(book)]

            if not available_books:
                return jsonify({'error': 'No more books available in this category.'}), 404
            else:
                random_book = random.choice(available_books)
                sent_books[random_book] = True
                return jsonify({'book': random_book})
    except FileNotFoundError:
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
