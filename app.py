"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify, make_response
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hello123'

connect_db(app)


@app.route('/')
def get_home_rt():
  '''Get home page.'''
  return render_template('home.html')

@app.route('/api/cupcakes', methods=['GET', 'POST'])
def get_or_add_cupcakes():
  '''GET all cupcakes from the database. POST a new cupcake to the database.'''
  if request.method == 'POST':
    if request.is_json:
      req = request.get_json()
      flavor = req['flavor']
      size = req['size']
      rating = req['rating']
      image = req['image']

      cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

      db.session.add(cupcake)
      db.session.commit()

      response_body = {'cupcake': {
        'id': cupcake.id,
        'flavor': flavor,
        'size' : size,
        'rating' : rating,
        'image' : image
      }}
      
      res = make_response(jsonify(response_body), 201)

      return res
    else:
      return make_response(jsonify({"message": "Request body must be JSON"}), 400)
  else:
    cupcakes = Cupcake.query.all()
    response_body = {}
    cpck_list = []

    for cupcake in cupcakes:
      cc_dict = {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
      }
      cpck_list.append(cc_dict)

    response_body['cupcakes'] = cpck_list

    res = make_response(jsonify(response_body), 200)

    return res
    

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_data(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id)

  response_body = {
    'cupcake': {
      'id': cupcake.id,
      'flavor': cupcake.flavor,
      'size': cupcake.size,
      'rating': cupcake.rating,
      'image': cupcake.image
    }
  }

  res = make_response(jsonify(response_body), 200)

  return res


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake_data(cupcake_id):
  if request.is_json:
    req = request.get_json()
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = req['flavor']
    cupcake.size = req['size']
    cupcake.rating = req['rating']
    cupcake.image = req['image']

    db.session.commit()

    response_body = {
      'cupcake': {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
        }
    }

    res = make_response(jsonify(response_body), 200)

    return res
  else:
    return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  Cupcake.query.filter(Cupcake.id == cupcake_id).delete()
  db.session.commit()

  return make_response(jsonify({"message": "Deleted"}), 200)
