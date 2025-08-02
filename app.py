from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import sqlparse
import os
from werkzeug.utils import secure_filename
from sql_analyzer import SQLAnalyzer
from sql_optimizer import SQLOptimizer
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Use environment variable

# Application Configuration
APP_CONFIG = {
    'name': 'SQL Optimizer Pro',
    'author': 'Scott Xin Shi',
    'version': '1.0.0',
    'description': 'Professional SQL query analysis and optimization tool',
    'github_url': 'https://github.com/yourusername/sql-optimizer-pro',
    'contact_email': 'scott.xin.shi@example.com',
    'linkedin_url': 'https://linkedin.com/in/yourusername'
}

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'sql', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APP_CONFIG'] = APP_CONFIG

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', config=APP_CONFIG)

@app.route('/analyze', methods=['POST'])
def analyze_sql():
    try:
        sql_content = ""
        
        # Handle file upload
        if 'sql_file' in request.files:
            file = request.files['sql_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Clean up uploaded file
                os.remove(filepath)
            else:
                return jsonify({'error': 'Invalid file type. Please upload a .sql or .txt file.'}), 400
        
        # Handle direct SQL input
        elif 'sql_text' in request.form:
            sql_content = request.form['sql_text']
        
        if not sql_content.strip():
            return jsonify({'error': 'No SQL content provided.'}), 400
        
        # Analyze SQL
        analyzer = SQLAnalyzer()
        optimizer = SQLOptimizer()
        
        # Parse and analyze
        parsed_queries = analyzer.parse_sql(sql_content)
        analysis_results = analyzer.analyze_queries(parsed_queries)
        optimization_suggestions = optimizer.generate_suggestions(analysis_results)
        
        # Format results for display
        formatted_results = {
            'queries': [],
            'summary': {
                'total_queries': len(parsed_queries),
                'issues_found': sum(len(result.get('issues', [])) for result in analysis_results),
                'optimization_score': optimizer.calculate_optimization_score(analysis_results)
            }
        }
        
        for i, (query, analysis) in enumerate(zip(parsed_queries, analysis_results)):
            formatted_results['queries'].append({
                'id': i + 1,
                'original_query': str(query),
                'formatted_query': sqlparse.format(str(query), reindent=True, keyword_case='upper'),
                'analysis': analysis,
                'suggestions': optimization_suggestions[i] if i < len(optimization_suggestions) else []
            })
        
        return jsonify(formatted_results)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        if not data or 'sql' not in data:
            return jsonify({'error': 'SQL content required in JSON format'}), 400
        
        sql_content = data['sql']
        
        analyzer = SQLAnalyzer()
        optimizer = SQLOptimizer()
        
        parsed_queries = analyzer.parse_sql(sql_content)
        analysis_results = analyzer.analyze_queries(parsed_queries)
        optimization_suggestions = optimizer.generate_suggestions(analysis_results)
        
        return jsonify({
            'analysis': analysis_results,
            'suggestions': optimization_suggestions,
            'optimization_score': optimizer.calculate_optimization_score(analysis_results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/examples')
def examples():
    return render_template('examples.html', config=APP_CONFIG)

@app.route('/about')
def about():
    return render_template('about.html', config=APP_CONFIG)

@app.route('/author')
def author():
    """Author page showcasing your work"""
    return render_template('author.html', config=APP_CONFIG)

if __name__ == '__main__':
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port) 