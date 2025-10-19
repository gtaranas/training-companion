"""
DeepSeek Integration for Soccer Prediction Agent
Implements Generator, Reflector, and Curator using DeepSeek API
"""

import os
import json
import httpx
from typing import List, Dict, Any
from ace_framework import (
    Generator, Reflector, Curator, ContextItem, ReflectionResult, ACEFramework
)
from dotenv import load_dotenv

load_dotenv()


class DeepSeekClient:
    """Client for interacting with DeepSeek API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"
        
    def call(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call DeepSeek API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"API Error: {str(e)}"


class DeepSeekGenerator(Generator):
    """Generate strategies and predictions using DeepSeek"""
    
    def __init__(self, client: DeepSeekClient):
        self.client = client
        
    def generate(self, task: str, context: List[ContextItem]) -> List[str]:
        """Generate strategies for soccer prediction"""
        
        # Build context summary
        context_summary = self._build_context_summary(context)
        
        prompt = f"""You are an expert soccer prediction analyst using self-learning techniques.

Current Context Knowledge:
{context_summary}

New Task: {task}

Based on the accumulated knowledge and patterns, generate 5 strategic approaches to improve prediction accuracy. 
Each approach should:
1. Leverage learned patterns from previous predictions
2. Address identified gaps or failures
3. Be specific and actionable
4. Include metrics or validation methods

Format your response as a JSON array of strategy objects with 'name', 'description', 'expected_improvement', and 'risk_level' fields."""

        response = self.client.call(prompt, temperature=0.7, max_tokens=1500)
        
        try:
            # Extract JSON from response
            strategies = self._parse_json_response(response)
            return strategies if isinstance(strategies, list) else [response]
        except:
            return [response]
    
    def _build_context_summary(self, context: List[ContextItem]) -> str:
        """Build summary of learned context"""
        if not context:
            return "No prior knowledge available. Starting fresh."
        
        categories = {}
        for item in context:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item.content)
        
        summary = "Previous Learnings:\n"
        for category, items in categories.items():
            summary += f"\n{category.upper()}:\n"
            for item in items[:5]:  # Limit to top 5 per category
                summary += f"  - {item}\n"
        
        return summary
    
    def _parse_json_response(self, response: str) -> List[str]:
        """Parse JSON from response text"""
        # Find JSON array in response
        start = response.find("[")
        end = response.rfind("]") + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            data = json.loads(json_str)
            if isinstance(data, list):
                return [str(item) for item in data]
        return []


class DeepSeekReflector(Reflector):
    """Analyze predictions and extract insights using DeepSeek"""
    
    def __init__(self, client: DeepSeekClient):
        self.client = client
    
    def reflect(self, execution_trace: Dict[str, Any], context: List[ContextItem]) -> ReflectionResult:
        """Analyze execution results and extract insights"""
        
        # Prepare execution summary
        exec_summary = self._prepare_execution_summary(execution_trace)
        context_summary = self._prepare_context_summary(context)
        
        prompt = f"""You are an expert analyzer of soccer prediction performance.

Execution Trace:
{exec_summary}

Current Context:
{context_summary}

Analyze this prediction attempt and provide:
1. Key Insights (what worked, what didn't)
2. Identified Patterns (recurring themes)
3. Failures/Errors (what went wrong)
4. Recommendations (how to improve)
5. Context Gaps (missing knowledge)

Format as JSON with keys: insights, patterns, failures, recommendations, context_gaps"""

        response = self.client.call(prompt, temperature=0.5, max_tokens=1500)
        
        return self._parse_reflection_response(response)
    
    def _prepare_execution_summary(self, trace: Dict[str, Any]) -> str:
        """Summarize execution trace"""
        summary = f"""
Match: {trace.get('match', 'N/A')}
Predicted Outcome: {trace.get('prediction', 'N/A')}
Actual Outcome: {trace.get('actual_outcome', 'N/A')}
Confidence: {trace.get('confidence', 'N/A')}
Accuracy: {'✓' if trace.get('correct', False) else '✗'}
Features Used: {', '.join(trace.get('features', []))}
"""
        return summary
    
    def _prepare_context_summary(self, context: List[ContextItem]) -> str:
        """Summarize current context"""
        if not context:
            return "No prior learnings"
        return f"Context items: {len(context)}, Categories: {set(c.category for c in context)}"
    
    def _parse_reflection_response(self, response: str) -> ReflectionResult:
        """Parse reflection response from DeepSeek"""
        try:
            # Extract JSON
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            data = json.loads(json_str)
            
            return ReflectionResult(
                insights=data.get("insights", []),
                patterns=data.get("patterns", []),
                failures=data.get("failures", []),
                recommendations=data.get("recommendations", []),
                context_gaps=data.get("context_gaps", [])
            )
        except:
            return ReflectionResult(
                insights=["Unable to parse insights"],
                patterns=[],
                failures=[],
                recommendations=["Continue monitoring performance"],
                context_gaps=[]
            )


class DeepSeekCurator(Curator):
    """Manage context updates using DeepSeek (incremental delta updates)"""
    
    def __init__(self, client: DeepSeekClient):
        self.client = client
    
    def curate(self, current_context: List[ContextItem], 
              new_insights: List[str], 
              reflections: ReflectionResult) -> List[ContextItem]:
        """Update context with new insights (delta updates, not rewrites)"""
        
        # Add new insights as context items
        for i, insight in enumerate(new_insights):
            new_item = ContextItem(
                id=f"insight_{len(current_context)}_{i}",
                content=insight,
                category="insight",
                priority=0.8
            )
            current_context.append(new_item)
        
        # Add recommendations as strategies
        for i, rec in enumerate(reflections.recommendations):
            strategy_item = ContextItem(
                id=f"strategy_{len(current_context)}_{i}",
                content=rec,
                category="strategy",
                priority=0.7
            )
            current_context.append(strategy_item)
        
        # Update effectiveness of existing context based on reflections
        if reflections.failures:
            for context_item in current_context:
                context_item.update_effectiveness(success=False, impact=0.5)
        
        return current_context


class SoccerPredictionAgent:
    """Self-learning soccer prediction agent using ACE framework"""
    
    def __init__(self, deepseek_api_key: str = None):
        self.client = DeepSeekClient(deepseek_api_key)
        
        # Initialize ACE components
        generator = DeepSeekGenerator(self.client)
        reflector = DeepSeekReflector(self.client)
        curator = DeepSeekCurator(self.client)
        
        self.ace = ACEFramework(generator, reflector, curator)
        self._initialize_context()
    
    def _initialize_context(self):
        """Initialize with baseline soccer knowledge"""
        baseline_knowledge = [
            ContextItem(
                id="baseline_1",
                content="Home advantage typically provides 3-5% win probability increase",
                category="pattern",
                priority=0.9,
                effectiveness_score=0.85
            ),
            ContextItem(
                id="baseline_2",
                content="Recent form (last 5 matches) is highly predictive of next outcome",
                category="pattern",
                priority=0.9,
                effectiveness_score=0.82
            ),
            ContextItem(
                id="baseline_3",
                content="Team strength ratings (offensive/defensive) should be normalized by opponents faced",
                category="strategy",
                priority=0.8,
                effectiveness_score=0.78
            ),
            ContextItem(
                id="baseline_4",
                content="Injuries to key players significantly impact prediction accuracy",
                category="pattern",
                priority=0.85,
                effectiveness_score=0.80
            ),
        ]
        
        for item in baseline_knowledge:
            self.ace.add_context_item(item)
    
    def predict_match(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a prediction for a soccer match"""
        
        # Generate strategies
        strategies = self.ace.generate_strategies(
            f"Predict outcome for: {match_data.get('home_team', 'N/A')} vs {match_data.get('away_team', 'N/A')}"
        )
        
        # Call DeepSeek for prediction
        prediction_prompt = self._build_prediction_prompt(match_data, strategies)
        prediction_response = self.client.call(prediction_prompt, temperature=0.3, max_tokens=800)
        
        # Parse prediction
        prediction = self._parse_prediction(prediction_response, match_data)
        
        return prediction
    
    def _build_prediction_prompt(self, match_data: Dict[str, Any], strategies: List[str]) -> str:
        """Build prediction prompt"""
        
        prompt = f"""As a professional soccer prediction analyst, predict the outcome of this match:

Match Details:
- Home Team: {match_data.get('home_team', 'N/A')}
- Away Team: {match_data.get('away_team', 'N/A')}
- League: {match_data.get('league', 'N/A')}
- Date: {match_data.get('date', 'N/A')}
- Home Form: {match_data.get('home_form', 'N/A')}
- Away Form: {match_data.get('away_form', 'N/A')}

Strategies to Consider:
{json.dumps(strategies, indent=2)}

Provide your prediction in JSON format with:
- prediction: "Home Win" / "Draw" / "Away Win"
- confidence: 0.0-1.0
- reasoning: brief explanation
- key_factors: list of important factors
- risk_level: "Low" / "Medium" / "High"
"""
        return prompt
    
    def _parse_prediction(self, response: str, match_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse prediction from response"""
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            prediction = json.loads(json_str)
            
            return {
                "match": f"{match_data.get('home_team')} vs {match_data.get('away_team')}",
                "prediction": prediction.get("prediction", "Draw"),
                "confidence": prediction.get("confidence", 0.5),
                "reasoning": prediction.get("reasoning", ""),
                "key_factors": prediction.get("key_factors", []),
                "risk_level": prediction.get("risk_level", "Medium"),
                "success": False  # Will be updated after match result
            }
        except:
            return {
                "match": f"{match_data.get('home_team')} vs {match_data.get('away_team')}",
                "prediction": "Draw",
                "confidence": 0.33,
                "reasoning": "Unable to analyze - using default prediction",
                "key_factors": [],
                "risk_level": "High",
                "success": False
            }
    
    def record_outcome(self, prediction: Dict[str, Any], actual_outcome: str):
        """Record actual outcome and learn from it"""
        
        # Check if prediction was correct
        was_correct = prediction["prediction"] == actual_outcome
        
        # Create execution trace
        execution_trace = {
            "match": prediction["match"],
            "prediction": prediction["prediction"],
            "actual_outcome": actual_outcome,
            "confidence": prediction["confidence"],
            "correct": was_correct,
            "features": prediction.get("key_factors", [])
        }
        
        # Reflect on execution
        reflections = self.ace.reflect_on_execution(execution_trace)
        
        # Curate context (learn from result)
        self.ace.curate_context(reflections)
        
        # Update prediction with success info
        prediction["success"] = was_correct
        
        return {
            "accuracy": was_correct,
            "reflections": {
                "insights": reflections.insights,
                "patterns": reflections.patterns,
                "recommendations": reflections.recommendations,
            }
        }
    
    def get_learning_state(self) -> Dict[str, Any]:
        """Get current learning state of the agent"""
        return self.ace.get_context_state()
