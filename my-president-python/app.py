from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search/<path:character_name>')
def search_leader(character_name):
    try:
        # Fetch from Arabic Wikipedia REST API
        wiki_url = f"https://ar.wikipedia.org/api/rest_v1/page/summary/{character_name}"
        res = requests.get(wiki_url)
        
        if res.status_code != 200:
            # Fallback to English Wikipedia if Arabic fails
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{character_name}"
            res = requests.get(wiki_url)
            
        if res.status_code != 200:
            return jsonify({"error": "لم يتم العثور على الشخصية في الأرشيف."}), 404
            
        data = res.json()
        
        # Extract image safely
        thumbnail = data.get('thumbnail')
        image_url = thumbnail.get('source') if thumbnail else "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=500&q=80"
        
        result = {
            "title": data.get('title', character_name),
            "extract": data.get('extract', 'لا توجد تفاصيل كافية متاحة حالياً.'),
            "image": image_url,
            "description": data.get('description', 'شخصية تاريخية عالمية')
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": "حدث خطأ أثناء الاتصال بأرشيف ويكيبيديا."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)