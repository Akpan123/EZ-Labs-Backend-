from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, ValidationError  # Added missing imports
from werkzeug.utils import secure_filename
import os
import secrets
from itsdangerous import URLSafeSerializer
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['ALLOWED_EXTENSIONS'] = {'pptx', 'docx', 'xlsx'}
app.config['OPS_CREDENTIALS'] = {'ops@example.com': 'opspassword'}

# Initialize URL serializer
serializer = URLSafeSerializer(app.config['SECRET_KEY'])

# Forms
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

    def validate_file(self, field):
        filename = field.data.filename
        if '.' not in filename or \
                filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_EXTENSIONS']:
            raise ValidationError('Only pptx, docx, and xlsx files allowed!')

class OpsLoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class ClientSignupForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    submit = SubmitField("Sign Up")

class ClientLoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    submit = SubmitField("Login")

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_file_size(path):
    """Get human-readable file size"""
    if not os.path.exists(path):
        return "0 B"
    
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"

# Context processors
@app.context_processor
def inject_global_vars():
    return {
        'current_year': datetime.now().year,
        'allowed_file': allowed_file,
        'get_file_size': get_file_size,
        'os': os,
        'UPLOAD_FOLDER': app.config['UPLOAD_FOLDER']  # Add this
    }

# Routes
@app.route('/')
def home():
    return render_template('index.html')

# Ops User Routes
@app.route('/ops/login', methods=['GET', 'POST'])
def ops_login():
    form = OpsLoginForm()
    if form.validate_on_submit():
        if form.email.data in app.config['OPS_CREDENTIALS'] and \
                form.password.data == app.config['OPS_CREDENTIALS'][form.email.data]:
            session['ops_logged_in'] = True
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('ops_login.html', form=form)

@app.route('/ops/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('ops_logged_in'):
        return redirect(url_for('ops_login'))
    
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash(f'File {filename} uploaded successfully!', 'success')
        else:
            flash('Invalid file type. Only pptx, docx, and xlsx allowed.', 'danger')
    return render_template('upload.html', form=form)

@app.route('/ops/logout')
def ops_logout():
    session.pop('ops_logged_in', None)
    return redirect(url_for('home'))

# Client User Routes
@app.route('/client/signup', methods=['GET', 'POST'])
def client_signup():
    form = ClientSignupForm()
    if form.validate_on_submit():
        # Generate encrypted verification URL
        token = serializer.dumps(form.email.data, salt='email-verify')
        verify_url = url_for('verify_email', token=token, _external=True)
        
        # In production: Send email with verify_url here
        flash(f'Verification email sent! (Demo: {verify_url})', 'info')
        return redirect(url_for('client_login'))
    return render_template('client_signup.html', form=form)

@app.route('/verify/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verify', max_age=3600)  # 1 hour expiry
        flash('Email verified successfully!', 'success')
        # In production: Update database to mark email as verified
        return redirect(url_for('client_login'))
    except:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('client_signup'))

@app.route('/client/login', methods=['GET', 'POST'])
def client_login():
    form = ClientLoginForm()
    if form.validate_on_submit():
        # In production: Check database for email
        session['client_logged_in'] = True
        session['client_email'] = form.email.data
        return redirect(url_for('list_files'))
    return render_template('client_login.html', form=form)

@app.route('/client/files')
def list_files():
    if not session.get('client_logged_in'):
        return redirect(url_for('client_login'))
    
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            files.append(filename)
    
    return render_template('files_list.html', files=files)

@app.route('/client/download/<filename>')
def download_file(filename):
    if not session.get('client_logged_in'):
        return redirect(url_for('client_login'))
    
    if allowed_file(filename):
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    flash('File type not allowed', 'danger')
    return redirect(url_for('list_files'))

@app.route('/client/logout')
def client_logout():
    session.pop('client_logged_in', None)
    session.pop('client_email', None)
    return redirect(url_for('home'))

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)