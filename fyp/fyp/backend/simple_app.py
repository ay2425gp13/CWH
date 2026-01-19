from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/pc-builder', methods=['POST'])
def pc_builder():
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"success": False, "message": "Message is required"}), 400

    try:
        # Mock response for testing
        message_lower = user_message.lower()
        if 'cpu' in message_lower or 'processor' in message_lower:
            mock_responses = [
                "For gaming, the best CPU options in your budget range would be:\n\n1. AMD Ryzen 7 7700X (~$350) - Excellent for gaming and multitasking\n2. Intel Core i7-13700K (~$400) - Great performance for high-end gaming\n3. AMD Ryzen 5 7600X (~$250) - Best value for 1440p gaming\n\nConsider your budget and whether you need integrated graphics.",
                "For a 3000 HKD (~$385 USD) budget focused on CPU for gaming:\n\n- AMD Ryzen 5 7600X: ~$250 - Best balance of performance and price\n- Intel Core i5-13600K: ~$320 - Slightly better gaming performance\n\nPair with a good GPU for optimal gaming experience.",
                "CPU recommendations for gaming:\n\nBudget (~$200-300):\n- AMD Ryzen 5 7600: ~$200\n- Intel Core i5-12400: ~$180\n\nMid-range (~$300-400):\n- AMD Ryzen 5 7600X: ~$250\n- Intel Core i5-13600K: ~$320\n\nHigh-end (~$400+):\n- AMD Ryzen 7 7700X: ~$350\n- Intel Core i7-13700K: ~$400"
            ]
        elif 'gpu' in message_lower or 'graphics' in message_lower or 'video card' in message_lower:
            mock_responses = [
                "Best GPU options for gaming:\n\nBudget (~$200-300):\n- NVIDIA RTX 4060: ~$300\n- AMD RX 7600: ~$250\n\nMid-range (~$400-500):\n- NVIDIA RTX 4070: ~$550\n- AMD RX 7800 XT: ~$450\n\nHigh-end (~$600+):\n- NVIDIA RTX 4070 Ti: ~$750\n- NVIDIA RTX 4080: ~$1000+",
                "For 1440p gaming, I recommend:\n\n- NVIDIA RTX 4070 (~$550) - Excellent 1440p performance\n- AMD RX 7800 XT (~$450) - Great value alternative\n- NVIDIA RTX 4060 Ti (~$450) - Good entry point\n\nMake sure your PSU can handle the power requirements.",
                "GPU recommendations:\n\nEntry level: RTX 4060 (~$300)\nMid-range: RTX 4070 (~$550)\nHigh-end: RTX 4070 Ti (~$750)\n\nConsider your monitor resolution and desired FPS target."
            ]
        elif 'ram' in message_lower or 'memory' in message_lower:
            mock_responses = [
                "RAM recommendations for gaming:\n\nMinimum: 16GB DDR4-3200 (~$60)\nRecommended: 16GB DDR5-5600 (~$80)\nHigh-end: 32GB DDR5-5600 (~$140)\n\nDDR5 offers better future-proofing, but DDR4 is still excellent for gaming.",
                "For gaming PCs:\n\n- 16GB DDR4-3200: ~$60 (minimum for modern gaming)\n- 16GB DDR5-5600: ~$80 (recommended)\n- 32GB DDR5-5600: ~$140 (for content creation)\n\nAlways get at least dual-channel (2 sticks).",
                "Memory recommendations:\n\nGaming: 16GB DDR4/DDR5\nContent creation: 32GB DDR5\n\nSpeed: 3200MHz+ for DDR4, 5200MHz+ for DDR5\n\nBrand: Corsair, G.Skill, or Kingston are reliable."
            ]
        else:
            mock_responses = [
                "For a gaming PC under 3000 HKD (~$385 USD), here's a balanced build:\n\n- CPU: AMD Ryzen 5 7600X (~$250)\n- GPU: NVIDIA RTX 4060 (~$300)\n- Motherboard: B650 (~$150)\n- RAM: 16GB DDR5 (~$80)\n- Storage: 1TB NVMe SSD (~$100)\n- PSU: 650W 80+ Bronze (~$80)\n- Case: Mid-tower (~$80)\n\nTotal: ~$1100. This will handle 1080p/1440p gaming well.",
                "Here's a solid gaming PC build for ~3000 HKD:\n\n- AMD Ryzen 5 7600X: ~$250\n- NVIDIA RTX 4060: ~$300\n- B650 motherboard: ~$150\n- 16GB DDR5 RAM: ~$80\n- 1TB NVMe SSD: ~$100\n- 650W PSU: ~$80\n- Mid-tower case: ~$80\n\nTotal: ~$1100. Great for 1440p gaming at high settings.",
                "Budget gaming PC build (~3000 HKD):\n\n- CPU: Ryzen 5 7600X (~$250)\n- GPU: RTX 4060 (~$300)\n- Motherboard: B650 (~$150)\n- RAM: 16GB DDR5 (~$80)\n- Storage: 1TB SSD (~$100)\n- PSU: 650W (~$80)\n- Case: ~$80\n\nTotal: ~$1100. Will run most games at 1440p with good performance."
            ]

        ai_response = random.choice(mock_responses)
        return jsonify({"success": True, "response": ai_response})

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5001)