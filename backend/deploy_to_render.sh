#!/bin/bash

echo "🚀 PinyImage PostgreSQL Deployment to Render"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this from the backend directory."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating template..."
    cat > .env << EOF
# Production Environment Variables
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://username:password@host:port/database
EOF
    echo "✅ Created .env template. Please update with your actual values."
fi

# Check if all required files exist
required_files=("main.py" "models.py" "config.py" "requirements.txt" "Procfile" "runtime.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file $file not found"
        exit 1
    fi
done

echo "✅ All required files present"

# Test the application locally
echo "🧪 Testing application locally..."
python test_postgresql_deployment.py

if [ $? -eq 0 ]; then
    echo "✅ Local tests passed"
else
    echo "⚠️  Local tests had issues, but continuing with deployment"
fi

# Check git status
if [ -d ".git" ]; then
    echo "📝 Git status:"
    git status --porcelain
    echo ""
    echo "💡 Make sure to commit your changes before deploying:"
    echo "   git add ."
    echo "   git commit -m 'Prepare for PostgreSQL deployment'"
    echo "   git push origin main"
else
    echo "⚠️  Not a git repository. Please initialize git and push to your repository."
fi

echo ""
echo "🎯 Next Steps for Render Deployment:"
echo "1. Go to https://render.com"
echo "2. Create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Set the following environment variables:"
echo "   - FLASK_ENV=production"
echo "   - SECRET_KEY=<generate-a-secure-secret>"
echo "   - OPENAI_API_KEY=<your-openai-api-key>"
echo "   - DATABASE_URL=<render-postgresql-url>"
echo "5. Set Build Command: pip install -r requirements.txt"
echo "6. Set Start Command: gunicorn main:app"
echo "7. Deploy!"

echo ""
echo "🔧 For PostgreSQL database:"
echo "1. Create a new PostgreSQL service on Render"
echo "2. Copy the Internal Database URL"
echo "3. Set it as DATABASE_URL environment variable"

echo ""
echo "✅ Deployment script completed!"
