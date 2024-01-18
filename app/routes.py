from app import app, model, books, ratings, matrix

@app.route('/popular', methods=['GET'])
def popular():
    '''
    Returns top 6 most purchased books
    '''
    book_ratings_count = ratings.groupby('ISBN').count()
    book_ratings_count = book_ratings_count[book_ratings_count['User-ID'] >= 24].sort_values(by='User-ID', ascending=False)

    popular_books = books[books['ISBN'].isin(book_ratings_count.head(6).index)]

    return popular_books.to_json(orient='records')


@app.route('/highest-rated', methods=['GET'])
def highest_rated():
    '''
    Returns top 6 highest rated books
    '''
    ratings_count = ratings.groupby('ISBN').count()
    ratings_count = ratings_count[ratings_count['User-ID'] >= 24]
    book_ratings = ratings[ratings['ISBN'].isin(ratings_count.index)]
    book_ratings = book_ratings.groupby('ISBN').mean().sort_values(by='Book-Rating', ascending=False)

    highest_rated_books = books[books['ISBN'].isin(book_ratings.head(6).index)]

    return highest_rated_books.to_json(orient='records')


@app.route('/book/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    '''
    Returns a single book with rating by ISBN 
    '''    
    selected_book = books[books['ISBN'] == isbn]

    return selected_book.head(1).to_json(orient='records')


@app.route('/recommendations/<isbn>', methods=['GET'])
def get_recommendations(isbn):
    '''
    Returns 6 book recommendations
    '''
    book = matrix[matrix.index == isbn].values
    
    if book.size == 0:
        return []

    _, neigh_ind = model.kneighbors(book)

    matrix_indexes = []
    for i in neigh_ind[0]:
        if matrix.index[i] != isbn:
            matrix_indexes.append(matrix.index[i])

    recommendations = books[books['ISBN'].isin(matrix_indexes)]

    return recommendations.to_json(orient='records')


@app.route('/search/<str>', methods=['GET'])
def search(str):
    '''
    Returns first 50 results that contain the string
    '''
    results = books[books['Book-Title'].str.contains(str, case=False)]

    return results.head(50).to_json(orient='records')
