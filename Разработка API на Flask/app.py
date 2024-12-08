from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Хранилище данных (вместо базы данных)
users = {}
posts = {}
user_id_counter = 1
post_id_counter = 1

# Создание пользователя
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json
    username = data.get('username')
    email = data.get('email')

    if username in users:
        return jsonify({'error': 'Имя пользователя уже существует.'}), 400

    user_id = user_id_counter
    users[username] = {'id': user_id, 'username': username, 'email': email}
    user_id_counter += 1

    return jsonify({'message': 'Пользователь создан.', 'user_id': user_id}), 201

# Получение списка пользователей
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

# Получение пользователя по ID
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users.values():
        if user['id'] == user_id:
            return jsonify(user), 200
    abort(404)

# Создание поста
@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    global post_id_counter
    data = request.json
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')

    # Проверка существования пользователя
    if not any(user['id'] == user_id for user in users.values()):
        return jsonify({'error': 'Пользователь не найден.'}), 400

    post_id = post_id_counter
    posts[post_id] = {'id': post_id, 'user_id': user_id, 'title': title, 'content': content}
    post_id_counter += 1

    return jsonify({'message': 'Пост создан.', 'post_id': post_id}), 201

# Получение списка постов
@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    return jsonify(list(posts.values())), 200

# Получение поста по ID
@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    if post_id in posts:
        return jsonify(posts[post_id]), 200
    abort(404)

# Обновление поста
@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    if post_id not in posts:
        abort(404)

    data = request.json
    title = data.get('title')
    content = data.get('content')

    if title:
        posts[post_id]['title'] = title
    if content:
        posts[post_id]['content'] = content

    return jsonify({'message': 'Пост обновлен.'}), 200

# Удаление поста
@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if post_id in posts:
        del posts[post_id]
        return jsonify({'message': 'Пост удален.'}), 204
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)