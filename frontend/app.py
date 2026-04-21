import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import base64
from io import StringIO
import pandas as pd

# Language options with native names
LANGUAGE_OPTIONS = {
    "en": "English",
    "kn": "ಕನ್ನಡ", 
    "ta": "தமிழ்",
    "te": "తెలుగు"
}

def get_json_download_link(feedback: Dict[str, Any], filename: str = "essay_feedback.json") -> str:
    """Generate a download link for the feedback JSON."""
    json_str = json.dumps(feedback, indent=2, ensure_ascii=False)
    b64 = base64.b64encode(json_str.encode()).decode()
    return f'<a href="data:application/json;base64,{b64}" download="{filename}" class="download-button">⬇️ Download JSON Report</a>'

def get_text_download_link(text: str, filename: str = "essay_feedback.txt") -> str:
    """Generate a download link for the text report."""
    b64 = base64.b64encode(text.encode('utf-8')).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-button">📄 Download TXT Report</a>'

def generate_text_report(feedback: Dict[str, Any]) -> str:
    """Generate a readable text report from feedback."""
    report = []
    report.append("=" * 60)
    report.append("ESSAY GRADING REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Score
    score = feedback.get('predicted_score', 0)
    report.append(f"SCORE: {score:.1f}/10")
    report.append("")
    
    # Language
    lang = feedback.get('selected_language', 'Unknown')
    report.append(f"LANGUAGE: {lang.upper()}")
    report.append("")
    
    # Strengths
    if 'strengths' in feedback and feedback['strengths']:
        report.append("STRENGTHS:")
        report.append("-" * 20)
        for i, strength in enumerate(feedback['strengths'], 1):
            report.append(f"{i}. {strength}")
        report.append("")
    
    # Weaknesses
    if 'weaknesses' in feedback and feedback['weaknesses']:
        report.append("WEAKNESSES:")
        report.append("-" * 20)
        for i, weakness in enumerate(feedback['weaknesses'], 1):
            report.append(f"{i}. {weakness}")
        report.append("")
    
    # Suggestions
    if 'suggestions' in feedback and feedback['suggestions']:
        report.append("SUGGESTIONS FOR IMPROVEMENT:")
        report.append("-" * 35)
        for i, suggestion in enumerate(feedback['suggestions'], 1):
            report.append(f"{i}. {suggestion}")
        report.append("")
    
    # Readability metrics
    if 'readability' in feedback:
        metrics = feedback['readability']
        report.append("READABILITY METRICS:")
        report.append("-" * 25)
        report.append(f"Word Count: {metrics.get('word_count', 0)}")
        report.append(f"Sentence Count: {metrics.get('sentence_count', 0)}")
        report.append(f"Avg Word Length: {metrics.get('avg_word_length', 0):.1f} characters")
        report.append(f"Avg Sentence Length: {metrics.get('avg_sentence_length', 0):.1f} words")
        report.append("")
    
    # Sentiment
    if 'sentiment' in feedback:
        sentiment = feedback['sentiment']
        report.append("SENTIMENT ANALYSIS:")
        report.append("-" * 22)
        report.append(f"Positive: {sentiment.get('positive', 0):.1f}%")
        report.append(f"Neutral: {sentiment.get('neutral', 0):.1f}%")
        report.append(f"Negative: {sentiment.get('negative', 0):.1f}%")
        report.append(f"Sentiment Score: {sentiment.get('compound', 0):.2f}")
        report.append("")
    
    # Language compliance
    if 'language_compliance' in feedback:
        compliance = feedback['language_compliance']
        report.append("LANGUAGE COMPLIANCE:")
        report.append("-" * 24)
        report.append(f"Compliance Score: {compliance.get('compliance_score', 0):.1f}%")
        report.append(f"Violations: {len(compliance.get('violations', []))}")
        if compliance.get('violations'):
            for violation in compliance['violations']:
                report.append(f"  - {violation}")
        report.append("")
    
    report.append("=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)
    
    return "\n".join(report)

def display_bias_analysis(bias_data: Dict[str, Any]) -> None:
    """Display bias analysis results."""
    if not bias_data:
        return
        
    with st.expander("⚖️ Bias Analysis", expanded=True):
        st.markdown("### 🎯 Potential Bias Detection")
        
        # Overall bias score
        bias_score = bias_data.get('bias_score', 0) * 100
        bias_level = "Low" if bias_score < 30 else "Moderate" if bias_score < 70 else "High"
        bias_color = "#4CAF50" if bias_score < 30 else "#FFC107" if bias_score < 70 else "#F44336"
        
        st.metric("Overall Bias Score", 
                 f"{bias_score:.1f}%", 
                 help="Lower scores indicate less bias (0-30%: Low, 30-70%: Moderate, 70-100%: High)")
        
        # Bias categories
        if 'bias_categories' in bias_data and bias_data['bias_categories']:
            st.markdown("#### 📊 Bias by Category")
            bias_categories = bias_data['bias_categories']
            
            # Create a horizontal bar chart for bias categories
            categories = list(bias_categories.keys())
            values = [bias_categories[cat].get('score', 0) * 100 for cat in categories]
            colors = ['#4CAF50' if v < 30 else '#FFC107' if v < 70 else '#F44336' for v in values]
            
            fig = go.Figure(go.Bar(
                x=values,
                y=categories,
                orientation='h',
                marker_color=colors,
                text=[f"{v:.1f}%" for v in values],
                textposition='auto'
            ))
            
            fig.update_layout(
                xaxis_title="Bias Score (%)",
                yaxis_title="Category",
                height=200 + len(categories) * 30,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show bias examples if available
            for category, data in bias_categories.items():
                if data.get('score', 0) > 0.3 and data.get('examples'):  # Only show if significant bias
                    with st.expander(f"ℹ️ {category} Bias Examples", expanded=False):
                        st.markdown("**Examples of potentially biased phrases:**")
                        for example in data.get('examples', [])[:3]:  # Show max 3 examples
                            st.markdown(f"- `{example}`")
        
        # Mitigation suggestions
        if 'mitigation_suggestions' in bias_data and bias_data['mitigation_suggestions']:
            st.markdown("#### 💡 Bias Mitigation Suggestions")
            for suggestion in bias_data['mitigation_suggestions']:
                st.markdown(f"- {suggestion}")
        
        # Additional context
        st.markdown("""
        <div style="margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
            <small>💡 <strong>Note:</strong> Bias detection is based on statistical analysis of language patterns. 
            Some bias may be contextually appropriate. Always review suggestions critically.</small>
        </div>
        """, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Essay Grader",
    page_icon="📝",
    layout="wide"
)

# Custom CSS for better visibility and light theme
st.markdown("""
    <style>
        /* Main app background - PROFESSIONAL GRAY */
        .stApp {
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
        }
        
        /* All text elements - dark text on light background */
        .stText, .stMarkdown, .stAlert p, .stTextInput, 
        .stTextArea, .stSelectbox, .stSlider, .stNumberInput,
        p, h1, h2, h3, h4, h5, h6, span, div {
            color: #1f1f1f !important;
        }
        
        /* Fix Streamlit containers */
        .css-1d391kg, .css-1v3fvcr, .css-1r6slb0,
        .css-1lcbmhc, .css-1outpf7, .css-1e5drgg {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid #e1e5e9;
        }
        
        /* Input fields styling - MORE AGGRESSIVE */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        input[type="text"], textarea, select {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
            border: 2px solid #e1e5e9 !important;
            border-radius: 4px !important;
            -webkit-appearance: none !important;
            appearance: none !important;
        }
        
        /* Focus states for inputs */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
            border-color: #2196f3 !important;
            box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
        }
        
        /* Sidebar - MORE AGGRESSIVE */
        .css-1d391kg, .css-1lcbmhc, .css-1outpf7,
        .element-container .stSidebar, .stSidebar {
            background-color: #f8f9fa !important;
            color: #1f1f1f !important;
            border: 1px solid #e1e5e9 !important;
        }
        
        /* Sidebar content */
        .stSidebar .stMarkdown, .stSidebar .stText,
        .stSidebar p, .stSidebar h1, .stSidebar h2, .stSidebar h3,
        .stSidebar h4, .stSidebar h5, .stSidebar h6,
        .stSidebar span, .stSidebar div {
            background-color: #f8f9fa !important;
            color: #1f1f1f !important;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #d4edda !important;
            color: #155724 !important;
            border-left: 4px solid #28a745 !important;
        }
        
        /* Error messages */
        .stError {
            background-color: #f8d7da !important;
            color: #721c24 !important;
            border-left: 4px solid #dc3545 !important;
        }
        
        /* Warning messages */
        .stWarning {
            background-color: #fff3cd !important;
            color: #856404 !important;
            border-left: 4px solid #ffc107 !important;
        }
        
        /* Info messages */
        .stInfo {
            background-color: #d1ecf1 !important;
            color: #0c5460 !important;
            border-left: 4px solid #17a2b8 !important;
        }
        
        /* Style for suggestion boxes */
        .suggestion-box {
            background-color: #f8f9fa !important;
            border-left: 4px solid #4CAF50 !important;
            padding: 15px !important;
            margin: 10px 0 !important;
            border-radius: 4px !important;
            color: #1f1f1f !important;
            border: 1px solid #e1e5e9 !important;
        }
        
        /* Score display - PROFESSIONAL THEME */
        .score-display {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #7f8c8d 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 25px !important;
            text-align: center !important;
            color: #ffffff !important;
            font-size: 28px !important;
            font-weight: bold !important;
            box-shadow: 0 8px 32px rgba(44, 62, 80, 0.2) !important;
            margin: 20px 0 !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .score-display::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%) !important;
        }
        
        /* Feedback sections - PROFESSIONAL THEME */
        .feedback-section {
            background: #ffffff !important;
            border: 2px solid #e9ecef !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            color: #2c3e50 !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
        }
        
        .feedback-section:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1) !important;
            border-color: #6c757d !important;
        }
        
        /* Strengths section - PROFESSIONAL GREEN */
        .strengths-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
            border-left: 5px solid #28a745 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            color: #2c3e50 !important;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.1) !important;
        }
        
        /* Weaknesses section - PROFESSIONAL AMBER */
        .weaknesses-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
            border-left: 5px solid #ffc107 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            color: #2c3e50 !important;
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.1) !important;
        }
        
        /* Suggestions section - PROFESSIONAL BLUE */
        .suggestions-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
            border-left: 5px solid #007bff !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            color: #2c3e50 !important;
            box-shadow: 0 4px 15px rgba(0, 123, 255, 0.1) !important;
        }
        
        /* Evaluation report - PROFESSIONAL */
        .evaluation-report {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
            border: 2px solid #dee2e6 !important;
            border-radius: 12px !important;
            padding: 25px !important;
            margin: 20px 0 !important;
            color: #2c3e50 !important;
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.05) !important;
            position: relative !important;
        }
        
        .evaluation-report pre {
            background: #f8f9fa !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 8px !important;
            padding: 20px !important;
            color: #2c3e50 !important;
            white-space: pre-wrap !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
            margin: 15px 0 !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.03) !important;
        }
        
        /* Section headers - PROFESSIONAL */
        .section-header {
            background: linear-gradient(135deg, #495057 0%, #6c757d 100%) !important;
            color: #ffffff !important;
            padding: 15px 20px !important;
            border-radius: 8px 8px 0 0 !important;
            margin: -20px -20px 15px -20px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
        }
        
        /* Metrics cards - PROFESSIONAL */
        .metric-card {
            background: #ffffff !important;
            border: 2px solid #dee2e6 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            text-align: center !important;
            color: #2c3e50 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .metric-card:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
            border-color: #6c757d !important;
        }
        
        .metric-card .metric-value {
            font-size: 32px !important;
            font-weight: bold !important;
            color: #495057 !important;
            margin: 10px 0 !important;
        }
        
        .metric-card .metric-label {
            font-size: 14px !important;
            color: #6c757d !important;
            font-weight: 600 !important;
        }
        
        /* Expander headers specifically */
        .streamlit-expanderHeader, .st-expander-header {
            background-color: #f8f9fa !important;
            color: #1f1f1f !important;
            border-bottom: 1px solid #e1e5e9 !important;
        }
        
        /* Expander content specifically */
        .streamlit-expanderContent, .st-expander-content {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
            padding: 15px !important;
        }
        
        /* All containers and elements - NUCLEAR OPTION */
        div, section, article, main, aside, header, footer, nav {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
        }
        
        /* Override main containers - PROFESSIONAL BACKGROUND */
        [data-testid="stAppViewContainer"], 
        [data-testid="stMain"] {
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
        }
        
        /* Keep sidebar white */
        [data-testid="stSidebarContent"],
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            color: #1f1f1f !important;
        }
        
        /* Download button style - ENHANCED */
        .download-button {
            display: inline-block !important;
            padding: 12px 24px !important;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
            color: white !important;
            text-decoration: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            font-size: 14px !important;
            margin-top: 1rem !important;
            text-align: center !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3) !important;
            min-width: 200px !important;
        }
        .download-button:hover {
            background: linear-gradient(135deg, #218838 0%, #1ea085 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4) !important;
            color: white !important;
            text-decoration: none !important;
        }
        
        /* Fix any remaining dark backgrounds */
        .element-container, .block-container, .main {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa !important;
            color: #1f1f1f !important;
        }
        
        /* Ensure all cards have proper background */
        .css-1lcbmhc, .css-1outpf7 {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
            border-radius: 8px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            border: 1px solid #e1e5e9 !important;
        }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"  # Updated to port 8000
def display_validation_errors(error_response: Dict[str, Any]) -> None:
    """Display validation errors from the backend."""
    st.error("🚫 Validation Failed")
    
    if error_response.get('language_violation'):
        st.error(f"""
        **LANGUAGE VIOLATION DETECTED**
        
        {error_response.get('message', 'Language mismatch detected')}
        
        - **Detected Language**: {LANGUAGE_OPTIONS.get(error_response.get('detected_language', 'en'), error_response.get('detected_language', 'Unknown'))}
        - **Selected Language**: {LANGUAGE_OPTIONS.get(error_response.get('selected_language', 'en'), error_response.get('selected_language', 'Unknown'))}
        
        **STRICT SYSTEM RULE**: Essay language must match the selected language. Please rewrite your essay in the correct language.
        """)
    
    if 'content_issues' in error_response:
        st.error("""
        **CONTENT VALIDATION FAILED**
        
        Issues found:
        """)
        for issue in error_response['content_issues']:
            st.markdown(f"- {issue}")
        
        st.markdown(f"""
        **Content Metrics:**
        - Word Count: {error_response.get('word_count', 0)}
        - Sentence Count: {error_response.get('sentence_count', 0)}
        """)
    
    if 'violations' in error_response:
        st.error("""
        **LANGUAGE COMPLIANCE VIOLATION**
        
        The system detected violations of the strict language rules:
        """)
        for violation in error_response['violations']:
            st.markdown(f"- {violation}")

def display_feedback(feedback: Dict[str, Any]) -> None:
    """Display feedback in a user-friendly way."""
    if not feedback:
        st.error("No feedback received from the server.")
        return

    # Score and Language - ENHANCED DISPLAY
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 Your Essay Score</div>
            <div class="metric-value">{feedback.get('predicted_score', 0):.1f}/10</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        lang_display = LANGUAGE_OPTIONS.get(
            feedback.get('selected_language', 'en'),
            "English"
        )
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🌐 Language</div>
            <div class="metric-value">{lang_display}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display validation status
    if feedback.get('validation_passed') and feedback.get('language_rules_followed'):
        st.success("✅ All validation rules passed")
        st.success("🌐 Language compliance verified")
    
    # Display strict response (formatted according to language rules)
    if 'strict_response' in feedback:
        with st.expander("📋 Strict Evaluation (Language-Rules Compliant)", expanded=True):
            st.markdown("""
            <div class="evaluation-report">
                <div class="section-header">
                    ✅ STRICT SYSTEM RULES FOLLOWED
                </div>
                <div style="padding: 0 20px;">
                    This response is generated exclusively in the selected language with no language mixing.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📝 Evaluation Report")
            st.markdown(f"""
            <div class="evaluation-report">
                <div class="section-header">
                    📋 Full Evaluation Report
                </div>
                <pre>{feedback['strict_response']}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Show language compliance details
            if 'language_compliance' in feedback:
                compliance = feedback['language_compliance']
                st.markdown("#### 🔍 Language Compliance Check")
                if compliance.get('is_compliant'):
                    st.success("✅ Response follows strict language rules")
                else:
                    st.error("❌ Language rule violations detected")
                    if 'violations' in compliance:
                        for violation in compliance['violations']:
                            st.markdown(f"- {violation}")
    
    # Display strengths and weaknesses separately - ENHANCED
    if 'strengths' in feedback and feedback['strengths']:
        with st.expander("💪 Strengths", expanded=True):
            st.markdown('<div class="strengths-section">', unsafe_allow_html=True)
            for strength in feedback['strengths']:
                st.markdown(f"""
                <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.7); border-radius: 6px;">
                    ✅ {strength}
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    if 'weaknesses' in feedback and feedback['weaknesses']:
        with st.expander("⚠️ Weaknesses", expanded=True):
            st.markdown('<div class="weaknesses-section">', unsafe_allow_html=True)
            for weakness in feedback['weaknesses']:
                st.markdown(f"""
                <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.7); border-radius: 6px;">
                    ❌ {weakness}
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Grammar Analysis
    with st.expander("🔍 Grammar Analysis", expanded=True):
        if 'grammar' in feedback:
            try:
                grammar = feedback['grammar']
                grammar_score = grammar.get('score', 0.8)
                
                # Display grammar score with progress bar
                st.markdown("### 📊 Grammar Score")
                st.progress(min(grammar_score, 1.0))
                st.write(f"Grammar Quality: {grammar_score*100:.1f}%")
                
                # Display grammar issues if any
                if 'issues' in grammar and grammar['issues']:
                    st.markdown("### ⚠️ Grammar Issues Found:")
                    for issue in grammar['issues']:
                        st.warning(issue)
                else:
                    st.success("✅ No grammar issues detected! Your writing is grammatically sound.")
                
                # Add additional grammar insights
                st.markdown("### 📝 Grammar Insights:")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Grammar Score", f"{grammar_score*100:.1f}%")
                    st.metric("Issues Found", len(grammar.get('issues', [])))
                
                with col2:
                    if grammar_score >= 0.8:
                        st.success("🌟 Excellent Grammar")
                    elif grammar_score >= 0.6:
                        st.info("👍 Good Grammar")
                    else:
                        st.warning("⚠️ Needs Improvement")
                        
            except Exception as grammar_error:
                st.info("Grammar analysis unavailable")
                st.write("Error processing grammar data")
        else:
            st.info("No grammar analysis data available")
            st.write("Grammar analysis couldn't be performed on this essay")

    # Readability Metrics
    with st.expander("📖 Readability Metrics", expanded=True):
        if 'readability' in feedback:
            metrics = feedback['readability']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Word Count", metrics.get('word_count', 0))
            with col2:
                st.metric("Sentence Count", metrics.get('sentence_count', 0))
            with col3:
                st.metric("Avg Word Length", f"{metrics.get('avg_word_length', 0):.1f} chars")
            with col4:
                st.metric("Avg Sentence Length", f"{metrics.get('avg_sentence_length', 0):.1f} words")

    # Sentiment Analysis with Pie Chart
    with st.expander("😊 Sentiment Analysis", expanded=True):
        if 'sentiment' in feedback:
            try:
                sentiment = feedback['sentiment']
                
                # Create a two-column layout
                col1, col2 = st.columns([1, 2])
                
                # Left column for metrics
                with col1:
                    st.metric("Positive", f"{sentiment.get('positive', 0)*100:.1f}%")
                    st.metric("Neutral", f"{sentiment.get('neutral', 0)*100:.1f}%")
                    st.metric("Negative", f"{sentiment.get('negative', 0)*100:.1f}%")
                    st.metric("Sentiment Score", f"{sentiment.get('compound', 0):.2f}")
                
                # Right column for the pie chart
                with col2:
                    try:
                        # Create pie chart data
                        sentiment_data = {
                            'Positive': sentiment.get('positive', 0) * 100,
                            'Neutral': sentiment.get('neutral', 0) * 100,
                            'Negative': sentiment.get('negative', 0) * 100
                        }
                        
                        # Filter out zero values to avoid chart issues
                        filtered_data = {k: v for k, v in sentiment_data.items() if v > 0}
                        
                        if filtered_data:
                            try:
                                # Try pie chart first
                                fig = px.pie(
                                    values=list(filtered_data.values()),
                                    names=list(filtered_data.keys()),
                                    title="Sentiment Distribution",
                                    color_discrete_map={
                                        'Positive': '#2E8B57', 
                                        'Neutral': '#FFD700', 
                                        'Negative': '#DC143C'
                                    }
                                )
                                
                                # Update layout for better display
                                fig.update_traces(
                                    textposition='inside', 
                                    textinfo='percent+label',
                                    textfont_size=12
                                )
                                fig.update_layout(
                                    font=dict(size=12),
                                    showlegend=True,
                                    height=350,
                                    margin=dict(l=20, r=20, t=40, b=20)
                                )
                                
                                # Display the chart
                                st.plotly_chart(fig, use_container_width=True)
                                
                            except Exception as pie_error:
                                # Fallback to bar chart
                                st.write("**Using Bar Chart (Pie Chart Failed):**")
                                fig_bar = px.bar(
                                    x=list(filtered_data.keys()),
                                    y=list(filtered_data.values()),
                                    title="Sentiment Distribution",
                                    color=list(filtered_data.keys()),
                                    color_discrete_map={
                                        'Positive': '#2E8B57', 
                                        'Neutral': '#FFD700', 
                                        'Negative': '#DC143C'
                                    }
                                )
                                fig_bar.update_layout(
                                    height=350,
                                    margin=dict(l=20, r=20, t=40, b=20),
                                    showlegend=False
                                )
                                fig_bar.update_yaxes(title_text="Percentage (%)")
                                fig_bar.update_xaxes(title_text="")
                                st.plotly_chart(fig_bar, use_container_width=True)
                        else:
                            st.info("No sentiment data to display")
                            
                    except Exception as chart_error:
                        st.info("Chart rendering unavailable")
                        # Show data as text fallback
                        st.write("**Sentiment Breakdown:**")
                        for sentiment_type, percentage in sentiment_data.items():
                            st.write(f"- {sentiment_type}: {percentage:.1f}%")
                        
            except Exception as sentiment_error:
                st.info("Sentiment analysis unavailable")
                st.write("Error processing sentiment data")
        else:
            st.info("No sentiment analysis data available")

    # Bias Analysis Section
    if 'bias_analysis' in feedback:
        display_bias_analysis(feedback['bias_analysis'])

    # Plagiarism Check
    with st.expander("🔎 Plagiarism Check", expanded=True):
        if 'plagiarism' in feedback:
            plagiarism = feedback['plagiarism']
            similarity = plagiarism.get('similarity_score', 0) * 100
            if similarity > 80:
                st.error(f"Similarity Score: {similarity:.1f}% - ⚠️ Potential plagiarism detected!")
            else:
                st.success(f"Similarity Score: {similarity:.1f}% - ✅ No plagiarism detected")

    # Suggestions
    with st.expander("💡 Suggestions for Improvement", expanded=True):
        if 'suggestions' in feedback and feedback['suggestions']:
            for suggestion in feedback['suggestions']:
                st.markdown(f'<div class="suggestion-box">✨ {suggestion}</div>', 
                           unsafe_allow_html=True)
        else:
            st.info("No specific suggestions available. Your essay looks good!")

    # Download Full Report
    st.markdown("---")
    st.markdown("### 📥 Download Full Report")
    
    # Create two download options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(get_json_download_link(feedback, "essay_feedback.json"), unsafe_allow_html=True)
    
    with col2:
        # Create PDF-like text report
        text_report = generate_text_report(feedback)
        st.markdown(get_text_download_link(text_report, "essay_feedback.txt"), unsafe_allow_html=True)
    
    st.info("💡 **Download Options:** Choose JSON for technical data or TXT for readable report")

def main():
    st.title("📝 Essay Grader")
    st.markdown("Get detailed feedback on your essay with our AI-powered grading system.")

    # Language selection with native names
    target_lang = st.selectbox(
        "Select Essay Language (STRICT: Essay must be written in this language)",
        options=list(LANGUAGE_OPTIONS.keys()),
        format_func=lambda x: LANGUAGE_OPTIONS[x],
        index=0,
        
    )
    # Essay input
    essay = st.text_area("Paste your essay here:", height=300)

    if st.button("Grade My Essay", type="primary"):
        if not essay.strip():
            st.error("Please enter an essay to grade.")
            return

        with st.spinner("Analyzing your essay"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/grade",
                    json={
                        "essay": essay,
                        "selected_language": target_lang
                    }
                )
                
                if response.status_code == 400:
                    # Handle validation errors
                    error_data = response.json()
                    if error_data.get('error'):
                        display_validation_errors(error_data)
                        return
                
                response.raise_for_status()
                feedback = response.json()
                
                if feedback.get('error'):
                    display_validation_errors(feedback)
                else:
                    display_feedback(feedback)

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the server: {str(e)}")
            except json.JSONDecodeError:
                st.error("Invalid response from the server.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()