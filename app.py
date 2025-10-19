"""
Soccer Prediction Agent - Streamlit Application
Self-learning agent using ACE framework with DeepSeek
"""

import streamlit as st
import json
from datetime import datetime
from deepseek_integration import SoccerPredictionAgent, DeepSeekClient
import os

# Page configuration
st.set_page_config(
    page_title="⚽ Soccer Prediction Agent",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .insight-card {
        background: #f0f2f6;
        padding: 15px;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 10px 0;
    }
    .learning-state {
        background: #e7f3ff;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.api_key = ""
    st.session_state.predictions = []
    st.session_state.learning_history = []

def initialize_agent(api_key: str):
    """Initialize the soccer prediction agent"""
    try:
        agent = SoccerPredictionAgent(deepseek_api_key=api_key)
        st.session_state.agent = agent
        return True, "Agent initialized successfully!"
    except Exception as e:
        return False, f"Error initializing agent: {str(e)}"

def main():
    st.title("⚽ Self-Learning Soccer Prediction Agent")
    st.markdown("*Powered by ACE Framework & DeepSeek AI*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key_input = st.text_input(
            "DeepSeek API Key",
            type="password",
            value=st.session_state.api_key,
            placeholder="Enter your DeepSeek API key"
        )
        
        if api_key_input and api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input
            success, message = initialize_agent(api_key_input)
            if success:
                st.success(message)
            else:
                st.error(message)
        
        # Information about ACE framework
        st.markdown("---")
        st.subheader("📚 About ACE Framework")
        st.markdown("""
        The **Agentic Context Engineering (ACE)** framework enables self-learning through:
        
        1. **Generator**: Creates strategies based on learned patterns
        2. **Reflector**: Analyzes execution and extracts insights
        3. **Curator**: Updates context with incremental delta updates
        
        This ensures continuous learning without forgetting previous knowledge.
        """)
        
        # Learning statistics
        if st.session_state.agent:
            st.markdown("---")
            st.subheader("📊 Learning Statistics")
            learning_state = st.session_state.agent.get_learning_state()
            st.metric("Context Items Learned", learning_state["total_items"])
            st.metric("Execution History", learning_state["execution_history_count"])
            
            if "by_category" in learning_state:
                for cat, count in learning_state["by_category"].items():
                    st.metric(f"{cat.capitalize()}", count)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Make Prediction", "📈 Prediction History", "🧠 Learning State", "ℹ️ Help"])
    
    with tab1:
        st.header("Make a Soccer Match Prediction")
        
        if not st.session_state.agent:
            st.warning("⚠️ Please configure your DeepSeek API key in the sidebar first.")
        else:
            with st.form("match_prediction_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    home_team = st.text_input("Home Team", placeholder="e.g., Manchester United")
                    away_team = st.text_input("Away Team", placeholder="e.g., Liverpool")
                    league = st.selectbox(
                        "League",
                        ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "Other"]
                    )
                
                with col2:
                    match_date = st.date_input("Match Date")
                    home_form = st.selectbox(
                        "Home Team Form",
                        ["Excellent (4-5 W)", "Good (3-4 W)", "Average (2 W-L)", "Poor (1-2 L)", "Very Poor (3+ L)"]
                    )
                    away_form = st.selectbox(
                        "Away Team Form",
                        ["Excellent (4-5 W)", "Good (3-4 W)", "Average (2 W-L)", "Poor (1-2 L)", "Very Poor (3+ L)"]
                    )
                
                additional_info = st.text_area(
                    "Additional Information (optional)",
                    placeholder="e.g., Key injuries, recent trades, special conditions...",
                    height=80
                )
                
                submit_button = st.form_submit_button("🔮 Get Prediction", use_container_width=True)
                
                if submit_button:
                    if not home_team or not away_team:
                        st.error("Please enter both team names.")
                    else:
                        match_data = {
                            "home_team": home_team,
                            "away_team": away_team,
                            "league": league,
                            "date": str(match_date),
                            "home_form": home_form,
                            "away_form": away_form,
                            "additional_info": additional_info
                        }
                        
                        with st.spinner("🤔 Analyzing match and generating strategies..."):
                            try:
                                prediction = st.session_state.agent.predict_match(match_data)
                                prediction["timestamp"] = datetime.now().isoformat()
                                st.session_state.predictions.append(prediction)
                                
                                # Display prediction
                                st.success("Prediction Generated!")
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Prediction", prediction["prediction"])
                                with col2:
                                    st.metric("Confidence", f"{prediction['confidence']:.1%}")
                                with col3:
                                    st.metric("Risk Level", prediction["risk_level"])
                                
                                # Reasoning
                                st.subheader("Analysis & Reasoning")
                                st.info(prediction["reasoning"])
                                
                                # Key factors
                                st.subheader("Key Factors")
                                if prediction["key_factors"]:
                                    for i, factor in enumerate(prediction["key_factors"], 1):
                                        st.write(f"{i}. {factor}")
                                
                                # Record actual outcome
                                st.markdown("---")
                                st.subheader("Record Actual Outcome (for learning)")
                                
                                actual_outcome = st.radio(
                                    "What was the actual match result?",
                                    ["Home Win", "Draw", "Away Win", "Not Yet Played"],
                                    horizontal=True
                                )
                                
                                if st.button("✅ Record Outcome", key="record_outcome", use_container_width=True):
                                    if actual_outcome != "Not Yet Played":
                                        with st.spinner("🧠 Learning from outcome..."):
                                            learning_result = st.session_state.agent.record_outcome(
                                                prediction,
                                                actual_outcome
                                            )
                                            
                                            st.session_state.learning_history.append({
                                                "match": prediction["match"],
                                                "timestamp": datetime.now().isoformat(),
                                                "accuracy": learning_result["accuracy"],
                                                "reflections": learning_result["reflections"]
                                            })
                                            
                                            if learning_result["accuracy"]:
                                                st.success("✅ Correct prediction! Agent has learned from this success.")
                                            else:
                                                st.info("❌ Incorrect prediction. Agent is learning from this failure.")
                                            
                                            st.subheader("Agent Insights")
                                            if learning_result["reflections"]["insights"]:
                                                for insight in learning_result["reflections"]["insights"]:
                                                    st.markdown(f"💡 {insight}")
                                            
                                            st.subheader("Recommendations for Next Time")
                                            if learning_result["reflections"]["recommendations"]:
                                                for i, rec in enumerate(learning_result["reflections"]["recommendations"], 1):
                                                    st.markdown(f"{i}. {rec}")
                                    else:
                                        st.warning("Please select an actual outcome to record learning.")
                            
                            except Exception as e:
                                st.error(f"Error generating prediction: {str(e)}")
    
    with tab2:
        st.header("📈 Prediction History")
        
        if not st.session_state.predictions:
            st.info("No predictions made yet. Start by making a prediction in the 'Make Prediction' tab.")
        else:
            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Predictions", len(st.session_state.predictions))
            with col2:
                successful = sum(1 for p in st.session_state.predictions if p.get("success", False))
                accuracy = (successful / len(st.session_state.predictions) * 100) if st.session_state.predictions else 0
                st.metric("Accuracy", f"{accuracy:.1f}%")
            with col3:
                avg_confidence = sum(p["confidence"] for p in st.session_state.predictions) / len(st.session_state.predictions)
                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
            
            # Display all predictions
            st.markdown("---")
            st.subheader("All Predictions")
            
            for i, pred in enumerate(reversed(st.session_state.predictions), 1):
                with st.expander(f"#{len(st.session_state.predictions) - i + 1}: {pred['match']}"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Prediction", pred["prediction"])
                    with col2:
                        st.metric("Confidence", f"{pred['confidence']:.1%}")
                    with col3:
                        status = "✅" if pred.get("success") else "❌" if pred.get("success") is False else "⏳"
                        st.metric("Status", status)
                    with col4:
                        st.metric("Risk", pred["risk_level"])
                    
                    st.write(f"**Reasoning**: {pred['reasoning']}")
                    
                    if pred.get("key_factors"):
                        st.write("**Key Factors**:", ", ".join(pred["key_factors"][:3]))
    
    with tab3:
        st.header("🧠 Agent Learning State")
        
        if not st.session_state.agent:
            st.warning("Agent not initialized. Please configure API key.")
        else:
            learning_state = st.session_state.agent.get_learning_state()
            
            # Overview
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Context Items", learning_state["total_items"])
            with col2:
                st.metric("Executions Analyzed", learning_state["execution_history_count"])
            
            # Context by category
            st.subheader("Knowledge by Category")
            if "by_category" in learning_state:
                for category, count in learning_state["by_category"].items():
                    st.progress(count / (sum(learning_state["by_category"].values()) or 1),
                               f"{category.capitalize()}: {count} items")
            
            # Detailed context items
            st.subheader("Detailed Context Items")
            if "items" in learning_state and learning_state["items"]:
                for item in learning_state["items"]:
                    with st.expander(f"{item['category'].upper()}: {item['content'][:50]}..."):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Priority", f"{item['priority']:.2f}")
                        with col2:
                            st.metric("Effectiveness", f"{item['effectiveness_score']:.2f}")
                        with col3:
                            st.metric("Usage Count", item['usage_count'])
                        
                        st.write(f"**Full Content**: {item['content']}")
                        st.caption(f"Created: {item['created_at']}")
            
            # Learning history
            if st.session_state.learning_history:
                st.subheader("Recent Learning Events")
                for event in reversed(st.session_state.learning_history[-5:]):
                    with st.expander(f"{event['match']} - {event['timestamp'][:10]}"):
                        status_icon = "✅" if event["accuracy"] else "❌"
                        st.write(f"{status_icon} **Accuracy**: {event['accuracy']}")
                        
                        if event["reflections"]["insights"]:
                            st.write("**Insights Extracted**:")
                            for insight in event["reflections"]["insights"][:3]:
                                st.write(f"• {insight}")
    
    with tab4:
        st.header("ℹ️ Help & Information")
        
        st.subheader("🚀 Getting Started")
        st.markdown("""
        1. **Add DeepSeek API Key**: Configure your API key in the sidebar
        2. **Make Predictions**: Enter match details and get AI-powered predictions
        3. **Record Outcomes**: After matches, record actual results for the agent to learn
        4. **Monitor Learning**: View the agent's evolving knowledge in the Learning State tab
        """)
        
        st.subheader("🎯 How the ACE Framework Works")
        st.markdown("""
        ### Generator
        Creates strategic approaches based on learned patterns. Generates 5 actionable strategies for each prediction.
        
        ### Reflector
        Analyzes prediction performance and extracts:
        - Key insights about what worked
        - Identified patterns
        - Failures and errors
        - Recommendations for improvement
        
        ### Curator
        Updates the agent's knowledge base through:
        - Incremental delta updates (not full rewrites)
        - Fine-grained context management
        - Effectiveness scoring
        - Periodic refinement to reduce redundancy
        """)
        
        st.subheader("⚽ Soccer-Specific Features")
        st.markdown("""
        - **Home Advantage**: Accounts for statistical advantage of home teams
        - **Form Analysis**: Considers recent 5-match performance
        - **Team Strength**: Analyzes offensive and defensive capabilities
        - **Injury Updates**: Incorporates key player availability
        - **Confidence Scoring**: Provides probability estimates
        """)
        
        st.subheader("📊 About Your Data")
        st.markdown("""
        All predictions and learning data are stored in your session. 
        To persist data, export from the Prediction History tab.
        """)
        
        # Export data button
        if st.session_state.predictions:
            st.subheader("📥 Export Data")
            export_data = {
                "predictions": st.session_state.predictions,
                "learning_history": st.session_state.learning_history
            }
            st.download_button(
                label="Download All Data (JSON)",
                data=json.dumps(export_data, indent=2),
                file_name=f"soccer_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
