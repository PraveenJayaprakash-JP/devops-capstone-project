from flask import Flask, jsonify, request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Sample data for demonstration
items = [
    {"id": 1, "name": "Item 1", "description": "First sample item"},
    {"id": 2, "name": "Item 2", "description": "Second sample item"}
]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Service is running"}), 200

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    logger.info("GET /api/items - Retrieving all items")
    return jsonify({"items": items}), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    logger.info(f"GET /api/items/{item_id} - Retrieving item with ID {item_id}")
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_id = max([item["id"] for item in items]) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": data["name"],
        "description": data.get("description", "")
    }
    items.append(new_item)
    logger.info(f"POST /api/items - Created new item with ID {new_id}")
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    logger.info(f"PUT /api/items/{item_id} - Updated item")
    return jsonify(item), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    global items
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    items = [item for item in items if item["id"] != item_id]
    logger.info(f"DELETE /api/items/{item_id} - Deleted item")
    return jsonify({"message": "Item deleted successfully"}), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
