# app.py - Main Streamlit Application

import streamlit as st
import pandas as pd
from typing import Dict, List
import time

# Import our modules
from config.settings import *
from ai_engine.orchestrator import AIOrchestrator
from utils.excel_exporter import ExcelExporter
from utils.validators import InputValidator

# Page configuration
st.set_page_config(
    page_title="AI Scholarship Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .scholarship-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .scholarship-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .scholarship-detail {
        margin: 0.3rem 0;
        font-size: 0.95rem;
    }
    .match-score {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)


class ScholarshipFinderApp:
    """Main application class"""
    
    def __init__(self):
        self.orchestrator = AIOrchestrator()
        self.validator = InputValidator()
        
        # Initialize session state
        if 'scholarships' not in st.session_state:
            st.session_state.scholarships = []
        if 'search_performed' not in st.session_state:
            st.session_state.search_performed = False
    
    def run(self):
        """Run the application"""
        self.render_header()
        self.render_sidebar()
        self.render_main_content()
    
    def render_header(self):
        """Render application header"""
        st.markdown('<h1 class="main-header">🎓 AI-Powered Scholarship Finder</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">Discover international scholarship opportunities tailored to your profile</p>',
            unsafe_allow_html=True
        )
    
    def render_sidebar(self):
        """Render sidebar with user inputs"""
        st.sidebar.header("📋 Your Profile")
        
        # Degree Level
        degree_level = st.sidebar.selectbox(
            "Degree Level *",
            options=DEGREE_LEVELS,
            help="Select your desired degree level"
        )
        
        # Field of Study
        field_of_study = st.sidebar.selectbox(
            "Field of Study *",
            options=FIELDS_OF_STUDY,
            help="Select your field of interest"
        )
        
        # Nationality
        nationality = st.sidebar.selectbox(
            "Nationality *",
            options=NATIONALITIES,
            help="Select your nationality"
        )
        
        # CGPA
        cgpa = st.sidebar.slider(
            "CGPA / GPA",
            min_value=0.0,
            max_value=4.0,
            value=3.0,
            step=0.1,
            help="Your current CGPA on a 4.0 scale"
        )
        
        # Desired Country
        country = st.sidebar.selectbox(
            "Desired Country *",
            options=COUNTRIES,
            help="Select your preferred destination country"
        )
        
        st.sidebar.markdown("---")
        
        # Search button
        if st.sidebar.button("🔍 Search Scholarships", use_container_width=True):
            self.perform_search({
                'degree_level': degree_level,
                'field_of_study': field_of_study,
                'nationality': nationality,
                'cgpa': cgpa,
                'country': country
            })
        
        # Info section
        st.sidebar.markdown("---")
        st.sidebar.info(
            "**How it works:**\n"
            "1. Fill in your profile\n"
            "2. Click 'Search Scholarships'\n"
            "3. AI scrapes real-time data from official sources\n"
            "4. View matched opportunities\n"
            "5. Export to Excel"
        )
    
    def perform_search(self, profile: Dict):
        """Execute scholarship search"""
        # Validate profile
        is_valid, errors = self.validator.validate_profile(profile)
        
        if not is_valid:
            st.error("❌ " + "\n".join(errors))
            return
        
        # Create progress container
        progress_container = st.empty()
        status_container = st.empty()
        
        with progress_container.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        def progress_callback(message: str, progress: float):
            """Update progress UI"""
            status_text.text(message)
            progress_bar.progress(progress)
        
        try:
            # Execute search
            status_container.info("🔍 Searching scholarships...")
            scholarships = self.orchestrator.search_scholarships(profile, progress_callback)
            
            # Store in session state
            st.session_state.scholarships = scholarships
            st.session_state.search_performed = True
            
            # Clear progress
            progress_container.empty()
            
            if scholarships:
                status_container.success(f"✅ Found {len(scholarships)} matching scholarships!")
                time.sleep(1)
                status_container.empty()
            else:
                status_container.warning("⚠️ No scholarships found matching your criteria. Try adjusting your filters.")
        
        except Exception as e:
            progress_container.empty()
            status_container.error(f"❌ An error occurred: {str(e)}")
    
    def render_main_content(self):
        """Render main content area"""
        if not st.session_state.search_performed:
            self.render_welcome_screen()
        else:
            self.render_results()
    
    def render_welcome_screen(self):
        """Render welcome screen when no search has been performed"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("## 🌟 Welcome!")
            st.markdown("""
            This AI-powered tool helps you discover international scholarship opportunities by:
            
            - 🌐 **Real-time scraping** from official sources (DAAD, HEC, and more)
            - 🎯 **Smart matching** based on your profile
            - 📊 **Comprehensive details** including deadlines, funding, and requirements
            - 📥 **Excel export** for easy management
            
            ### Get Started:
            1. Complete your profile in the sidebar
            2. Click "Search Scholarships"
            3. Explore your matched opportunities
            """)
            
            st.markdown("---")
            
            # Feature highlights
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("### 🚀 Fast")
                st.markdown("Real-time data from multiple sources in seconds")
            
            with col_b:
                st.markdown("### 🎯 Accurate")
                st.markdown("AI-powered matching to your exact profile")
            
            with col_c:
                st.markdown("### 🔒 Reliable")
                st.markdown("Official sources with verified information")
    
    def render_results(self):
        """Render search results"""
        scholarships = st.session_state.scholarships
        
        if not scholarships:
            st.warning("No scholarships found. Try adjusting your search criteria.")
            return
        
        # Results header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"## 📚 Found {len(scholarships)} Scholarships")
        
        with col2:
            if st.button("📥 Export to Excel", use_container_width=True):
                self.export_to_excel(scholarships)
        
        st.markdown("---")
        
        # Display scholarships
        for idx, sch in enumerate(scholarships, 1):
            self.render_scholarship_card(sch, idx)
    
    def render_scholarship_card(self, scholarship: Dict, index: int):
        """Render individual scholarship card"""
        match_score = scholarship.get('match_score', 0)
        
        # Color gradient based on match score
        if match_score >= 80:
            gradient = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
        elif match_score >= 60:
            gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        else:
            gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        
        st.markdown(f"""
        <div class="scholarship-card" style="background: {gradient};">
            <div class="scholarship-title">
                {index}. {scholarship.get('title', 'Untitled Scholarship')}
                <span class="match-score">Match: {match_score:.0f}%</span>
            </div>
            <div class="scholarship-detail">🌍 <strong>Country:</strong> {scholarship.get('country', 'N/A')}</div>
            <div class="scholarship-detail">🎓 <strong>Degree:</strong> {scholarship.get('degree', 'N/A')}</div>
            <div class="scholarship-detail">📚 <strong>Field:</strong> {scholarship.get('field', 'N/A')}</div>
            <div class="scholarship-detail">⏱️ <strong>Duration:</strong> {scholarship.get('duration', 'N/A')}</div>
            <div class="scholarship-detail">💰 <strong>Funding:</strong> {scholarship.get('funding', 'N/A')}</div>
            <div class="scholarship-detail">✅ <strong>Eligibility:</strong> {scholarship.get('eligibility', 'N/A')}</div>
            <div class="scholarship-detail">📄 <strong>Documents:</strong> {scholarship.get('documents', 'N/A')}</div>
            <div class="scholarship-detail">📅 <strong>Deadline:</strong> {scholarship.get('deadline', 'N/A')}</div>
            <div class="scholarship-detail">🔗 <strong>Link:</strong> <a href="{scholarship.get('url', '#')}" target="_blank" style="color: white; text-decoration: underline;">{scholarship.get('url', 'N/A')}</a></div>
        </div>
        """, unsafe_allow_html=True)
    
    def export_to_excel(self, scholarships: List[Dict]):
        """Export scholarships to Excel"""
        try:
            exporter = ExcelExporter()
            filename = exporter.export_scholarships(scholarships)
            
            # Read file for download
            with open(filename, 'rb') as f:
                excel_data = f.read()
            
            st.download_button(
                label="⬇️ Download Excel File",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success(f"✅ Excel file generated: {filename}")
        
        except Exception as e:
            st.error(f"❌ Error generating Excel: {str(e)}")


def main():
    """Main entry point"""
    app = ScholarshipFinderApp()
    app.run()


if __name__ == "__main__":
    main()