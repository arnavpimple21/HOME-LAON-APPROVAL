import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from flask import Flask, request, render_template

# Initialize the Flask app
app = Flask(__name__)

# Load pre-trained model
model = pickle.load(open('best_model.pkl', 'rb'))

# Create label encoders (they should match the ones used during training)
label_encoder_income_type = LabelEncoder()
label_encoder_income_type.classes_ = np.array(['salary', 'self-employed', 'investment_income', 'rental_income', 'pension', 'alimony'])

label_encoder_education_type = LabelEncoder()
label_encoder_education_type.classes_ = np.array(['High School', 'Associate Degree', "Bachelor's Degree", "Master's Degree", 'Doctorate/PhD', 'Vocational/Technical Certification', 'Some College (No Degree)'])

label_encoder_family_status = LabelEncoder()
label_encoder_family_status.classes_ = np.array(['Single', 'Married', 'Divorced', 'Widowed', 'Separated', 'Living with Partner', 'Single Parent'])

label_encoder_gender = LabelEncoder()
label_encoder_gender.classes_ = np.array(['Male', 'Female', 'Other'])

label_encoder_housing_type = LabelEncoder()
label_encoder_housing_type.classes_ = np.array(['Owned', 'Rented', 'Mortgage', 'Living with Family/Friends', 'Social Housing'])

# Function to process input data and convert categories to numerical values
def process_input_data(form_data):
    # Encode categorical features
    form_data['NAME_INCOME_TYPE'] = label_encoder_income_type.transform([form_data['NAME_INCOME_TYPE']])[0]
    form_data['NAME_EDUCATION_TYPE'] = label_encoder_education_type.transform([form_data['NAME_EDUCATION_TYPE']])[0]
    form_data['NAME_FAMILY_STATUS'] = label_encoder_family_status.transform([form_data['NAME_FAMILY_STATUS']])[0]
    form_data['CODE_GENDER'] = label_encoder_gender.transform([form_data['CODE_GENDER']])[0]
    form_data['NAME_HOUSING_TYPE'] = label_encoder_housing_type.transform([form_data['NAME_HOUSING_TYPE']])[0]

    # Convert EXT_SOURCE_1 and APARTMENTS_AVG to numeric values
    form_data['EXT_SOURCE_1'] = 1 if form_data['EXT_SOURCE_1'] == 'Good' else 0
    form_data['APARTMENTS_AVG'] = 1 if form_data['APARTMENTS_AVG'] == 'Good' else 0

    # Convert days values to negative
    form_data['DAYS_BIRTH'] = -form_data['DAYS_BIRTH']
    form_data['DAYS_EMPLOYED'] = -form_data['DAYS_EMPLOYED']
    form_data['DAYS_REGISTRATION'] = -form_data['DAYS_REGISTRATION']

    return form_data

# Root route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input values from the form
        form_data = {
            'AMT_CREDIT': float(request.form['AMT_CREDIT']),
            'AMT_INCOME_TOTAL': float(request.form['AMT_INCOME_TOTAL']),
            'AMT_ANNUITY': float(request.form['AMT_ANNUITY']),
            'AMT_GOODS_PRICE': float(request.form['AMT_GOODS_PRICE']),
            'DAYS_BIRTH': int(request.form['DAYS_BIRTH']),
            'DAYS_EMPLOYED': int(request.form['DAYS_EMPLOYED']),
            'DAYS_REGISTRATION': float(request.form['DAYS_REGISTRATION']),
            'CNT_CHILDREN': int(request.form['CNT_CHILDREN']),
            'NAME_INCOME_TYPE': request.form['NAME_INCOME_TYPE'],
            'NAME_EDUCATION_TYPE': request.form['NAME_EDUCATION_TYPE'],
            'NAME_FAMILY_STATUS': request.form['NAME_FAMILY_STATUS'],
            'YEARS_BUILD_AVG': float(request.form['YEARS_BUILD_AVG']),
            'AMT_REQ_CREDIT_BUREAU_YEAR': float(request.form['AMT_REQ_CREDIT_BUREAU_YEAR']),
            'CODE_GENDER': request.form['CODE_GENDER'],
            'NAME_HOUSING_TYPE': request.form['NAME_HOUSING_TYPE'],
            'FLAG_OWN_REALTY': 1 if request.form['FLAG_OWN_REALTY'].lower() == 'yes' else 0,
            'FLAG_OWN_CAR': 1 if request.form['FLAG_OWN_CAR'].lower() == 'yes' else 0,
            'EXT_SOURCE_1': request.form['EXT_SOURCE_1'],
            'APARTMENTS_AVG': request.form['APARTMENTS_AVG'],
            'YEARS_BEGINEXPLUATATION_AVG': float(request.form['YEARS_BEGINEXPLUATATION_AVG']),
        }

        # Process the input data (encoding and conversion)
        processed_data = process_input_data(form_data)

        # Prepare input data for prediction
        input_data = np.array([[ 
            processed_data['AMT_CREDIT'],
            processed_data['AMT_INCOME_TOTAL'],
            processed_data['AMT_ANNUITY'],
            processed_data['AMT_GOODS_PRICE'],
            processed_data['DAYS_BIRTH'],
            processed_data['DAYS_EMPLOYED'],
            processed_data['DAYS_REGISTRATION'],
            processed_data['CNT_CHILDREN'],
            processed_data['NAME_INCOME_TYPE'],
            processed_data['NAME_EDUCATION_TYPE'],
            processed_data['NAME_FAMILY_STATUS'],
            processed_data['YEARS_BUILD_AVG'],
            processed_data['AMT_REQ_CREDIT_BUREAU_YEAR'],
            processed_data['CODE_GENDER'],
            processed_data['NAME_HOUSING_TYPE'],
            processed_data['FLAG_OWN_REALTY'],
            processed_data['FLAG_OWN_CAR'],
            processed_data['EXT_SOURCE_1'],
            processed_data['APARTMENTS_AVG'],
            processed_data['YEARS_BEGINEXPLUATATION_AVG']
        ]])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = "The client presents a higher risk profile for loan approval" if prediction == 1 else "This client demonstrates the ability to comfortably repay the loan"
        return render_template('index.html', prediction=result)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
