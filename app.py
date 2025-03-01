from flask import Flask, request, jsonify, render_template, url_for
from flask_restx import Api, Resource, apidoc, fields
from analyze import read_image
import os

API_VERSION = "V0.1"
SERVICE_NAME = "ocr-api"


def register_custom_apidoc(app):
    """Register custom API documentation."""
    custom_apidoc = apidoc.Apidoc(
        "restx_custom_doc",
        __name__,
        template_folder="templates",
        static_folder=os.path.join(os.path.dirname(apidoc.__file__), "static"),
        static_url_path="swaggerui",
    )

    @custom_apidoc.add_app_template_global
    def swagger_static(filename):
        return url_for("restx_custom_doc.static", filename=filename)

    app.register_blueprint(custom_apidoc, url_prefix=f"/{SERVICE_NAME}/docs")


app = Flask(__name__, template_folder='templates')
api = Api(app, version=API_VERSION, title=SERVICE_NAME, description="OCR API")

image_model = api.model('Image', {
    'ImageUri': fields.String(required=True, description='Image URI')
})

@app.route("/home")
def home():
    return render_template('index.html')

# API at /api/v1/analysis/ 
@api.route("/api/v1/analysis/")
class OCRAnalysis(Resource):
    @api.expect(image_model,  validate=True)  # Expect JSON with ImageUri
    def post(self):
        try:
            data = api.payload  # Extract the JSON payload
            image_uri = data.get('ImageUri')
        except:
            return {'error': 'Missing URI in JSON'}
        # Try to get the text from the image
        try:
            res = read_image(image_uri)
            response_data = {
                "text": res
            }
            return response_data
        except:
            return {'error': 'Error in processing'}


# Register Custom API Documentation
register_custom_apidoc(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)