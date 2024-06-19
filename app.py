from flask import Flask, render_template, request, redirect, url_for, flash
import fingerprint

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        location = int(request.form['location'])
        if fingerprint.enroll_finger(location):
            flash('Fingerprint enrolled successfully!', 'success')
        else:
            flash('Failed to enroll fingerprint. Try again.', 'danger')
        return redirect(url_for('enroll'))
    return render_template('enroll.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if fingerprint.get_fingerprint():
            flash('Fingerprint recognized!', 'success')
        else:
            flash('Fingerprint not recognized. Try again.', 'danger')
        return redirect(url_for('verify'))
    return render_template('verify.html')

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        if 'delete' in request.form:
            location = int(request.form['location'])
            if fingerprint.delete_finger(location):
                flash('Fingerprint deleted successfully!', 'success')
            else:
                flash('Failed to delete fingerprint. Try again.', 'danger')
        return redirect(url_for('manage'))
    templates = fingerprint.get_fingerprint_templates()
    return render_template('manage.html', templates=templates)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
