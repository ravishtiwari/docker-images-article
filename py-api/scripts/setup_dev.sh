
#!/bin/bash

# Development environment setup script

echo "Setting up IMDb API Development Environment"
echo "=========================================="

# Check if Python 3.11+ is available
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
pip install pytest-cov black isort flake8 mypy

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Make scripts executable
chmod +x scripts/*.sh

echo ""
echo "=========================================="
echo "Development environment setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start PostgreSQL with pgvector extension"
echo "3. Run: source venv/bin/activate"
echo "4. Run: alembic upgrade head"
echo "5. Run: uvicorn main:app --reload"
echo ""
echo "Or use Docker:"
echo "docker-compose up -d"
