import sqlite3
import flask
import wtforms, flask_wtf


app = flask.Flask('Pizzeria', template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'Valentyna'

DATABASE = 'db.db'
pizzas = {
    1: "Маргарита",
    2: "Пепероні",
    3: "Чотири сира",
    4: "Гавайська",
    5: "Вегетеріанська",
}

def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(DATABASE)
    return db

def create_db():
    cr = sqlite3.connect(DATABASE)
    cr.execute('''CREATE TABLE IF NOT EXISTS order_info
            (name VARCHAR(128), order_composition VARCHAR(128), address VARCHAR(128), phone VARCHAR(32))''')
    cr.execute('''CREATE TABLE IF NOT EXISTS feedback
            (name VARCHAR(128), rating INTEGER(1), feedback VARCHAR)''')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()
@app.route('/')
@app.route('/index')
def main_page():
    return flask.render_template("main_page.html")

@app.route('/menu')
def menu():
    return flask.render_template("menu.html")

@app.route('/about_us')
def about_us():
    return flask.render_template("about_us.html")

@app.route('/order/', methods=['GET', 'POST'])
def order():
    if flask.request.method == "POST":
        name = flask.request.form.get("name")
        order_composition = flask.request.form.get("order")
        address = flask.request.form.get("address")
        phone = flask.request.form.get("phone")


        cr = get_db()
        cr.execute('INSERT INTO order_info (name, order_composition, address, phone) VALUES (?, ?, ?, ?)', (name, order_composition, address, phone))
        cr.commit()
        return flask.render_template("main_page.html")

    else:
        return flask.render_template("order.html", for_order=pizzas)

@app.route('/db')
def db():
    cr = get_db()
    cr.row_factory = sqlite3.Row
    cr = cr.cursor()
    cr.execute("SELECT * FROM order_info")
    data = cr.fetchall()
    cr.close()
    return flask.render_template("db.html", data=data)

class FeedbackForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name', validators=[wtforms.validators.DataRequired()])
    rating = wtforms.RadioField('Grade', validators=[wtforms.validators.DataRequired()])
    feedback = wtforms.StringField('Feedback')
    submit = wtforms.SubmitField('Відправити відгук')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    form.rating.choices = [('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')]
    
    if flask.request.method == "POST":
        name = form.name.data
        rating = form.rating.data[2]
        feedback = form.feedback.data

        cr = get_db()
        cr.execute('INSERT INTO feedback (name, rating, feedback) VALUES (?, ?, ?)', (name, rating, feedback))
        cr.commit()
        return flask.render_template("main_page.html")
    else:
        return flask.render_template("feedback.html", form=form)

@app.route('/feedbacks', methods=['GET', 'POST'])
def feedbacks():
    data = get_db().execute('SELECT * FROM feedback').fetchall()
    return flask.render_template("feedbacks.html", feedbacks=data)


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port='7000')