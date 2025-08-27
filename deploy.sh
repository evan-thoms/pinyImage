#!/bin/bash

echo "🚀 PinyImage Deployment Script"
echo "================================"

# Check if we're in the right directory
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Check if build was successful
if [ ! -d "frontend/build" ]; then
    echo "❌ Error: Frontend build failed"
    exit 1
fi

echo "✅ Frontend built successfully"

# Check backend dependencies
echo "🔧 Checking backend dependencies..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python test_api.py

if [ $? -eq 0 ]; then
    echo "✅ Tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi

cd ..

echo ""
echo "🎉 Setup complete! Your project is ready for deployment."
echo ""
echo "Next steps:"
echo "1. Set up your environment variables (see backend/env.example)"
echo "2. Deploy to your preferred platform:"
echo "   - Railway: Connect your GitHub repo"
echo "   - Heroku: Use 'git push heroku main'"
echo "   - Vercel: Connect your GitHub repo"
echo ""
echo "For local development:"
echo "  Backend: cd backend && python main.py"
echo "  Frontend: cd frontend && npm start"
