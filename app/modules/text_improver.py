# ==========================================
# modules/recommendation_engine.py
# Text Improvement Recommendation System
# ==========================================

import requests
import os
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Simple recommendation engine that takes user input text and provides
    an improved version using Google Gemini API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the recommendation engine
        
        Args:
            api_key: Google AI Studio API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model = "gemini-1.5-flash"  # Use this instead of gemini-2.0-flash
        
        if not self.api_key:
            logger.warning("No API key provided. Set GOOGLE_API_KEY environment variable or pass api_key parameter")
    
    def get_recommendation(self, user_text: str) -> Dict:
        """
        Get text improvement recommendation
        
        Args:
            user_text: The text input by the user to improve
            
        Returns:
            Dictionary with recommendation results:
            {
                "success": bool,
                "original": str,
                "recommendation": str,
                "error": str (if failed)
            }
        """
        
        # Input validation
        if not user_text or not user_text.strip():
            return {
                "success": False,
                "error": "Please provide text to improve",
                "original": user_text,
                "recommendation": ""
            }
        
        if not self.api_key:
            return {
                "success": False,
                "error": "API key not configured",
                "original": user_text,
                "recommendation": ""
            }
        
        # Create recommendation prompt
        prompt = self._create_improvement_prompt(user_text.strip())
        
        try:
            # Make API call
            response = self._call_gemini_api(prompt)
            
            if response["success"]:
                return {
                    "success": True,
                    "original": user_text,
                    "recommendation": response["content"],
                    "error": ""
                }
            else:
                return {
                    "success": False,
                    "original": user_text,
                    "recommendation": "",
                    "error": response["error"]
                }
                
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return {
                "success": False,
                "original": user_text,
                "recommendation": "",
                "error": f"System error: {str(e)}"
            }
    
    def _create_improvement_prompt(self, text: str) -> str:
        """Create the prompt for text improvement"""
        
        return f"""
Please improve this text to make it more professional, clear, and constructive:

ORIGINAL TEXT: "{text}"

Requirements:
1. Fix any grammar, spelling, or punctuation errors
2. Replace vague language with specific, actionable feedback
3. Use professional and respectful tone
4. Make suggestions constructive rather than just critical
5. Ensure clarity and readability
6. Maintain the original intent and meaning

Provide only the improved text, nothing else.
"""
    
    def _call_gemini_api(self, prompt: str) -> Dict:
        """Make API call to Google Gemini"""
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent"
            
            headers = {"Content-Type": "application/json"}
            params = {"key": self.api_key}  # Use params instead of adding to URL
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 400,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            response = requests.post(url, params=params, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if "candidates" in result and result["candidates"]:
                    content = result["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "success": True,
                        "content": content.strip()
                    }
                else:
                    return {
                        "success": False,
                        "error": "No content generated by API"
                    }
            else:
                return {
                    "success": False,
                    "error": f"API error {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"API call failed: {str(e)}"
        }

# ==========================================
# CONVENIENCE FUNCTIONS FOR EASY INTEGRATION
# ==========================================

def get_text_recommendation(text: str, api_key: Optional[str] = None) -> str:
    """
    Simple function to get text recommendation
    
    Args:
        text: Text to improve
        api_key: Optional API key
        
    Returns:
        Improved text or error message
    """
    engine = RecommendationEngine(api_key)
    result = engine.get_recommendation(text)
    
    if result["success"]:
        return result["recommendation"]
    else:
        return f"Error: {result['error']}"

def get_detailed_recommendation(text: str, api_key: Optional[str] = None) -> Dict:
    """
    Get detailed recommendation with full response
    
    Args:
        text: Text to improve
        api_key: Optional API key
        
    Returns:
        Full recommendation dictionary
    """
    engine = RecommendationEngine(api_key)
    return engine.get_recommendation(text)

# ==========================================
# GRADIO INTERFACE INTEGRATION
# ==========================================

def create_gradio_recommendation_interface(api_key: Optional[str] = None):
    """
    Create Gradio interface for the recommendation engine
    
    Args:
        api_key: Optional API key for the engine
        
    Returns:
        Gradio Interface object
    """
    try:
        import gradio as gr
    except ImportError:
        raise ImportError("Gradio not installed. Install with: pip install gradio")
    
    engine = RecommendationEngine(api_key)
    
    def gradio_recommend(user_input):
        """Function for Gradio interface"""
        
        if not user_input or not user_input.strip():
            return "Please enter some text to get a recommendation."
        
        result = engine.get_recommendation(user_input)
        
        if result["success"]:
            return f"""**ORIGINAL:**
{result['original']}

**RECOMMENDATION:**
{result['recommendation']}"""
        else:
            return f"❌ {result['error']}"
    
    # Create interface
    interface = gr.Interface(
        fn=gradio_recommend,
        inputs=gr.Textbox(
            label="📝 Enter Text for Improvement",
            placeholder="Enter your text here for professional improvement recommendations...",
            lines=5
        ),
        outputs=gr.Textbox(
            label="✨ Recommendation",
            lines=10
        ),
        title="🎯 Text Improvement Recommendations",
        description="Get professional recommendations to improve your text quality, clarity, and tone.",
        examples=[
            ["john is okay worker but could be better at his job"],
            ["the meeting was fine but we need to discuss some issues"],
            ["sarah does good work sometimes but has room for improvement"],
            ["the project is going alright but there are some problems we should address"]
        ]
    )
    
    return interface

# ==========================================
# INTEGRATION WITH EXISTING MODULES
# ==========================================

def integrate_with_text_processor(text_processor, user_text: str, api_key: Optional[str] = None) -> Dict:
    """
    Integrate recommendation engine with your existing TextProcessor
    
    Args:
        text_processor: Your existing TextProcessor instance
        user_text: User input text
        api_key: Optional API key
        
    Returns:
        Combined analysis and recommendation
    """
    
    # Process text with your existing processor
    processed_data = text_processor.preprocess(user_text)
    
    # Get recommendation
    engine = RecommendationEngine(api_key)
    recommendation = engine.get_recommendation(user_text)
    
    # Extract linguistic features from spaCy doc
    doc = processed_data["doc"]
    
    # Analyze text characteristics
    word_count = len(processed_data["raw_text"].split())
    sentence_count = len(processed_data["sentences"])
    token_count = len(processed_data["tokens"]["input_ids"][0])
    
    # Get linguistic insights from spaCy
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    pos_tags = [(token.text, token.pos_) for token in doc if not token.is_space]
    
    return {
        "text_analysis": {
            "raw_text": processed_data["raw_text"],
            "sentences": processed_data["sentences"],
            "word_count": word_count,
            "sentence_count": sentence_count,
            "token_count": token_count,
            "entities": entities,
            "pos_tags": pos_tags[:10],  # First 10 POS tags
            "spacy_doc": doc  # Keep the spaCy doc for further analysis
        },
        "recommendation": recommendation,
        "success": recommendation["success"],
        "transformer_tokens": processed_data["tokens"]  # Keep transformer tokens
    }

# ==========================================
# EXAMPLE USAGE
# ==========================================

if __name__ == "__main__":
    
    # Example 1: Basic usage
    print("🔧 TESTING RECOMMENDATION ENGINE")
    print("=" * 40)
    
    # You would set your API key here
    API_KEY = "your-api-key-here"  # Replace with actual key
    
    # Test texts
    test_texts = [
        "john is okay worker but could be better",
        "the meeting was fine but we should talk about some stuff",
        "sarah good at her job sometimes but needs improvement"
    ]
    
    engine = RecommendationEngine(API_KEY)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Original: {text}")
        
        result = engine.get_recommendation(text)
        
        if result["success"]:
            print(f"Recommendation: {result['recommendation']}")
        else:
            print(f"Error: {result['error']}")
    
    # Example 2: Gradio interface
    print("\n🎨 CREATING GRADIO INTERFACE...")
    try:
        interface = create_gradio_recommendation_interface(API_KEY)
        print("🚀 Launching interface...")
        interface.launch()
    except Exception as e:
        print(f"Gradio interface error: {e}")
        print("Make sure gradio is installed: pip install gradio")