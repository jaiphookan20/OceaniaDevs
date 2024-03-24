from flask import Flask, render_template, request
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-seeker', methods=['GET', 'POST'])
def add_seeker():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        email_id = request.form['email_id']
        
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()
            
            query = """
                INSERT INTO seekers (fname, lname, city, state, country, email_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (fname, lname, city, state, country, email_id)
            
            cur.execute(query, values)
            conn.commit()
            
            cur.close()
            conn.close()
            
            return "Job Seeker added successfully"
        
        except psycopg2.Error as e:
            print(f"Error inserting seeker: {e}")
            return "An error occurred while adding the seeker"
    
    return render_template('add_seeker.html')

if __name__ == '__main__':
    app.run(debug=True)