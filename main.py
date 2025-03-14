import streamlit as st
import requests
import json

# API endpoint
url = 'https://loan-default-back-590586875127.asia-southeast1.run.app/'

st.title("Loan Default Prediction")

# Custom Styling for Streamlit
st.markdown("""
    <style>
        .big-font {
            font-size: 24px !important;
            color: #4CAF50;
        }
        .input-box {
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 2px solid #4CAF50;
            width: 100%;
            margin-bottom: 20px;
        }
        .prediction-box {
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 18px;
        }
        .prediction-default {
            border: 2px solid red;
            color: red;
        }
        .prediction-fully-paid {
            border: 2px solid green;
            color: green;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Enter Loan Information</p>', unsafe_allow_html=True)

# Option to choose between Form Input, File Upload, or Text Input
input_option = st.radio("Choose how to enter your information", ("Fill out a Form", "Upload a File", "Paste Text"))

# Default Text Input for JSON (for form)
default_text = '''
{
    "loan_amnt": 2500.0,
    "term": 36,
    "int_rate": 15.27,
    "installment": 59.83,
    "emp_length": 1,
    "home_ownership": "RENT",
    "annual_inc": 30000.0,
    "verification_status": "Verified",
    "fico_range_low": 740.0,
    "fico_range_high": 744.0,
    "dti": 1.00,
    "revol_util": 9.4,
    "total_pymnt": 1014.53,
    "total_rec_prncp": 456.46,
    "total_rec_int": 435.17,
    "last_pymnt_amnt": 119.66,
    "inq_last_6mths": 5,
    "mths_since_last_delinq": 0,
    "purpose": "car"
}
'''

# Handling Form Input
if input_option == "Fill out a Form":
    st.subheader("Fill out the form below")
    loan_amnt = st.number_input('Loan Amount (in dollars)', value=2500.0, min_value=0.0, step=100.0)
    term = st.selectbox('Loan Term (in months)', [36, 60], index=0)
    int_rate = st.number_input('Interest Rate (%)', value=15.27, min_value=0.0, step=0.01)
    installment = st.number_input('Monthly Payment (in dollars)', value=59.83, min_value=0.0, step=0.01)
    emp_length = st.number_input('Years Employed', value=1, min_value=0)
    home_ownership = st.selectbox("Home Ownership Status", ['OWN', 'RENT', 'MORTGAGE', 'OTHER'], index=1)
    annual_inc = st.number_input('Annual Income (in dollars)', value=30000.0, min_value=0.0, step=1000.0)
    verification_status = st.selectbox("Verification Status", ['Verified', 'Source Verified', 'Not Verified'], index=1)
    fico_range_low = st.number_input('Lower Credit Score', value=740.0, min_value=300.0, max_value=850.0)
    fico_range_high = st.number_input('Upper Credit Score', value=744.0, min_value=300.0, max_value=850.0)
    dti = st.number_input('Debt-to-Income Ratio', value=1.00, min_value=0.0, step=0.01)
    revol_util = st.number_input('Credit Usage (%)', value=9.4, min_value=0.0, step=0.1)
    total_pymnt = st.number_input('Total Paid (in dollars)', value=1014.53, min_value=0.0, step=0.01)
    total_rec_prncp = st.number_input('Principal Paid (in dollars)', value=456.46, min_value=0.0, step=0.01)
    total_rec_int = st.number_input('Interest Paid (in dollars)', value=435.17, min_value=0.0, step=0.01)
    last_pymnt_amnt = st.number_input('Last Payment Made (in dollars)', value=119.66, min_value=0.0, step=0.01)
    inq_last_6mths = st.number_input('Recent Credit Inquiries (last 6 months)', value=5, min_value=0, step=1)
    mths_since_last_delinq = st.number_input('Months Since Last Payment Problem', value=0, min_value=0, step=1)
    purpose = st.selectbox('Purpose of the Loan', ['debt_consolidation', 'credit_card', 'home_improvement', 'major_purchase', 'small_business', 'car', 'wedding', 'medical', 'moving', 'vacation', 'house', 'renewable_energy', 'educational', 'other'])

    model_option = st.radio("Choose model", ("Logistic Regression", "Catboost"))
    # Prediction Button for Form Input
    if st.button('Predict'):
        payload = {
            'loan_amnt': loan_amnt,
            'term': term,
            'int_rate': int_rate,
            'installment': installment,
            'emp_length': emp_length,
            'home_ownership': home_ownership,
            'annual_inc': annual_inc,
            'verification_status': verification_status,
            'fico_range_low': fico_range_low,
            'fico_range_high': fico_range_high,
            'dti': dti,
            'revol_util': revol_util,
            'total_pymnt': total_pymnt,
            'total_rec_prncp': total_rec_prncp,
            'total_rec_int': total_rec_int,
            'last_pymnt_amnt': last_pymnt_amnt,
            'inq_last_6mths': inq_last_6mths,
            'mths_since_last_delinq': mths_since_last_delinq,
            'purpose': purpose
        }

        response = None
        if model_option == 'Logistic Regression':
            response = requests.post(url=url+"lg", json=payload)
        elif model_option == 'Catboost':
            response = requests.post(url=url+"catboost", json=payload)

        if response.status_code == 200:
            result = response.json()
            prediction = result.get('predicted_status')
            probability = result.get('probability', 'N/A')
            if prediction == 1:
                st.markdown(f'<div class="prediction-box prediction-default">Prediction: Default<br>Probability: {probability}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="prediction-box prediction-fully-paid">Prediction: Fully Paid<br>Probability: {probability}</div>', unsafe_allow_html=True)
        else:
            st.error(f"Error: {response.status_code}")
            st.error(f"Response Content: {response.text}")

# Handling File Upload Input
elif input_option == "Upload a File":
    st.subheader("Upload a JSON file")
    uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
    model_option = st.radio("Choose model", ("Logistic Regression", "Catboost"))
    if uploaded_file is not None:
        try:
            # Read the uploaded file and parse it as JSON
            file_content = uploaded_file.read().decode("utf-8")
            payload = json.loads(file_content)

            response = None
            if model_option == 'Logistic Regression':
                response = requests.post(url=url+"lg", json=payload)
            elif model_option == 'Catboost':
                response = requests.post(url=url+"catboost", json=payload)
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('predicted_status')
                probability = result.get('probability', 'N/A')
                if prediction == 1:
                    st.markdown(f'<div class="prediction-box prediction-default">Prediction: Default<br>Probability: {probability}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="prediction-box prediction-fully-paid">Prediction: Fully Paid<br>Probability: {probability}</div>', unsafe_allow_html=True)
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"Response Content: {response.text}")
        except json.JSONDecodeError:
            st.error("The uploaded file is not a valid JSON file. Please check the file structure.")
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")

# Handling Text Input
elif input_option == "Paste Text":
    st.subheader("Paste JSON Text")
    text_data = st.text_area("Paste your loan information here", value=default_text, height=300, max_chars=1500, key="text_input", help="Please paste the loan information in JSON format.")

    model_option = st.radio("Choose model", ("Logistic Regression", "Catboost"))
    # Prediction Button for Text Input
    if st.button('Predict'):
        if text_data:
            try:
                payload = json.loads(text_data)  # Convert string to JSON object
                
                # Send the request to the model for prediction
                response = None
                if model_option == 'Logistic Regression':
                    response = requests.post(url=url+"lg", json=payload)
                elif model_option == 'Catboost':
                    response = requests.post(url=url+"catboost", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get('predicted_status')
                    probability = result.get('probability', 'N/A')
                    if prediction == 1:
                        st.markdown(f'<div class="prediction-box prediction-default">Prediction: Default<br>Probability: {probability}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="prediction-box prediction-fully-paid">Prediction: Fully Paid<br>Probability: {probability}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"Response Content: {response.text}")
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please check the JSON structure and try again.")
            except Exception as e:
                st.error(f"Error processing the input: {e}")
        else:
            st.warning("Please enter some data to predict.")
