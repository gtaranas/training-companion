# 🚀 Quick Setup Guide

## ✅ Status: Ready to Use

All files are installed and verified. Follow these steps to start using your soccer prediction agent.

---

## 📋 Prerequisites

- Python 3.8 or higher ✅
- DeepSeek API key (get free at https://platform.deepseek.com/)
- ~500MB disk space

---

## 🔧 Step-by-Step Setup

### 1️⃣ Navigate to Project Directory

```bash
cd /project/workspace/training-companion
```

### 2️⃣ Activate Virtual Environment

```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**You should see `(venv)` in your terminal**

### 3️⃣ Verify Installation

```bash
# Check all dependencies are installed
pip list | grep -E "streamlit|httpx|pandas|deepseek"

# Or run the verification test
python3 << 'PYEND'
import ace_framework
import deepseek_integration
import streamlit
print("✅ All modules imported successfully!")
PYEND
```

### 4️⃣ Configure DeepSeek API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# Open .env in your editor and replace:
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

**You'll see output like:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://XXX.XXX.X.XXX:8501
```

### 6️⃣ Open in Browser

Visit: **http://localhost:8501**

---

## 🎯 First Time Using the App

1. **Sidebar**: Paste your DeepSeek API key
2. **Make Prediction Tab**: Enter match details (teams, league, form)
3. **Click**: "🔮 Get Prediction"
4. **Review**: Prediction details and reasoning
5. **Record**: Actual outcome after the match
6. **Monitor**: Learning progress in the "Learning State" tab

---

## ✅ Verification Checklist

- [x] Virtual environment created
- [x] Dependencies installed
- [x] All tests passing (10/10)
- [x] Modules importable
- [x] Ready for use

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'httpx'`

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
# Make sure venv is activated (should see (venv) in terminal)
source venv/bin/activate

# Reinstall
pip install streamlit==1.28.1
```

### Issue: API key not working

**Solution:**
1. Get a valid key from https://platform.deepseek.com/
2. Check `.env` file has: `DEEPSEEK_API_KEY=your_actual_key`
3. No spaces or quotes around the key
4. Restart the app: `streamlit run app.py`

### Issue: Port 8501 already in use

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

Then visit: http://localhost:8502

### Issue: Streamlit not responding

**Solution:**
```bash
# Clear cache and restart
streamlit cache clear
streamlit run app.py
```

---

## 📚 File Structure

```
training-companion/
├── app.py                          # Main Streamlit app
├── ace_framework.py                # ACE Framework
├── deepseek_integration.py         # DeepSeek integration
├── test_ace_framework.py           # Tests
├── example_usage.py                # Usage example
├── requirements.txt                # Dependencies
├── .env.example                    # Env template
├── README.md                       # Full documentation
├── SETUP_GUIDE.md                  # This file
└── venv/                           # Virtual environment
```

---

## 🚀 Running Tests

```bash
# Activate environment
source venv/bin/activate

# Run all tests
python3 test_ace_framework.py

# Expected output:
# Ran 10 tests in 0.001s
# OK
```

---

## 📖 Documentation

- **README.md** - Full feature documentation
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **FINAL_DELIVERY.md** - Deployment guide
- **example_usage.py** - Code examples

---

## 🎓 How It Works

1. **Generate** - Creates 5 strategies based on learned patterns
2. **Predict** - Makes match prediction using strategies
3. **Record** - You record the actual match result
4. **Reflect** - Agent analyzes what worked/failed
5. **Curate** - Updates knowledge base with findings
6. **Improve** - Next prediction uses improved knowledge

---

## 💡 Tips for Best Results

1. **Record outcomes promptly** after matches end
2. **Provide context** in additional info (injuries, trades)
3. **Use consistent team names** across predictions
4. **Monitor learning** in the Learning State tab
5. **Export data** regularly for backup

---

## ✨ What's Next?

After setup:
1. ✅ Make your first prediction
2. ✅ Record some match outcomes (for learning)
3. ✅ Monitor accuracy in History tab
4. ✅ Watch learning in Learning State tab
5. ✅ See improvements over time

---

**Ready to go!** 🚀⚽

For issues, check the troubleshooting section above or review the full documentation.
