import gradio as gr
import torch
from modules.pipeline import PerformanceReviewAnalyzer
from modules.vizualisations import visualize_feedback_types, display_analysis_summary, visualize_objective_alignment
import pandas as pd
import os

# OPTIONAL: Add Google API key for AI text improvement
GOOGLE_API_KEY = os.getenv["GOOGLE_API_KEY"]  # ← PASTE YOUR API KEY HERE IF YOU WANT AI IMPROVEMENT

# Create analyzer instances
analyzer = PerformanceReviewAnalyzer()  # Your existing analyzer (unchanged)
analyzer_with_ai = None

# Setup AI analyzer if API key provided
if GOOGLE_API_KEY:
    try:
        analyzer_with_ai = PerformanceReviewAnalyzer(google_api_key=GOOGLE_API_KEY)
        print("✅ AI Text Improvement: ENABLED")
    except Exception as e:
        print(f"❌ AI Text Improvement error: {e}")
else:
    print("ℹ️ AI Text Improvement: DISABLED (no API key provided)")

# UNCHANGED: Your existing analysis function
def analyze_review(review_text):
    if not review_text:
        return "Please enter some review text to analyze.", pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # UNCHANGED: Exactly your existing logic
    results = analyzer.analyze(review_text, objectives=None)
    outputs = [pd.DataFrame(data) if data is not None else pd.DataFrame({"sentence": [], "label": [], "intensity": [], "prediction": [], "recommendation":[]}) for data in results["recommendations"].values()]

    return "✅ Analysis completed successfully!", outputs[0], outputs[1], outputs[2]

# NEW: Function to generate AI recommendation using the same text
def generate_ai_recommendation(review_text):
    if not review_text or not review_text.strip():
        return "Please enter review text first and click 'Analyze Review'."
    
    if not analyzer_with_ai:
        return "❌ AI recommendations not available. Please configure your Google API key."
    
    try:
        # Get AI improvement using the same text that was analyzed
        ai_result = analyzer_with_ai.get_ai_improvement_only(review_text)
        
        if ai_result["success"]:
            return f"""**ORIGINAL TEXT:**
{ai_result['original']}

**AI IMPROVED VERSION:**
{ai_result['recommendation']}

---
✨ *Professional improvement suggestions based on your analysis*"""
        else:
            return f"❌ Error generating recommendation: {ai_result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Check if GPU is available (unchanged)
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")
    print("Using CPU")

# Create Gradio interface - simplified with single input
with gr.Blocks(title="Performance Review Analysis System") as demo:
    
    # Title and description
    gr.Markdown("# 🎯 Performance Review Analysis System")
    gr.Markdown("""
    **Analyze performance reviews and get AI-powered improvement suggestions**
    
    📈 **Analysis Features:** Bias detection • Specificity assessment • Feedback type classification  
    ✨ **AI Improvement:** Professional text enhancement and recommendations
    """)
    
    # Single input section
    review_input = gr.Textbox(
        lines=8, 
        label="📝 Performance Review Text", 
        placeholder="Enter your performance review text here..."
    )
    
    # Buttons section
    with gr.Row():
        analyze_btn = gr.Button("📊 Analyze Review", variant="primary", size="lg")
        recommend_btn = gr.Button("✨ Generate AI Recommendation", variant="secondary", size="lg")
    
    # Status message
    status_output = gr.Textbox(label="📋 Status", interactive=False)
    
    # Analysis outputs (your existing ones)
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📈 Analysis Results")
            bias_output = gr.DataFrame(label="🎯 Bias Analysis")
            specificity_output = gr.DataFrame(label="📏 Specificity Analysis")
            feedback_output = gr.DataFrame(label="💬 Feedback Type Analysis")
        
        with gr.Column():
            gr.Markdown("### ✨ AI Recommendations")
            recommendation_output = gr.Textbox(
                label="🤖 Professional Text Improvement",
                lines=12,
                show_copy_button=True,
                placeholder="Click 'Generate AI Recommendation' after analyzing your text..."
            )
    
    # Examples section
    gr.Markdown("### 💡 Try These Examples:")
    gr.Examples(
        examples=[
            ["john is okay worker but could be better at his job and presentations"],
            ["sarah does good work sometimes but has room for improvement in communication"],
            ["ricardo excellent performance very professional outstanding results highly recommended"],
            ["needs improvement in several areas including time management and teamwork skills"]
        ],
        inputs=[review_input],
        label="Click any example to test:"
    )
    
    # Button click handlers
    analyze_btn.click(
        fn=analyze_review,
        inputs=[review_input],
        outputs=[status_output, bias_output, specificity_output, feedback_output]
    )
    
    recommend_btn.click(
        fn=generate_ai_recommendation,
        inputs=[review_input],  # Uses the same input text
        outputs=[recommendation_output]
    )
    
    # Simple instructions
    gr.Markdown("""
    ### 🔧 How to Use:
    1. **📝 Enter** your performance review text above
    2. **📊 Click "Analyze Review"** to get detailed analysis  
    3. **✨ Click "Generate AI Recommendation"** to get improved version of the same text
    4. **📋 Copy** the improved text using the copy button
    """)

# Launch the interface (unchanged)
demo.launch(server_name="0.0.0.0", debug=True, share=True, server_port=7860)
