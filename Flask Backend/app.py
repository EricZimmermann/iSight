from flask import Flask, render_template, request, redirect, url_for, jsonify, json, flash, send_from_directory, session

app = Flask(__name__)


@app.route('/')
def default():

    return render_template('base.html')


if __name__ == '__main__':
    app.run()
