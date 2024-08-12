import http.server
import socketserver
import json

# Datasets with name and price in rupees
home_appliances = [
    {"name": "Washing Machine", "category": "Laundry", "price": 50000},
    {"name": "Refrigerator", "category": "Cooling", "price": 80000},
    {"name": "Microwave Oven", "category": "Cooking", "price": 15000},
    {"name": "Dishwasher", "category": "Cleaning", "price": 30000},
    {"name": "Air Conditioner", "category": "Cooling", "price": 60000},
    {"name": "Vacuum Cleaner", "category": "Cleaning", "price": 20000}
]

fruits = [
    {"name": "Apple", "category": "Fruit", "price": 80},
    {"name": "Banana", "category": "Fruit", "price": 40},
    {"name": "Orange", "category": "Fruit", "price": 100},
    {"name": "Mango", "category": "Fruit", "price": 120},
    {"name": "Strawberry", "category": "Fruit", "price": 200},
    {"name": "Grapes", "category": "Fruit", "price": 300}
]

vegetables = [
    {"name": "Carrot", "category": "Vegetable", "price": 60},
    {"name": "Broccoli", "category": "Vegetable", "price": 150},
    {"name": "Spinach", "category": "Vegetable", "price": 200},
    {"name": "Potato", "category": "Vegetable", "price": 50},
    {"name": "Tomato", "category": "Vegetable", "price": 100},
    {"name": "Cucumber", "category": "Vegetable", "price": 120}
]

# Combined dataset for search
datasets = {
    "home_appliances": home_appliances,
    "fruits": fruits,
    "vegetables": vegetables
}

def search_dataset(query):
    results = []
    for category, items in datasets.items():
        matched_items = [item for item in items if query.lower() in item['name'].lower()]
        for item in matched_items:
            results.append({**item, "category": category})
    return results

def find_s_algorithm(search_term):
    positive_examples = []
    for category, items in datasets.items():
        for item in items:
            if search_term.lower() in item['name'].lower():
                positive_examples.append(item)
    
    if not positive_examples:
        return []
    
    specific_hypothesis = {key: positive_examples[0].get(key) for key in positive_examples[0] if key != 'name'}

    recommendations = []
    for category, items in datasets.items():
        for item in items:
            if (item['category'] == specific_hypothesis['category']) and (item['name'].lower() != search_term.lower()):
                recommendations.append(item)
    
    return recommendations

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path.startswith('/search'):
            parts = self.path.split('?')
            if len(parts) > 1:
                params = parts[1].split('=')
                query = params[1] if len(params) > 1 else ""
                result = search_dataset(query)
                self._set_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))

        elif self.path.startswith('/recommend'):
            parts = self.path.split('?')
            if len(parts) > 1:
                params = parts[1].split('=')
                item_name = params[1] if len(params) > 1 else ""
                recommendations = find_s_algorithm(item_name)
                self._set_headers()
                self.wfile.write(json.dumps(recommendations).encode('utf-8'))

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

PORT = 8000

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
