from flask import Blueprint, render_template, request, jsonify
from .utils import extract_text_from_pdf, analyze_resume

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('resume')
    role = request.form.get('role')
    if not file or not role:
        return jsonify({'error': 'Missing file or role'}), 400
    pdf_bytes = file.read()
    text = extract_text_from_pdf(pdf_bytes)
    result = analyze_resume(text, role)
    return jsonify(result)
