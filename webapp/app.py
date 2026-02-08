#!/usr/bin/env python3
"""
Reselling App - Web Interface
By: Buddy Dubby (Dub) 🫠

A simple web app to help Dian price and list items for resale.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
import uuid
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Simple JSON-based inventory (will upgrade to SQLite later)
INVENTORY_FILE = 'inventory.json'

def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    return {'items': []}

def save_inventory(data):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    inventory = load_inventory()
    return render_template('index.html', items=inventory['items'])

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Handle form submission
        item = {
            'id': str(uuid.uuid4())[:8],
            'name': request.form.get('name', ''),
            'brand': request.form.get('brand', ''),
            'category': request.form.get('category', ''),
            'condition': request.form.get('condition', 'good'),
            'color': request.form.get('color', ''),
            'size': request.form.get('size', ''),
            'measurements': request.form.get('measurements', ''),
            'cost': float(request.form.get('cost', 0) or 0),
            'floor_price': float(request.form.get('floor_price', 0) or 0),
            'target_price': float(request.form.get('target_price', 0) or 0),
            'notes': request.form.get('notes', ''),
            'photos': [],
            'status': 'unlisted',
            'created_at': datetime.now().isoformat(),
            'platforms': []
        }
        
        # Handle photo upload
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo.filename:
                    filename = f"{item['id']}_{uuid.uuid4().hex[:6]}_{photo.filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    photo.save(filepath)
                    item['photos'].append(filename)
        
        # Save to inventory
        inventory = load_inventory()
        inventory['items'].append(item)
        save_inventory(inventory)
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/item/<item_id>')
def view_item(item_id):
    inventory = load_inventory()
    item = next((i for i in inventory['items'] if i['id'] == item_id), None)
    if not item:
        return "Item not found", 404
    return render_template('item.html', item=item)

@app.route('/item/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    inventory = load_inventory()
    item_idx = next((i for i, item in enumerate(inventory['items']) if item['id'] == item_id), None)
    
    if item_idx is None:
        return "Item not found", 404
    
    if request.method == 'POST':
        item = inventory['items'][item_idx]
        item['name'] = request.form.get('name', item['name'])
        item['brand'] = request.form.get('brand', item['brand'])
        item['category'] = request.form.get('category', item['category'])
        item['condition'] = request.form.get('condition', item['condition'])
        item['color'] = request.form.get('color', item.get('color', ''))
        item['size'] = request.form.get('size', item.get('size', ''))
        item['measurements'] = request.form.get('measurements', item.get('measurements', ''))
        item['cost'] = float(request.form.get('cost', 0) or 0)
        item['floor_price'] = float(request.form.get('floor_price', 0) or 0)
        item['target_price'] = float(request.form.get('target_price', 0) or 0)
        item['notes'] = request.form.get('notes', item['notes'])
        item['status'] = request.form.get('status', item['status'])
        
        save_inventory(inventory)
        return redirect(url_for('view_item', item_id=item_id))
    
    return render_template('edit.html', item=inventory['items'][item_idx])

@app.route('/item/<item_id>/delete', methods=['POST'])
def delete_item(item_id):
    inventory = load_inventory()
    inventory['items'] = [i for i in inventory['items'] if i['id'] != item_id]
    save_inventory(inventory)
    return redirect(url_for('index'))

@app.route('/tools')
def tools():
    """Tools page - background remover, price checker, etc."""
    return render_template('tools.html')

@app.route('/api/price-check', methods=['POST'])
def price_check():
    """API endpoint to check prices across platforms"""
    from price_scraper import generate_price_recommendation
    
    data = request.json
    query = data.get('query', '')
    brand = data.get('brand', '')
    condition = data.get('condition', 'good')
    retail_price = data.get('retail_price')
    item_cost = data.get('item_cost', 0)
    
    # Convert to float if provided
    if retail_price:
        retail_price = float(retail_price)
    if item_cost:
        item_cost = float(item_cost)
    
    # Get recommendation
    result = generate_price_recommendation(
        item_name=query,
        brand=brand,
        condition=condition,
        retail_price=retail_price,
        item_cost=item_cost
    )
    
    # Format for frontend
    estimates = result['estimates']
    platforms = result['platforms']
    
    response = {
        'query': query,
        'estimates': {
            platform: {
                'low': platforms[platform]['quick_sale']['net_payout'],
                'high': platforms[platform]['max_value']['net_payout'],
                'avg': platforms[platform]['fair_price']['net_payout'],
                'profit': platforms[platform]['fair_price']['profit']
            }
            for platform in ['poshmark', 'depop', 'mercari', 'ebay']
        },
        'recommendation': {
            'quick_sale': estimates['quick_sale'],
            'fair_price': estimates['fair_price'],
            'max_value': estimates['max_value']
        },
        'tip': result['recommendation']
    }
    
    return jsonify(response)

@app.route('/api/inventory')
def api_inventory():
    """API endpoint to get all inventory"""
    return jsonify(load_inventory())

@app.route('/api/generate-description', methods=['POST'])
def generate_description_api():
    """API endpoint to generate listing descriptions"""
    from description_generator import generate_description
    
    data = request.json
    
    result = generate_description(
        name=data.get('name', ''),
        brand=data.get('brand', ''),
        category=data.get('category', ''),
        condition=data.get('condition', 'good'),
        color=data.get('color', ''),
        size=data.get('size', ''),
        measurements=data.get('measurements', ''),
        notes=data.get('notes', '')
    )
    
    return jsonify(result)

@app.route('/api/remove-background', methods=['POST'])
def remove_background_api():
    """API endpoint to remove background from uploaded image"""
    from background_remover import remove_background_bytes, add_white_background
    from PIL import Image
    import io
    import base64
    
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    try:
        # Read image bytes
        image_bytes = file.read()
        
        # Remove background
        transparent_bytes = remove_background_bytes(image_bytes)
        
        # Create white background version
        transparent_img = Image.open(io.BytesIO(transparent_bytes))
        white_bg_img = add_white_background(transparent_img)
        
        # Convert to bytes
        white_buf = io.BytesIO()
        white_bg_img.save(white_buf, format='JPEG', quality=95)
        white_bytes = white_buf.getvalue()
        
        # Save to uploads folder
        original_name = Path(file.filename).stem
        
        # Save transparent version
        transparent_filename = f"{original_name}_transparent_{uuid.uuid4().hex[:6]}.png"
        transparent_path = os.path.join(app.config['UPLOAD_FOLDER'], transparent_filename)
        with open(transparent_path, 'wb') as f:
            f.write(transparent_bytes)
        
        # Save white bg version
        white_filename = f"{original_name}_white_{uuid.uuid4().hex[:6]}.jpg"
        white_path = os.path.join(app.config['UPLOAD_FOLDER'], white_filename)
        with open(white_path, 'wb') as f:
            f.write(white_bytes)
        
        return jsonify({
            "success": True,
            "transparent": {
                "filename": transparent_filename,
                "url": f"/uploads/{transparent_filename}"
            },
            "white_bg": {
                "filename": white_filename,
                "url": f"/uploads/{white_filename}"
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/item/<item_id>/remove-bg/<photo_index>', methods=['POST'])
def remove_bg_for_item(item_id, photo_index):
    """Remove background from a specific item photo"""
    from background_remover import process_product_photo
    
    inventory = load_inventory()
    item = next((i for i in inventory['items'] if i['id'] == item_id), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    try:
        photo_idx = int(photo_index)
        if photo_idx >= len(item.get('photos', [])):
            return jsonify({"error": "Photo not found"}), 404
        
        photo_filename = item['photos'][photo_idx]
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        
        if not os.path.exists(photo_path):
            return jsonify({"error": "Photo file not found"}), 404
        
        # Process the photo
        result = process_product_photo(photo_path, app.config['UPLOAD_FOLDER'])
        
        # Add processed photos to item
        transparent_name = os.path.basename(result['transparent'])
        white_name = os.path.basename(result['white_bg'])
        
        if 'processed_photos' not in item:
            item['processed_photos'] = []
        
        item['processed_photos'].append({
            "original": photo_filename,
            "transparent": transparent_name,
            "white_bg": white_name
        })
        
        save_inventory(inventory)
        
        return jsonify({
            "success": True,
            "transparent": f"/uploads/{transparent_name}",
            "white_bg": f"/uploads/{white_name}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory('static', filename)

@app.route('/favicon.ico')
def favicon():
    from flask import send_from_directory
    return send_from_directory('static', 'icon.svg', mimetype='image/svg+xml')

if __name__ == '__main__':
    print("🫠 Dub's Reselling App")
    print("=" * 40)
    print("Starting server at http://localhost:5050")
    app.run(debug=True, port=5050, host='0.0.0.0')
