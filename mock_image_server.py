from flask import Flask, jsonify
import os

app = Flask(__name__)

# Mock database of vehicle images
VEHICLE_IMAGES = {
    "1731517390": [
        "https://images.kijiji.ca/api/v1/canon/images/1e/1e4b3e8c-8c5e-4b3e-8c5e-4b3e8c5e4b3e?rule=kijijica-640.jpg",
        "https://images.kijiji.ca/api/v1/canon/images/2f/2f5c4f9d-9d6f-4f9d-9d6f-4f9d9d6f4f9d?rule=kijijica-640.jpg"
    ]
}

@app.route('/v1/leads/<ad_id>/images', methods=['GET'])
def get_images(ad_id):
    images = VEHICLE_IMAGES.get(ad_id, [])
    if images:
        return jsonify({
            "status": "success",
            "ad_id": ad_id,
            "images": images
        })
    else:
        return jsonify({
            "status": "error",
            "message": "No images found for this ad_id"
        }), 404

if __name__ == '__main__':
    # Running on port 8080 as a placeholder
    app.run(host='0.0.0.0', port=8080)
