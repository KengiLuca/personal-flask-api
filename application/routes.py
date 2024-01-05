from application import app, db
from flask import request, jsonify, render_template, redirect
from application.models import StarwarsCharacter
from application.forms import AddCharacterForm

def format_character(character):
    return {
        "name": character.name,
        "type": character.type,
        "catch_phrase": character.catch_phrase
    }

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# GET
@app.route("/success")
def get_sucess():
    return render_template('success.html')

# POST

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    form = AddCharacterForm()
    if form.validate_on_submit():
        character = StarwarsCharacter(form.name.data, form.type.data, form.catch_phrase.data)
        db.session.add(character)
        db.session.commit()
        return redirect('/characters')
    return render_template('submit.html', form=form)

# GET
@app.route("/characters")
def get_characters():
    characters = StarwarsCharacter.query.all()
    character_list = []
    for character in characters:
        character_list.append(format_character(character))
    return render_template('characters.html', characters=character_list)

# GET /:id
@app.route('/characters/<id>')
def get_character(id):
    # filter_by
    character = StarwarsCharacter.query.filter_by(id=id).first()
    # return jsonify(id=character.id, name=character.name, type=character.type, catch_phrase=character.catch_phrase)
    return render_template('character.html', character=format_character(character))

# DELETE /:id
@app.route("/characters/<id>", methods=['DELETE'])
def delete_character(id):
    character = StarwarsCharacter.query.filter_by(id=id).first()
    db.session.delete(character)
    db.session.commit()
    return f"Character deleted {id}"

# PATCH /:id
@app.route("/characters/<id>", methods=["PATCH"])
def update_character(id):
    character = StarwarsCharacter.query.filter_by(id=id)
    data = request.json
    character.update(dict(name=data["name"], type=data["type"], catch_phrase=data["catch_phrase"]))
    # Commit the change to the database
    db.session.commit()
    # Retrieve specific character from the filtering
    updatedCharacter = character.first()
    # Return JSON response to client 
    return jsonify(id=updatedCharacter.id, name=updatedCharacter.name, type=updatedCharacter.type, catch_phrase=updatedCharacter.catch_phrase)
