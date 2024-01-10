from app import app, model
import pandas

@app.route('/popular', methods=['GET'])
def popular():
    '''
    Returns top 6 most purchased books
    '''
    books = pandas.read_pickle('books')
    ratings = pandas.read_pickle('ratings')

    book_ratings_count = ratings.groupby('ISBN').count()
    book_ratings_count = book_ratings_count[book_ratings_count['User-ID'] >= 24].sort_values(by='User-ID', ascending=False)

    books = books[books['ISBN'].isin(book_ratings_count.head(6).index)]

    return books.to_json(orient='records')


@app.route('/highest-rated', methods=['GET'])
def highest_rated():
    '''
    Returns top 6 highest rated books
    '''
    books = pandas.read_pickle('books')
    ratings = pandas.read_pickle('ratings')

    ratings_count = ratings.groupby('ISBN').count()
    ratings_count = ratings_count[ratings_count['User-ID'] >= 24]
    book_ratings = ratings[ratings['ISBN'].isin(ratings_count.index)]
    book_ratings = book_ratings.groupby('ISBN').mean().sort_values(by='Book-Rating', ascending=False)

    books = books[books['ISBN'].isin(book_ratings.head(6).index)]

    return books.to_json(orient='records')


@app.route('/book/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    '''
    Returns a single book with rating by ISBN 
    '''
    books = pandas.read_pickle('books')
    ratings = pandas.read_pickle('ratings')
    
    books = books[books['ISBN'] == isbn]
    ratings = ratings[ratings['ISBN'].isin(books['ISBN'])]
    ratings_count = [ratings.size]

    if ratings_count[0] != 0:
        ratings = ratings.groupby('ISBN').mean().round(1)
        average_book_rating = [ratings['Book-Rating'].values[0]]
        books['Average-Book-Rating'] = average_book_rating
        books['Ratings-Count'] = ratings_count
    else:
        books['Average-Book-Rating'] = 0
        books['Ratings-Count'] = 0

    return books.head(1).to_json(orient='records')


@app.route('/recommendations/<isbn>', methods=['GET'])
def get_recommendations(isbn):
    '''
    Returns 6 book recommendations
    '''
    books = pandas.read_pickle('books')
    matrix = pandas.read_pickle('matrix')

    book = matrix[matrix.index == isbn].values
    
    if book.size == 0:
        return []

    _, neigh_ind = model.kneighbors(book)

    matrix_indexes = []
    for i in neigh_ind[0]:
        if matrix.index[i] != isbn:
            matrix_indexes.append(matrix.index[i])

    books = books[books['ISBN'].isin(matrix_indexes)]

    return books.to_json(orient='records')


@app.route('/search/<str>', methods=['GET'])
def search(str):
    '''
    Returns first 50 results that contain the string
    '''
    books = pandas.read_pickle('books')

    books = books[books['Book-Title'].str.contains(str, case=False)]

    return books.head(50).to_json(orient='records')
