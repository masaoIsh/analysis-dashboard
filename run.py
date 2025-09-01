#!/usr/bin/env python3
"""
Simple startup script for the Notebook Dashboard
"""

from app import app

if __name__ == '__main__':
    print("🚀 Starting Notebook Dashboard...")
    print("📱 Open your browser and go to: http://localhost:5001")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Use port 5001 since 5000 is often busy on macOS
        print("⚠️  Using port 5001 to avoid conflicts with macOS AirPlay")
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
