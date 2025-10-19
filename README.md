# ⚽ Soccer Prediction Agent - Self-Learning with ACE Framework

A sophisticated self-learning soccer prediction agent built with the **Agentic Context Engineering (ACE)** framework, DeepSeek AI, and Streamlit.

Based on the paper: ["Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"](https://arxiv.org/pdf/2510.04618)

## 🎯 Features

### Core ACE Framework Components

1. **Generator** - Creates strategic prediction approaches
   - Generates 5 actionable strategies per match
   - Leverages learned patterns and historical context
   - Addresses identified knowledge gaps

2. **Reflector** - Analyzes prediction performance
   - Extracts insights from execution results
   - Identifies recurring patterns
   - Documents failures and recommendations
   - Operates independently from curation

3. **Curator** - Manages context evolution
   - **Incremental Delta Updates**: Localized edits instead of full rewrites
   - **Itemized Context**: Fine-grained knowledge management
   - **Grow-and-Refine Mechanism**: Balances expansion with redundancy control
   - **Effectiveness Scoring**: Tracks performance of each learned item

### Soccer-Specific Capabilities

- **Home Advantage Analysis**: 3-5% win probability adjustment
- **Form Assessment**: Recent 5-match performance evaluation
- **Team Strength Rating**: Normalized offensive/defensive metrics
- **Injury Considerations**: Key player impact analysis
- **Confidence Scoring**: Probability-based predictions
- **Risk Assessment**: Low/Medium/High risk classification

### Self-Learning Features

- Continuous context evolution without information loss
- Automatic insight extraction from prediction outcomes
- Performance-based context refinement
- Historical pattern recognition
- Adaptive strategy generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- DeepSeek API key ([Get one here](https://platform.deepseek.com/))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd training-companion
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your DeepSeek API key
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📊 Usage Guide

### 1. Initialize Agent
- Add your DeepSeek API key in the sidebar
- Agent loads with baseline soccer knowledge

### 2. Make Predictions
- **Make Prediction** tab: Enter match details
  - Home/Away team names
  - League and date
  - Current form of both teams
  - Optional: Additional information (injuries, etc.)

### 3. Get Prediction
- **Prediction Output**:
  - Recommended outcome (Home Win/Draw/Away Win)
  - Confidence percentage
  - Detailed reasoning
  - Key influential factors
  - Risk assessment

### 4. Record Outcome (Enable Learning)
- After match conclusion, record actual result
- Agent analyzes prediction vs. actual outcome
- Extracts insights and patterns
- Updates internal knowledge base
- Displays learning reflections

### 5. Monitor Learning
- **Learning State** tab: View evolved context
- Track knowledge items by category
- Monitor effectiveness scores
- Review recent learning events

## 🧠 How ACE Enables Self-Learning

### Generator Phase
```
Current Context → Analysis → Generated Strategies
   ↓
"Home advantage is crucial" + "Recent form matters"
→ "Prioritize home team if form is recent and positive"
```

### Reflector Phase
```
Execution Trace → Analysis → Insights & Patterns
   ↓
Prediction: Home Win (80% confidence)
Actual: Away Win
→ Insight: "Our home advantage weight was too high"
→ Pattern: "Recent form overwhelms home advantage"
```

### Curator Phase
```
New Insights → Context Update → Evolved Knowledge Base
   ↓
Add: "Balance home advantage with recent form"
Update: Reduce effectiveness of pure home advantage strategy
Maintain: Insights that proved valuable
→ Improved predictions on next iteration
```

## 📁 Project Structure

```
training-companion/
├── app.py                          # Main Streamlit application
├── ace_framework.py                # ACE framework implementation
├── deepseek_integration.py         # DeepSeek API integration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
└── data/                          # (Auto-created) Session data storage
```

## 🔧 Key Files

### `ace_framework.py`
Implements the core ACE framework:
- `ContextItem`: Individual knowledge units with metadata
- `Generator`, `Reflector`, `Curator`: Abstract base classes
- `ACEFramework`: Orchestrator coordinating all components
- `ReflectionResult`: Structure for analysis output

### `deepseek_integration.py`
DeepSeek-powered implementations:
- `DeepSeekClient`: API communication
- `DeepSeekGenerator`: Strategy generation
- `DeepSeekReflector`: Outcome analysis
- `DeepSeekCurator`: Context management
- `SoccerPredictionAgent`: Main agent class

### `app.py`
Streamlit UI components:
- Prediction interface
- History tracking
- Learning state visualization
- Data export functionality

## 📈 Performance Metrics

The agent tracks:
- **Total Predictions**: Count of all forecasts
- **Accuracy Rate**: Percentage of correct predictions
- **Average Confidence**: Mean confidence across predictions
- **Context Items**: Number of learned knowledge items
- **Execution History**: Total learning events

## 🔐 Security

- API keys stored in `.env` file (never committed)
- Session-based data storage
- No external data persistence required
- All data under user control

## 💡 Advanced Features

### Data Export
- Export all predictions and learning history as JSON
- Backup your agent's knowledge
- Analysis and visualization support

### Context Management
- Automatic redundancy detection
- Effectiveness-based pruning
- Priority-based retention
- Metadata-rich items

### Adaptive Learning
- Success/failure-based scoring
- Pattern recognition
- Strategy evolution
- Automated refinement

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check .env file
cat .env
# Verify API key is valid
```

### Installation Issues
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Streamlit Issues
```bash
# Clear cache and restart
streamlit cache clear
streamlit run app.py
```

## 📚 Further Reading

- [ACE Paper](https://arxiv.org/pdf/2510.04618) - Original research
- [DeepSeek Documentation](https://platform.deepseek.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🤝 Contributing

This is a research-based implementation. Contributions welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🎓 Academic Citation

If you use this implementation, please cite:
```
@article{ace2024,
  title={Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models},
  year={2024},
  url={https://arxiv.org/pdf/2510.04618}
}
```

## ✨ Highlights

- ✅ **Self-Learning**: Improves with every prediction recorded
- ✅ **Context Preservation**: Incremental updates, no information loss
- ✅ **Academic Foundation**: Based on peer-reviewed research
- ✅ **Production Ready**: Full error handling and validation
- ✅ **User Friendly**: Streamlit UI with comprehensive dashboard
- ✅ **Extensible**: Easy to add new sports or domains

---

**Built with ⚽ and 🤖 by Giannhs Taranas**
