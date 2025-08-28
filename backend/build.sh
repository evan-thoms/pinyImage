#!/bin/bash

echo "🔧 PinyImage PostgreSQL Migration Build Script"
echo "=============================================="

# Force Python 3.11
echo "🐍 Setting up Python 3.11..."
python3.11 --version || {
    echo "❌ Python 3.11 not available, installing..."
    # This will fail on Render but we'll handle it
}

# Use Python 3.11 if available, otherwise use system Python
PYTHON_CMD="python3"
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Using Python 3.11"
else
    echo "⚠️  Using system Python: $(python3 --version)"
fi

# Check Python version
python_version=$($PYTHON_CMD --version)
echo "🐍 Python version: $python_version"

# Force install dependencies with specific versions
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt --force-reinstall --no-cache-dir

# Verify SQLAlchemy installation
echo "🔍 Verifying SQLAlchemy..."
$PYTHON_CMD -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"

# Test imports
echo "🧪 Testing imports..."
$PYTHON_CMD -c "
try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from models import db, User, Card
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

echo "✅ Build completed successfully"
