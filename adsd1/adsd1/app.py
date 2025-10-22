from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Atlas connection
app.config["MONGO_URI"] = "Add Your MangoDB token here" #Please do not ignore this
mongo = PyMongo(app)

@app.route('/')
def index():
    recipes = list(mongo.db.recipes.find())
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])  # Convert ObjectId to string
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe = {
            'name': request.form['name'],
            'cuisine_type': request.form['cuisine_type'],
            'ingredients': request.form['ingredients']
        }
        mongo.db.recipes.insert_one(recipe)
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/edit/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    if recipe:
        recipe['_id'] = str(recipe['_id'])  # Convert ObjectId to string
    if request.method == 'POST':
        updated_recipe = {
            'name': request.form['name'],
            'cuisine_type': request.form['cuisine_type'],
            'ingredients': request.form['ingredients']
        }
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$set': updated_recipe})
        return redirect(url_for('index'))
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete/<recipe_id>', methods=['GET'])
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
