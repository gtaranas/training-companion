"""
Unit tests for ACE Framework components
"""

import unittest
from ace_framework import (
    ContextItem, ReflectionResult, Generator, Reflector, Curator, ACEFramework
)


class TestContextItem(unittest.TestCase):
    """Test ContextItem functionality"""
    
    def test_context_item_creation(self):
        """Test creating a context item"""
        item = ContextItem(
            id="test_1",
            content="Test insight",
            category="insight",
            priority=0.9
        )
        self.assertEqual(item.content, "Test insight")
        self.assertEqual(item.category, "insight")
        self.assertEqual(item.priority, 0.9)
        self.assertEqual(item.effectiveness_score, 0.5)  # Default
    
    def test_context_item_effectiveness_update(self):
        """Test effectiveness scoring"""
        item = ContextItem(
            id="test_2",
            content="Test pattern",
            category="pattern"
        )
        
        # Initial score
        initial_score = item.effectiveness_score
        
        # Update with success
        item.update_effectiveness(success=True, impact=1.0)
        self.assertGreater(item.effectiveness_score, initial_score)
        
        # Update with failure
        item.update_effectiveness(success=False, impact=1.0)
        self.assertLess(item.effectiveness_score, 1.0)
        self.assertGreater(item.effectiveness_score, 0.0)
    
    def test_context_item_to_dict(self):
        """Test converting context item to dictionary"""
        item = ContextItem(
            id="test_3",
            content="Test",
            category="strategy"
        )
        
        item_dict = item.to_dict()
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['id'], "test_3")
        self.assertEqual(item_dict['content'], "Test")


class TestReflectionResult(unittest.TestCase):
    """Test ReflectionResult dataclass"""
    
    def test_reflection_result_creation(self):
        """Test creating reflection result"""
        result = ReflectionResult(
            insights=["Insight 1", "Insight 2"],
            patterns=[{"pattern": "Recent form"}],
            failures=[{"failure": "Ignored injury"}],
            recommendations=["Recommendation 1"],
            context_gaps=["Missing data"]
        )
        
        self.assertEqual(len(result.insights), 2)
        self.assertEqual(len(result.patterns), 1)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(len(result.recommendations), 1)
        self.assertEqual(len(result.context_gaps), 1)


class MockGenerator(Generator):
    """Mock Generator for testing"""
    
    def generate(self, task: str, context) -> list:
        return ["Strategy 1", "Strategy 2"]


class MockReflector(Reflector):
    """Mock Reflector for testing"""
    
    def reflect(self, execution_trace: dict, context) -> ReflectionResult:
        return ReflectionResult(
            insights=["Test insight"],
            patterns=[],
            failures=[],
            recommendations=["Test recommendation"],
            context_gaps=[]
        )


class MockCurator(Curator):
    """Mock Curator for testing"""
    
    def curate(self, current_context: list, new_insights: list, reflections) -> list:
        # Add new insights
        for insight in new_insights:
            item = ContextItem(
                id=f"mock_{len(current_context)}",
                content=insight,
                category="insight"
            )
            current_context.append(item)
        return current_context


class TestACEFramework(unittest.TestCase):
    """Test ACE Framework orchestration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = MockGenerator()
        self.reflector = MockReflector()
        self.curator = MockCurator()
        self.ace = ACEFramework(self.generator, self.reflector, self.curator)
    
    def test_ace_initialization(self):
        """Test ACE framework initialization"""
        self.assertIsNotNone(self.ace.generator)
        self.assertIsNotNone(self.ace.reflector)
        self.assertIsNotNone(self.ace.curator)
        self.assertEqual(len(self.ace.context), 0)
    
    def test_add_context_item(self):
        """Test adding context items"""
        item = ContextItem(
            id="test_1",
            content="Test",
            category="strategy"
        )
        
        self.ace.add_context_item(item)
        self.assertEqual(len(self.ace.context), 1)
    
    def test_generate_strategies(self):
        """Test strategy generation"""
        strategies = self.ace.generate_strategies("Test task")
        self.assertEqual(len(strategies), 2)
        self.assertIn("Strategy 1", strategies)
    
    def test_reflect_on_execution(self):
        """Test reflection on execution"""
        execution_trace = {
            "match": "Test vs Test",
            "prediction": "Draw",
            "actual_outcome": "Home Win",
            "confidence": 0.7
        }
        
        reflections = self.ace.reflect_on_execution(execution_trace)
        self.assertIsInstance(reflections, ReflectionResult)
        self.assertGreater(len(reflections.insights), 0)
    
    def test_curate_context(self):
        """Test context curation"""
        reflections = ReflectionResult(
            insights=["New insight"],
            patterns=[],
            failures=[],
            recommendations=["New recommendation"],
            context_gaps=[]
        )
        
        initial_count = len(self.ace.context)
        self.ace.context = self.curator.curate(
            self.ace.context, 
            reflections.insights, 
            reflections
        )
        
        # Context should have grown
        self.assertGreater(len(self.ace.context), initial_count)
    
    def test_get_context_state(self):
        """Test getting context state"""
        item = ContextItem(
            id="test_1",
            content="Test",
            category="strategy"
        )
        self.ace.add_context_item(item)
        
        state = self.ace.get_context_state()
        self.assertIn("total_items", state)
        self.assertIn("by_category", state)
        self.assertEqual(state["total_items"], 1)


if __name__ == "__main__":
    unittest.main()
