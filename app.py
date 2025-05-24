from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simple log list to store recent signals
recent_signals = []

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get raw data
        raw_data = request.get_data()
        data = raw_data.decode('utf-8').strip()
       
        # Parse signal
        signal_type = None
        if data.upper() in ['BUY', 'LONG']:
            signal_type = 'BUY'
        elif data.upper() in ['SELL', 'SHORT']:
            signal_type = 'SELL'
        else:
            try:
                json_data = json.loads(data)
                action = json_data.get('action', '').upper()
                if action in ['BUY', 'LONG']:
                    signal_type = 'BUY'
                elif action in ['SELL', 'SHORT']:
                    signal_type = 'SELL'
            except:
                pass
       
        # Log signal
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        signal_log = {
            'timestamp': timestamp,
            'signal': signal_type,
            'raw_data': data
        }
       
        recent_signals.append(signal_log)
        if len(recent_signals) > 10:  # Keep only last 10
            recent_signals.pop(0)
       
        print(f"[{timestamp}] Signal received: {signal_type} | Raw: {data}")
       
        if signal_type:
            return jsonify({
                'success': True,
                'message': f'Signal {signal_type} processed successfully',
                'timestamp': timestamp
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid signal format',
                'received': data
            })
           
    except Exception as e:
        error_msg = f"Webhook error: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({'success': False, 'message': error_msg})

@app.route('/')
def home():
    return "TradingView Webhook Server is running!"

@app.route('/status')
def status():
    return jsonify({
        'status': 'running',
        'recent_signals': recent_signals,
        'total_signals': len(recent_signals)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
