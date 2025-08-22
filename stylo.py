import streamlit as st

def set_custom_styles():
    # CSS personalizado
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f0f4f8;
        color: #2d3748;
    }
    .hero-header {
        background: linear-gradient(135deg, #4c51bf 0%, #6b46c1 100%);
        color: #ffffff;
        padding: 40px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .hero-header p {
        font-size: 1.25rem;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .hero-header .source-info {
        font-size: 0.875rem;
        opacity: 0.7;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 120px;
        margin-bottom: 16px;
    }
    .metric-card .icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }
    .metric-card .title {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2c5282;
        line-height: 1.2;
    }
    .metric-card .value.green {
        color: #2f855a;
    }
    .metric-card .value.red {
        color: #e53e3e;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 20px;
    }
    .analysis-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 20px;
    }
    .general-analysis {
        background-color: #ffffff;
        border-left: 4px solid #718096;
        color: #2d3748;
        padding: 16px;
        border-radius: 0.375rem;
    }
    .general-analysis ul {
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .general-analysis li {
        margin-bottom: 8px;
    }
    .dynamic-analysis {
        background-color: #ebf8ff;
        border-left: 4px solid #3182ce;
        color: #2c5282;
        padding: 16px;
        border-radius: 0.375rem;
        white-space: pre-wrap;
    }
    .explanation-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 20px;
    }
    .key-info {
        background-color: #ebf8ff;
        border-left: 4px solid #3182ce;
        color: #2c5282;
        padding: 16px;
        border-radius: 0.375rem;
        margin-top: 16px;
    }
    .weekly-insight {
        background-color: #f0fff4;
        border-left: 4px solid #38a169;
        color: #2f855a;
        padding: 16px;
        border-radius: 0.375rem;
        margin-top: 16px;
    }
    .weekly-insight h4 {
        margin-top: 0;
        color: #2f855a;
    }
    .weekly-insight ul {
        margin-bottom: 0;
    }
    .footer {
        text-align: center;
        color: #718096;
        font-size: 0.875rem;
        margin-top: 40px;
    }
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 600;
        background-color: #e2e8f0;
        color: #4a5568;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #4c51bf;
        color: white;
    }
    .dataframe-container {
        margin-top: 20px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }
    .url-params-info {
        background-color: #f0fff4;
        border-left: 4px solid #38a169;
        color: #2f855a;
        padding: 16px;
        border-radius: 0.375rem;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)