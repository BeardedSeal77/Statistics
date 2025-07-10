# api/index.py
from flask import Flask, jsonify
from flask_cors import CORS

# Import existing routes (if any)
# from .auth.login import auth_bp
# from .diary.dashboard import dashboard_bp
# from .diary.diary import diary_bp
# from .diary.drivers import drivers_bp

# Import new statistics routes
from .routes.stats_routes import stats_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configure app
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Register existing blueprints (uncomment as needed)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(dashboard_bp)
    # app.register_blueprint(diary_bp)
    # app.register_blueprint(drivers_bp)
    
    # Register statistics blueprint
    app.register_blueprint(stats_bp)
    
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'ZealotAI Statistics API is running',
            'version': '1.0.0',
            'endpoints': {
                'statistics': '/api/statistics/',
                'help': '/api/statistics/help'
            }
        })
    
    @app.route('/api/')
    def api_root():
        return jsonify({
            'message': 'ZealotAI Statistics API',
            'version': '1.0.0',
            'available_modules': [
                'descriptive_stats',
                'normal_distribution', 
                'confidence_intervals',
                'hypothesis_testing'
            ],
            'documentation': '/api/statistics/help'
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5328)