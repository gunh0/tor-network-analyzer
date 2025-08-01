# Tor Anonymous Network Analysis

A comprehensive tool for analyzing Tor hidden services (.onion sites) with enhanced testing capabilities and detailed result reporting.

## 🚀 Features

- **🎯 Simple Execution**: Easy-to-use Makefile commands
- **📊 Web Dashboard**: Beautiful results viewer with charts and statistics
- **🔄 Independent Services**: Separate analysis and viewer containers
- **🧪 Built-in Testing**: Connectivity tests and validation
- **📈 Multiple Targets**: Analyze multiple .onion addresses
- **🛠 Demo Mode**: Test without Tor using demo data

## Prerequisites

- Docker and Docker Compose
- For local development: Python 3.8+ and Tor daemon

## Quick Start

### 🔍 Run Analysis

```bash
make analyze
```

### 📊 View Results

```bash
make viewer
# Open http://localhost:8080
```

### 🚀 Run Both (Analysis + Viewer)

```bash
make run
```

## Available Commands

```bash
make help          # Show all available commands
make build         # Build Docker image
make analyze       # Run analysis only
make viewer        # Start results viewer only
make run           # Run analysis + start viewer
make test          # Quick test with sample URL
make demo          # Run demo without Tor
make logs          # Show analyzer logs
make stop          # Stop all services
make clean         # Clean up everything
```

## Local Development

### Install Dependencies

```bash
pip install -r src/requirements.txt
```

### Start Tor Service

```bash
# macOS
brew install tor && tor

# Ubuntu/Debian
sudo apt install tor && sudo systemctl start tor
```

### Test Results Viewer Locally

```bash
cd results
python3 server.py 8080
# Open http://localhost:8080
```

## Architecture

**🔍 tor-analyzer**: Runs Tor network analysis and generates reports  
**📊 results-viewer**: Serves web interface for viewing results

Benefits:

- Run analysis independently without starting the web viewer
- View existing results without running new analysis
- Scale each component separately

## Configuration

- **Target URLs**: Edit `src/assets/collect_target_address.txt`
- **Proxy Settings**: Modify `src/analyzer.py` if needed
- **Analysis Parameters**: Configure in `main.py`

## Results Dashboard

The web interface provides:

- 📊 **Analysis Results** with success rates and response times
- 📈 **Performance Charts** for all analysis runs  
- 🔄 **Auto-refresh** functionality
- 📱 **Responsive design** for all devices
- 📅 **Historical Data** from previous analyses

## License

This project is for educational and research purposes only. Use responsibly and in accordance with local laws.
