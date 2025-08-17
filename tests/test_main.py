import pytest
import json
import sys
import os

# Add src directory to path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['message'] == 'Service is running'

def test_get_all_items(client):
    """Test retrieving all items"""
    response = client.get('/api/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 2  # Default sample items

def test_get_item_by_id(client):
    """Test retrieving a specific item by ID"""
    response = client.get('/api/items/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1
    assert data['name'] == 'Item 1'
    assert data['description'] == 'First sample item'

def test_get_nonexistent_item(client):
    """Test retrieving a non-existent item"""
    response = client.get('/api/items/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

def test_create_item(client):
    """Test creating a new item"""
    new_item = {
        'name': 'Test Item',
        'description': 'A test item description'
    }
    response = client.post('/api/items', 
                          data=json.dumps(new_item),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Item'
    assert data['description'] == 'A test item description'
    assert 'id' in data

def test_create_item_without_name(client):
    """Test creating an item without required name field"""
    invalid_item = {
        'description': 'Missing name field'
    }
    response = client.post('/api/items',
                          data=json.dumps(invalid_item),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Name is required'

def test_create_item_no_data(client):
    """Test creating an item with no data"""
    response = client.post('/api/items',
                          data='',
                          content_type='application/json')
    assert response.status_code == 400

def test_update_item(client):
    """Test updating an existing item"""
    updated_item = {
        'name': 'Updated Item',
        'description': 'Updated description'
    }
    response = client.put('/api/items/1',
                         data=json.dumps(updated_item),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Item'
    assert data['description'] == 'Updated description'
    assert data['id'] == 1

def test_update_nonexistent_item(client):
    """Test updating a non-existent item"""
    updated_item = {
        'name': 'Updated Item'
    }
    response = client.put('/api/items/999',
                         data=json.dumps(updated_item),
                         content_type='application/json')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

def test_update_item_no_data(client):
    """Test updating an item with no data"""
    response = client.put('/api/items/1',
                         data='',
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'No data provided'

def test_delete_item(client):
    """Test deleting an item"""
    response = client.delete('/api/items/2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Item deleted successfully'
    
    # Verify item is deleted
    response = client.get('/api/items/2')
    assert response.status_code == 404

def test_delete_nonexistent_item(client):
    """Test deleting a non-existent item"""
    response = client.delete('/api/items/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

def test_404_handler(client):
    """Test 404 error handler for invalid endpoints"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Endpoint not found'

def test_partial_update(client):
    """Test partial update of an item"""
    # Only update description
    partial_update = {
        'description': 'Partially updated description'
    }
    response = client.put('/api/items/1',
                         data=json.dumps(partial_update),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['description'] == 'Partially updated description'
    # Name should remain unchanged from any previous tests
    assert 'name' in data
