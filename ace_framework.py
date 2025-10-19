"""
Agentic Context Engineering (ACE) Framework
For Self-Improving Language Model Agents
Based on: "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
from abc import ABC, abstractmethod


@dataclass
class ContextItem:
    """Individual context item with metadata for fine-grained management"""
    id: str
    content: str
    category: str  # e.g., 'strategy', 'insight', 'pattern', 'failure'
    priority: float = 1.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    usage_count: int = 0
    effectiveness_score: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def update_effectiveness(self, success: bool, impact: float = 1.0):
        """Update effectiveness based on outcome"""
        if success:
            self.effectiveness_score = min(1.0, self.effectiveness_score + impact * 0.1)
        else:
            self.effectiveness_score = max(0.0, self.effectiveness_score - impact * 0.05)
        self.updated_at = datetime.now().isoformat()


@dataclass
class ReflectionResult:
    """Output from the Reflector component"""
    insights: List[str]
    patterns: List[Dict[str, Any]]
    failures: List[Dict[str, Any]]
    recommendations: List[str]
    context_gaps: List[str]


class Generator(ABC):
    """
    Generator: Creates new strategies and hypotheses
    Part of the ACE framework
    """
    
    @abstractmethod
    def generate(self, task: str, context: List[ContextItem]) -> List[str]:
        """Generate strategies based on task and existing context"""
        pass


class Reflector(ABC):
    """
    Reflector: Evaluates and extracts insights
    Separates evaluation from curation for better performance
    """
    
    @abstractmethod
    def reflect(self, execution_trace: Dict[str, Any], context: List[ContextItem]) -> ReflectionResult:
        """Analyze execution and extract insights"""
        pass


class Curator(ABC):
    """
    Curator: Manages context through incremental delta updates
    Replaces monolithic rewrites with localized edits
    """
    
    @abstractmethod
    def curate(self, current_context: List[ContextItem], 
              new_insights: List[str], 
              reflections: ReflectionResult) -> List[ContextItem]:
        """Update context with refined knowledge through delta updates"""
        pass


class ACEFramework:
    """
    Main ACE Framework orchestrator
    Coordinates Generator, Reflector, and Curator
    """
    
    def __init__(self, generator: Generator, reflector: Reflector, curator: Curator):
        self.generator = generator
        self.reflector = reflector
        self.curator = curator
        self.context: List[ContextItem] = []
        self.execution_history: List[Dict[str, Any]] = []
        self.refinement_threshold = 0.3  # Trigger refinement when redundancy exceeds this
        
    def add_context_item(self, item: ContextItem):
        """Add new context item"""
        self.context.append(item)
        
    def get_context_by_category(self, category: str) -> List[ContextItem]:
        """Retrieve context items by category"""
        return [item for item in self.context if item.category == category]
    
    def generate_strategies(self, task: str) -> List[str]:
        """Generate new strategies using Generator"""
        strategies = self.generator.generate(task, self.context)
        return strategies
    
    def reflect_on_execution(self, execution_trace: Dict[str, Any]) -> ReflectionResult:
        """Analyze execution using Reflector"""
        self.execution_history.append(execution_trace)
        reflections = self.reflector.reflect(execution_trace, self.context)
        return reflections
    
    def curate_context(self, reflections: ReflectionResult) -> List[ContextItem]:
        """Update context using Curator (incremental delta updates)"""
        # Convert insights to context items
        new_insights = [
            ContextItem(
                id=f"insight_{len(self.context)}_{i}",
                content=insight,
                category="insight",
                priority=0.8
            )
            for i, insight in enumerate(reflections.insights)
        ]
        
        # Curate context
        self.context = self.curator.curate(self.context, reflections.insights, reflections)
        
        # Periodic refinement (grow-and-refine mechanism)
        if len(self.context) > 20:  # Threshold for refinement
            self.refine_context()
        
        return self.context
    
    def refine_context(self):
        """
        Grow-and-Refine: Deduplicate and prune redundant context
        Balances context expansion with redundancy control
        """
        # Remove low-effectiveness, duplicate items
        sorted_context = sorted(
            self.context,
            key=lambda x: x.effectiveness_score * x.priority,
            reverse=True
        )
        
        # Keep top 50% or at least 10 items
        keep_count = max(10, len(sorted_context) // 2)
        self.context = sorted_context[:keep_count]
    
    def get_context_state(self) -> Dict[str, Any]:
        """Get current state of context"""
        return {
            "total_items": len(self.context),
            "by_category": {
                cat: len(self.get_context_by_category(cat))
                for cat in set(item.category for item in self.context)
            },
            "items": [item.to_dict() for item in self.context],
            "execution_history_count": len(self.execution_history)
        }
