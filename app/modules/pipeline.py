# SAFE pipeline.py - Only adds text_improver, no other changes
from .textprocessor import TextProcessor
from .zero_shot_classification import ZeroShotAnalyzer
from .bias_detection import BiasDetector
from .specificity_analyzer import SpecificityAnalyzer
from .recommendation_engine import RecommendationEngine  # Your existing recommendation engine - UNCHANGED
from .vectorstore import VectorStore
from .feedbacktype import FeedbackTypeAnalyzer

# NEW IMPORT: Only addition - text improver module
try:
    from .text_improver import RecommendationEngine as TextImprover
except ImportError:
    TextImprover = None
    print("text_improver module not found - AI improvement will be disabled")

class PerformanceReviewAnalyzer:
    def __init__(self, google_api_key=None):
        # UNCHANGED: All your existing initialization
        self.text_processor = TextProcessor()
        self.zero_shot = ZeroShotAnalyzer()
        self.feedback_type = FeedbackTypeAnalyzer(self.zero_shot)
        self.bias_detector = BiasDetector(self.zero_shot)
        self.specificity_analyzer = SpecificityAnalyzer(self.zero_shot)
        
        # UNCHANGED: Your existing vectorstore logic
        try:
            self.vectorstore = VectorStore(host="localhost", port=8000)
        except ValueError as e:
            print(f"Error connecting to vectorstore: {e}. Using default settings.")
            # Fallback to default settings if connection fails
            self.vectorstore = VectorStore(host="app-performance-vectorstore-1", port=8000)
        
        # NEW: Only addition - optional text improver
        self.text_improver = None
        if google_api_key and TextImprover:
            try:
                self.text_improver = TextImprover(google_api_key)
            except Exception as e:
                print(f"Failed to initialize text improver: {e}")

    def analyze(self, review_text, objectives=None):  # UNCHANGED: Same signature
        # UNCHANGED: Your existing logic exactly as it was
        if not review_text.strip():
            return {
                "error": "No review text provided"
            }

        # UNCHANGED: Process text
        processed = self.text_processor.preprocess(review_text)

        # UNCHANGED: Check alignment with objectives if provided
        objective_alignment = None

        # UNCHANGED: Combine all analysis results
        analysis_results = {
            "biases": self.bias_detector.detect_bias(processed),
            "specificities": self.specificity_analyzer.analyze_specificity(processed),
            "feedbacks": self.feedback_type.feedback_type(processed),
            "objectives": objective_alignment
        }

        # UNCHANGED: Generate recommendations using your existing RecommendationEngine
        recommender = RecommendationEngine(analysis_results)
        recommendations = {
            "bias": recommender.generate_table_bias(),
            "specificity": recommender.generate_table_specificity(),
            "feedback": recommender.generate_table_feedback()
        }

        # UNCHANGED: Your existing return structure
        base_result = {
            "analysis": analysis_results,
            "recommendations": recommendations
        }

        # NEW: Optional AI improvement (only addition - doesn't affect existing functionality)
        if self.text_improver:
            try:
                ai_result = self.text_improver.get_recommendation(review_text)
                base_result["ai_improvement"] = ai_result
            except Exception as e:
                base_result["ai_improvement"] = {
                    "success": False,
                    "error": f"AI improvement failed: {str(e)}"
                }
        else:
            base_result["ai_improvement"] = {
                "success": False,
                "error": "AI improvement not available"
            }

        return base_result

    # NEW: Optional method - doesn't affect existing functionality
    def get_ai_improvement_only(self, review_text):
        """Optional method to get only AI improvement"""
        if self.text_improver:
            return self.text_improver.get_recommendation(review_text)
        else:
            return {
                "success": False,
                "error": "AI improvement not configured"
            }