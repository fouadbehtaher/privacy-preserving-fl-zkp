#!/bin/bash

echo "🚀 Setting up Privacy-Preserving Federated Learning with ZKP System..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.11"

if [ $(echo "$python_version >= $required_version" | bc -l) -eq 1 ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $required_version or higher is required"
    exit 1
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p {server,client,zkp-circuits,zkp-utils,scripts,tests,docs,docker,data/{sample_data,trained_models}}

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup ZKP circuits
echo "🔧 Setting up ZKP circuits..."
cd zkp-circuits

# Initialize Node.js project if package.json doesn't exist
if [ ! -f package.json ]; then
    npm init -y
    npm install snarkjs circomlib
fi

cd ..

# Make scripts executable
chmod +x scripts/*.sh

echo "✅ Setup completed successfully!"
echo ""
echo "📚 Next steps:"
echo "1. Review configuration files"
echo "2. Build ZKP circuits: ./scripts/build_circuits.sh"
echo "3. Run the system: ./scripts/run_system.sh"
echo "4. Check documentation: docs/ directory"
