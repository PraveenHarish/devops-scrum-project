from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "responses.db"


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def init_db():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# ABOUT PAGE
# ==========================================

@app.route("/about")
def about():

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>About - DevOps Project</title>

        <style>
            body {
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #070b14;
                color: white;
                font-family: Arial, sans-serif;
            }

            .about-box {
                width: 90%;
                max-width: 700px;
                padding: 50px;
                background: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            }

            h1 {
                color: #38bdf8;
                margin-bottom: 20px;
            }

            p {
                color: #94a3b8;
                line-height: 1.8;
                font-size: 16px;
            }

            a {
                display: inline-block;
                margin-top: 25px;
                padding: 12px 22px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }

            a:hover {
                background: #1d4ed8;
            }
        </style>
    </head>

    <body>

        <div class="about-box">

            <h1>About the Application</h1>

            <p>
                This is a DevOps demonstration project developed using
                Python and Flask.
            </p>

            <p>
                The project demonstrates Git version control,
                GitHub branching and pull requests, automated testing
                using GitHub Actions, CI/CD practices and cloud deployment
                using Vercel.
            </p>

            <p>
                The application also demonstrates the concept of migrating
                a monolithic application towards a microservices architecture.
            </p>

            <a href="/">← Back to Home</a>

        </div>

    </body>
    </html>
    """


# ==========================================
# SUBMIT RESPONSE
# ==========================================

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    # Check empty fields
    if not name or not email or not message:

        return "All fields are required.", 400

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO responses
        (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    connection.commit()

    connection.close()

    return redirect(url_for("success"))


# ==========================================
# SUCCESS PAGE
# ==========================================

@app.route("/success")
def success():

    return render_template("success.html")


# ==========================================
# VIEW RESPONSES
# ==========================================

@app.route("/responses")
def responses():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, message
        FROM responses
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return render_template(
        "responses.html",
        responses=data
    )


# ==========================================
# DELETE ONE RESPONSE
# ==========================================

@app.route("/delete/<int:response_id>", methods=["POST"])
def delete_response(response_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM responses
        WHERE id = ?
    """, (response_id,))

    connection.commit()

    connection.close()

    return redirect(url_for("responses"))


# ==========================================
# DELETE ALL RESPONSES
# ==========================================

@app.route("/delete-all", methods=["POST"])
def delete_all():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM responses")

    connection.commit()

    connection.close()

    return redirect(url_for("responses"))


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return {
        "status": "healthy"
    }


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)