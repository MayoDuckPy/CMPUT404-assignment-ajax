#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask

from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True
app.template_folder = 'static'

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    __slots__ = ['space']

    def __init__(self):
        self.clear()

    def update(self, entity, key, value):
        entry = self.space.get(entity, dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity, dict())

    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}'

myWorld = World()

@app.route("/")
def hello():
    '''Show main content'''
    return render_template('index.html')

@app.route("/entity/<entity>", methods=['POST', 'PUT'])
def update(entity):
    '''update the entities via this interface'''
    # Assumes entities don't have an enforced schema
    # Assumes request data is json-compatible
    data = request.json if request.json else {}
    if request.method == 'POST':
        myWorld.set(entity, data)
    elif request.method == 'PUT':
        for key, val in data.items():
            myWorld.update(entity, key, val)

    return data

@app.route("/world", methods=['POST', 'GET'])
def world():
    '''Return the world'''
    # No specification on handling POST and GET so just return world
    return myWorld.world()

@app.route("/entity/<entity>")
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    return myWorld.get(entity)

@app.route("/clear", methods=['POST', 'GET'])
def clear():
    '''Clear the world out!'''
    # Again, no specification on handling POST and GET so both behave the same
    myWorld.clear()
    return myWorld.world()

if __name__ == "__main__":
    app.run()
