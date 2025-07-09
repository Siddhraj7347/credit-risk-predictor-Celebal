import streamlit as st
import requests
import json
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Creditworthiness Predictor",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Custom CSS for enhanced styling (mimicking some Tailwind effects) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #f3f4f6; /* text-gray-100 */
        background-color: #111827; /* bg-gray-900 */
    }

    .stApp {
        background: #111827;
    }

    .main .block-container {
        padding: 2rem;
        background-color: #1f2937; /* slate-800 */
        border-radius: 1.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        border: 1px solid #374151;
    }

    h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        color: #f9fafb;
        margin-bottom: 1rem;
    }

    p {
        text-align: center;
        color: #d1d5db;
        margin-bottom: 2rem;
        font-size: 1.125rem;
    }

    .stSlider > div > div > div:nth-child(2) {
        background-color: #4b5563;
    }

    .stSlider > div > div > div:nth-child(2) > div {
        background-color: #8b5cf6;
    }

    .stSelectbox > div > div {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
    }

    .stButton > button {
    /* Background and Color */
    background: linear-gradient(to right, #7c3aed, #4f46e5); /* Gradient from purple-600 to indigo-600 */
    color: white; /* White text color */

    /* Typography */
    font-weight: 700; /* Bold font weight */
    font-size: 1.125rem; /* 18px */

    /* Spacing and Layout */
    padding: 0.75rem 1.5rem; /* 12px vertical, 24px horizontal padding */
    margin: 0.5rem auto; /* Centered */
    display: flex; /* Use flex to center text horizontally/vertically */
    align-items: center;
    justify-content: center;
    text-align: center;

    /* Border and Shape */
    border: none;
    border-radius: 0.75rem;

    /* Shadow and Transition */
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.7);
    transition: all 0.3s ease-in-out;

    /* Ensure transparent background inside */
    background-color: transparent;
}

/* Fix inner span or div that may have black background */
.stButton > button * {
    background-color: transparent !important;
}

/* Hover effect */
.stButton > button:hover {
    background: linear-gradient(to right, #6d28d9, #4338ca);
    transform: scale(1.05);
}

    .prediction-result {
        margin-top: 2rem;
        padding: 1.75rem;
        border-radius: 1rem;
        text-align: center;
        font-weight: 800;
        font-size: 1.875rem;
        animation: fadeIn 0.5s ease-out;
    }

    .good-risk {
        background-color: #064e3b;
        color: #a7f3d0;
        border: 1px solid #10b981;
    }

    .bad-risk {
        background-color: #7f1d1d;
        color: #fecaca;
        border: 1px solid #f87171;
    }

    .error-message {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #7f1d1d;
        color: #fecaca;
        border: 1px solid #f87171;
        font-size: 1.125rem;
        font-weight: 500;
        text-align: center;
    }

    .loading-message {
        text-align: center;
        margin-top: 2rem;
        color: #c084fc;
        font-size: 1.25rem;
        font-weight: 600;
        animation: pulse 1.5s infinite;
    }

    footer {
        color: #9ca3af !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title and Description ---
st.markdown("<h1>🏦 Creditworthiness Predictor</h1>", unsafe_allow_html=True)
st.markdown("""
    <p>This application simulates whether a person is a <span style="font-weight: 800; color: #166534;">Good</span> or <span style="font-weight: 800; color: #991b1b;">Bad</span> credit risk based on a set of common financial criteria.</p>
""", unsafe_allow_html=True)

# --- Input Form ---
st.subheader("Enter Customer Details")

# Using columns for a 2-column layout
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 75, 30, help="Customer's age")
    duration = st.slider("Credit Duration (months)", 4, 72, 24, help="How long the credit will last")
    amount = st.slider("Credit Amount", 250, 20000, 1500, step=50, help="The total amount of credit requested")

with col2:
    purpose_options = ["radio/tv", "education", "furniture/equipment", "new car", "used car", "business", "repairs", "domestic appliance", "other"]
    purpose = st.selectbox("Purpose", purpose_options, index=purpose_options.index("radio/tv"), help="The reason for the credit")

    housing_options = ["own", "for free", "rent"]
    housing = st.selectbox("Housing", housing_options, index=housing_options.index("own"), help="Customer's housing situation")

    job_options = ["skilled", "unskilled resident", "highly skilled", "unemployed/non-resident"]
    job = st.selectbox("Job", job_options, index=job_options.index("skilled"), help="Customer's job category")

# --- Prediction Logic ---
def get_prediction(age, duration, amount, purpose, housing, job):
    # Construct the prompt for the Gemini API
    prompt = f"""Based on the following customer details, determine if they are likely a "Good Credit Risk" or "Bad Credit Risk". Provide a clear answer: "Good Credit Risk" or "Bad Credit Risk".
    Age: {age}
    Credit Duration: {duration} months
    Credit Amount: {amount}
    Purpose: {purpose}
    Housing: {housing}
    Job: {job}

    Consider general factors like higher age, lower duration, and lower amount being generally better, and purposes like education/business being potentially better than luxury items.
    """

    # Gemini API details
    api_key = "AIzaSyDaNmkRNAW72972phhJHaKcZJn438jVtow" # API key will be provided by the environment
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result.get('candidates') and len(result['candidates']) > 0 and \
           result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts') and \
           len(result['candidates'][0]['content']['parts']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Failed to get a prediction. Unexpected API response structure."
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch prediction: {e}. Please check your internet connection or API key."
    except json.JSONDecodeError:
        return "Failed to parse API response. Invalid JSON."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Predict Button ---
if st.button("Predict Creditworthiness"):
    with st.spinner("Analyzing data, please wait..."): # Loading indicator
        prediction_text = get_prediction(age, duration, amount, purpose, housing, job)

    # Display Prediction Result
    if "Good Credit Risk" in prediction_text:
        st.markdown(f"""
            <div class="prediction-result good-risk">
                <h2>Prediction Result:</h2>
                <p>✅ {prediction_text}</p>
                <p class="sub-text">This prediction is based on the provided inputs and general credit assessment principles.</p>
            </div>
        """, unsafe_allow_html=True)
    elif "Bad Credit Risk" in prediction_text:
        st.markdown(f"""
            <div class="prediction-result bad-risk">
                <h2>Prediction Result:</h2>
                <p>❌ {prediction_text}</p>
                <p class="sub-text">This prediction is based on the provided inputs and general credit assessment principles.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Handle API errors or unexpected responses
        st.markdown(f"""
            <div class="error-message">
                <p>Error: {prediction_text}</p>
                <p class="sub-text">Please check your internet connection or try again later.</p>
            </div>
        """, unsafe_allow_html=True)

# --- Footer ---
year = datetime.now().year
st.markdown(f"&copy; {year} Creditworthiness Predictor. All rights reserved.", unsafe_allow_html=True)

