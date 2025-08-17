# Neighbourhood Energy Optimizer

A sophisticated multi-agent system for analyzing residential energy consumption and providing personalized discount incentives based on energy efficiency criteria.

🎥 [Watch Demo Video](https://youtu.be/r3MOKz0hM1c)


## 🏗️ System Architecture

The system uses a multi-agent architecture with the following components:

- **Energy Monitor Agent**: Processes consumer data and manages the sequential processing flow
- **Incentives Agent**: Analyzes eligibility and generates personalized notifications
- **MCP (Model Context Protocol)**: Handles data access and communication
- **BeeAI Framework**: Provides agent infrastructure and communication
- **LLM Integration**: WatsonX AI for personalized message generation with fallback templates
- <img width="785" height="580" alt="image" src="https://github.com/user-attachments/assets/bd430fd8-6a7d-4b88-9d48-c713ad1c9b32" />


### Architecture Diagrams

Generate visual diagrams using the provided scripts:

```bash
# Generate both architecture and functional diagrams
python architecture/generate_all_diagrams.py

# Or generate individually
python architecture/generate_architecture_diagram.py
python architecture/generate_functional_diagram.py
```

## 🚀 Features

### Energy Efficiency Analysis
- **Usage Threshold**: Analyzes consumption against 4 kWh/day threshold
- **Equipment Efficiency**: Evaluates energy-efficient equipment usage
- **Solar Production**: Considers solar energy generation
- **Personalized Discounts**: Provides targeted incentives based on multiple criteria

### Discount Scenarios
1. **10% Discount**: < 4 kWh/day + Efficient Equipment + Solar Production
2. **5% Discount (Efficient)**: < 4 kWh/day + Efficient Equipment (no solar)
3. **5% Discount (Solar)**: < 4 kWh/day + Solar Production (no efficient equipment)
4. **No Discount (Low Usage)**: < 4 kWh/day (no other qualifying factors)
5. **High Usage**: ≥ 4 kWh/day (encouragement and recommendations)

### Intelligent Notifications
- **Personalized Messages**: LLM-generated content with consumer-specific details
- **Actionable Advice**: Clear recommendations for improving eligibility
- **Fallback System**: Template-based messages when LLM is unavailable
- **Comprehensive Coverage**: Detailed notifications for all consumer categories

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd neighbourhood_energy_optimizer
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install BeeAI Framework**:
   ```bash
   pip install beeai-framework
   ```

## ⚙️ Configuration

### LLM Configuration (Optional)

To use WatsonX AI for personalized notifications:

1. Create a `.env` file in the root directory:
   ```env
   USE_WATSONX=true
   WATSONX_API_KEY=your_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_MODEL=ibm/granite-3-2-8b-instruct
   ```

2. Get WatsonX credentials from [IBM Cloud](https://cloud.ibm.com/ai/watsonx)

**Note**: The system works with mock LLM by default and will automatically fallback to templates if WatsonX is not configured.

## 🚀 Usage

### Quick Start

Run the complete system:

```bash
python src/main.py
```

### Individual Components

**Generate mock data**:
```bash
python scripts/generate_mock_db.py
```

**Run agents separately**:
```bash
python agents/run_beeai_agents.py
```

**Generate architecture diagrams**:
```bash
python architecture/generate_all_diagrams.py
```

## 📊 Data Structure

The system uses a SQLite database with the following schema:

```sql
CREATE TABLE consumption (
    consumer_id TEXT,
    date TEXT,
    daily_kwh REAL,
    uses_efficient_equipment INTEGER,
    produces_solar INTEGER
);
```

### Mock Data Generation

The system generates 50 consumers with the following distribution:
- **5 consumers**: 10% discount eligible
- **5 consumers**: 5% discount (efficient equipment)
- **5 consumers**: 5% discount (solar production)
- **5 consumers**: No discount (low usage)
- **30 consumers**: High usage (various combinations)

## 🔄 System Flow

1. **Initialization**: System starts and generates fresh mock data
2. **Sequential Processing**: Monitor agent sends one consumer at a time
3. **Analysis**: Incentives agent analyzes each consumer's eligibility
4. **Notification Generation**: Personalized messages created via LLM or templates
5. **Acknowledgment**: Processing confirmed before next consumer
6. **Completion**: All 50 consumers processed with detailed output

## 📁 Project Structure

```
neighbourhood_energy_optimizer/
├── agents/                     # Multi-agent system components
│   ├── energy_monitor_beeai.py # Energy monitoring agent
│   ├── incentives_beeai.py     # Incentives analysis agent
│   └── run_beeai_agents.py     # Agent orchestration
├── architecture/               # System documentation
│   ├── generate_architecture_diagram.py
│   ├── generate_functional_diagram.py
│   └── generate_all_diagrams.py
├── data/                       # Database storage
│   └── mock_data.db
├── llm/                        # Language model integration
│   └── watson_client.py
├── mcp/                        # Model Context Protocol
│   ├── mcp_client.py
│   ├── mcp_server.py
│   └── store.py
├── scripts/                    # Utility scripts
│   └── generate_mock_db.py
├── src/                        # Main application
│   └── main.py
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🧪 Testing

The system includes comprehensive testing scenarios:

- **All Discount Categories**: Ensures every scenario is covered
- **Sequential Processing**: Validates one-by-one consumer processing
- **LLM Integration**: Tests both WatsonX and fallback scenarios
- **Randomized Data**: Uses realistic consumer IDs for testing

## 🔧 Customization

### Adding New Discount Criteria

1. Update the `determine_discount_scenario()` method in `agents/incentives_beeai.py`
2. Add new notification templates in `llm/watson_client.py`
3. Update the mock data generation in `scripts/generate_mock_db.py`

### Modifying LLM Prompts

Edit the prompt templates in `llm/watson_client.py` to customize notification content and style.

### Extending Agent Functionality

Add new agents by extending the `BaseAgent` class and implementing the required methods.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review the architecture diagrams
3. Examine the code comments
4. Create an issue in the repository

## 🔮 Future Enhancements

- **Real-time Data Integration**: Connect to actual energy monitoring systems
- **Machine Learning**: Predictive analytics for energy consumption
- **Web Interface**: Dashboard for monitoring and management
- **API Endpoints**: RESTful API for external integrations
- **Advanced Analytics**: Detailed energy efficiency insights

