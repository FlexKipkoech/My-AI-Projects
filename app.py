import streamlit as st
import requests
import json
from datetime import datetime
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Fix Kenya Document Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Fix Kenya branding
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E91E63;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #E91E63;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #C2185B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generation_status' not in st.session_state:
    st.session_state.generation_status = None
if 'last_request' not in st.session_state:
    st.session_state.last_request = None

# Header
st.markdown('<h1 class="main-header">Fix Kenya Document Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate professional market research and strategy documents in minutes</p>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. **Select document type** - Choose what you want to generate
    2. **Fill in client details** - All fields marked with * are required
    3. **Review information** - Ensure accuracy
    4. **Generate documents** - Click the button and wait
    5. **Check your email** - Documents will be sent to the specified email
    """)
    
    st.markdown("---")
    
    st.markdown("## ⏱️ Estimated Time")
    st.markdown("""
    - **Market Research Only**: ~5 minutes
    - **Strategy Only**: ~5 minutes
    - **Both Documents**: ~10 minutes
    """)
    
    st.markdown("---")
    
    st.markdown("## 🆘 Need Help?")
    st.markdown("Contact: support@fix.co.ke")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Document Request Form")
    
    # Document type selection
    doc_type = st.selectbox(
        "Select Document Type*",
        ["Market Research Only", "Strategy Document Only", "Both Documents"],
        help="Choose which document(s) you want to generate"
    )
    
    # Map friendly names to API values
    doc_type_map = {
        "Market Research Only": "market_research",
        "Strategy Document Only": "strategy",
        "Both Documents": "both"
    }
    
    # Client Information
    st.markdown("#### Client Information")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        client_name = st.text_input("Client Name*", placeholder="e.g., Safari Tech Solutions")
        industry = st.text_input("Industry*", placeholder="e.g., Technology, Retail, Healthcare")
        target_market = st.text_input("Target Market*", placeholder="e.g., SMEs in Nairobi")
    
    with col_b:
        contact_email = st.text_input("Contact Email*", placeholder="client@example.com")
        budget = st.text_input("Budget*", placeholder="e.g., KES 500,000")
        timeline = st.text_input("Timeline*", placeholder="e.g., 6 months")
    
    business_description = st.text_area(
        "Business Description*",
        placeholder="Brief description of the client's business, products/services, and unique value proposition",
        height=100
    )
    
    # Digital Presence (for strategy documents)
    if doc_type in ["Strategy Document Only", "Both Documents"]:
        current_digital_presence = st.text_area(
            "Current Digital Presence*",
            placeholder="Describe current website, social media, digital marketing efforts",
            height=80
        )
    else:
        current_digital_presence = "Not applicable for market research only"
    
    # Competitors
    st.markdown("#### Competition & Objectives")
    
    competitors_input = st.text_area(
        "Known Competitors (one per line)",
        placeholder="Competitor 1\nCompetitor 2\nCompetitor 3",
        height=80
    )
    
    objectives_input = st.text_area(
        "Business Objectives (one per line)*",
        placeholder="Increase brand awareness by 50%\nGenerate 100 qualified leads monthly\nImprove customer engagement",
        height=100
    )
    
    # Additional Information
    st.markdown("#### Additional Information")
    
    col_c, col_d = st.columns(2)
    
    with col_c:
        requested_by = st.text_input("Requested By*", placeholder="Your name")
        priority = st.selectbox("Priority", ["normal", "high", "urgent"])
    
    with col_d:
        internal_notes = st.text_area(
            "Internal Notes",
            placeholder="Any special requirements or notes for the team",
            height=80
        )

with col2:
    st.markdown("### 📊 Request Summary")
    
    # Display summary in an info box
    if client_name and industry and target_market:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**Client:** {client_name}")
        st.markdown(f"**Industry:** {industry}")
        st.markdown(f"**Document Type:** {doc_type}")
        st.markdown(f"**Timeline:** {timeline if timeline else 'Not specified'}")
        st.markdown(f"**Priority:** {priority.capitalize()}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Generation status
    if st.session_state.generation_status:
        if st.session_state.generation_status['success']:
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.markdown("✅ **Success!**")
            st.markdown(st.session_state.generation_status['message'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">', unsafe_allow_html=True)
            st.markdown("❌ **Error**")
            st.markdown(st.session_state.generation_status['message'])
            st.markdown('</div>', unsafe_allow_html=True)

# Generate button
st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    if st.button("🚀 Generate Documents", type="primary", use_container_width=True):
        # Validate required fields
        if not all([client_name, industry, target_market, contact_email, budget, timeline, 
                   business_description, requested_by, objectives_input]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Parse competitors and objectives
            competitors = [c.strip() for c in competitors_input.split('\n') if c.strip()]
            objectives = [o.strip() for o in objectives_input.split('\n') if o.strip()]
            
            # Prepare request data
            request_data = {
                "requestType": doc_type_map[doc_type],
                "clientData": {
                    "clientName": client_name,
                    "industry": industry,
                    "businessDescription": business_description,
                    "targetMarket": target_market,
                    "currentDigitalPresence": current_digital_presence,
                    "knownCompetitors": competitors,
                    "objectives": objectives,
                    "budget": budget,
                    "timeline": timeline,
                    "contactEmail": contact_email
                },
                "metadata": {
                    "requestedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "requestedBy": requested_by,
                    "priority": priority,
                    "internalNotes": internal_notes
                },
                "options": {
                    "generateMarketResearch": doc_type in ["Market Research Only", "Both Documents"],
                    "generateStrategy": doc_type in ["Strategy Document Only", "Both Documents"],
                    "combineDocuments": doc_type == "Both Documents",
                    "sendSeparateEmails": False
                }
            }
            
            # Store request in session state
            st.session_state.last_request = request_data
            
            # Show spinner while sending request
            with st.spinner(f"Generating {doc_type.lower()}... This may take a few minutes."):
                try:
                    # Get webhook URL from environment
                    webhook_url = os.getenv('WEBHOOK_URL_ROUTER')
                    
                    if not webhook_url:
                        st.error("Webhook URL not configured. Please contact support.")
                    else:
                        # Send request to Make.com
                        response = requests.post(
                            webhook_url,
                            json=request_data,
                            headers={'Content-Type': 'application/json'},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            st.session_state.generation_status = {
                                'success': True,
                                'message': f"Documents are being generated and will be sent to {contact_email}. Please check your email in 5-10 minutes."
                            }
                            st.rerun()
                        else:
                            st.session_state.generation_status = {
                                'success': False,
                                'message': f"Request failed with status code: {response.status_code}"
                            }
                            st.rerun()
                            
                except requests.exceptions.Timeout:
                    st.session_state.generation_status = {
                        'success': False,
                        'message': "Request timed out. Please try again."
                    }
                    st.rerun()
                except Exception as e:
                    st.session_state.generation_status = {
                        'success': False,
                        'message': f"An error occurred: {str(e)}"
                    }
                    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">Powered by Fix Kenya Limited | AI Document Generation System</p>',
    unsafe_allow_html=True
)