from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_data().decode('utf-8')
        print(f"Signal received: {data}")
       
        if data in ['BUY', 'SELL', 'LONG', 'SHORT']:
            return jsonify({'success': True, 'message': f'Signal {data} processed'})
        else:
            return jsonify({'success': False, 'message': 'Invalid signal'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/')
def home():
    return "TradingView Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
