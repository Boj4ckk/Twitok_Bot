from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """
    Renders the homepage.
    """
    return render_template('home.html', title="Home")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handles video uploads.
    """
    if request.method == 'POST':
        # Process uploaded file
        uploaded_file = request.files.get('file')
        if uploaded_file:
            file_path = f"uploads/{uploaded_file.filename}"
            uploaded_file.save(file_path)
            return redirect(url_for('home'))
    return render_template('upload.html', title="Upload Video")

if __name__ == '__main__':
    app.run(debug=True)
