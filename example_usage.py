"""
Example usage of the Soccer Prediction Agent
Demonstrates core functionality
"""

from deepseek_integration import SoccerPredictionAgent
import os

def main():
    # Initialize agent
    print("🚀 Initializing Soccer Prediction Agent with ACE Framework...\n")
    
    # Get API key from environment
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ Error: DEEPSEEK_API_KEY not set in environment")
        print("   Please set your DeepSeek API key:")
        print("   export DEEPSEEK_API_KEY='your-api-key-here'")
        return
    
    agent = SoccerPredictionAgent(deepseek_api_key=api_key)
    print("✅ Agent initialized with baseline soccer knowledge\n")
    
    # Example 1: Make a prediction
    print("=" * 60)
    print("EXAMPLE 1: Making a Soccer Prediction")
    print("=" * 60)
    
    match_data = {
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "league": "Premier League",
        "date": "2024-02-10",
        "home_form": "Good (3-4 W)",
        "away_form": "Excellent (4-5 W)",
        "additional_info": "Manchester United has key midfielder out due to injury"
    }
    
    print(f"\nMatch: {match_data['home_team']} vs {match_data['away_team']}")
    print(f"League: {match_data['league']}")
    print(f"Home Form: {match_data['home_form']}")
    print(f"Away Form: {match_data['away_form']}\n")
    
    print("🔮 Generating prediction...\n")
    prediction = agent.predict_match(match_data)
    
    print(f"Prediction: {prediction['prediction']}")
    print(f"Confidence: {prediction['confidence']:.1%}")
    print(f"Risk Level: {prediction['risk_level']}")
    print(f"\nAnalysis:\n{prediction['reasoning']}")
    print(f"\nKey Factors:")
    for i, factor in enumerate(prediction['key_factors'], 1):
        print(f"  {i}. {factor}")
    
    # Example 2: Record outcome and learn
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Recording Outcome & Learning")
    print("=" * 60)
    
    actual_outcome = "Draw"  # Assume match ended in draw
    print(f"\nActual Match Result: {actual_outcome}")
    print("🧠 Agent is learning from this outcome...\n")
    
    learning_result = agent.record_outcome(prediction, actual_outcome)
    
    print(f"Prediction Accuracy: {'✅ Correct' if learning_result['accuracy'] else '❌ Incorrect'}")
    print(f"\nLearned Insights:")
    for insight in learning_result['reflections']['insights'][:3]:
        print(f"  💡 {insight}")
    
    print(f"\nRecommendations for Future:")
    for i, rec in enumerate(learning_result['reflections']['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    # Example 3: View learning state
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Agent Learning State")
    print("=" * 60)
    
    state = agent.get_learning_state()
    print(f"\nTotal Context Items Learned: {state['total_items']}")
    print(f"Execution History: {state['execution_history_count']}")
    print(f"\nKnowledge by Category:")
    for category, count in state.get('by_category', {}).items():
        print(f"  - {category}: {count} items")
    
    print("\n" + "=" * 60)
    print("Example completed! The agent is now ready for production.")
    print("=" * 60)

if __name__ == "__main__":
    main()
