import streamlit as st
import pickle
import time
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler # type: ignore

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# Load data and model
data = load_model()
df = pd.read_csv('cleaned_data.csv')  # Dataset containing trek details and features

regressor = data["model"]
le_grade = data["le_grade"]
le_accomodation = data["le_accomodation"]
le_sex = data["le_sex"]
le_guide = data["le_guide"]
knn_model = data["knn_model"]
scaler = data["scaler"]


def show_predict_page():

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">Cost estimation and Trek Recommendation System</div>', unsafe_allow_html=True)
        
    st.write("##### Enter your trek preferences below to get recommendations.")
    
    # Minimalist Input Fields with Sections
    st.markdown('<div class="input-section">Trek Preferences</div>', unsafe_allow_html=True)
    
    grades = {
        "Moderate", 
        "Hard", 
        "Easy to Moderate", 
        "Easy"
    }

    accomodations = {
        'Hotel/Guesthouse',
        'Hotel/Teahouse', 
        'Hotel/Luxury Lodge',
        'Hotel/Lodge'
    }

    sex = {
        'Male',
        'Female',  
        'Transgender',
        'Non-Binary'
    }

    guide = {
        'Guide',
        'No Guide'
    }

    col1, spacer, col2 = st.columns([4, 2, 4])
    
    # Input fields
    with col1:
        age = st.slider("Age", 20, 40, 25 )
        time = st.slider("Duration of trek", 5, 30, 5 )
        group_size = st.slider("Number of people", 2, 15, 5 )
    
    with col2:
        guide = st.selectbox("Do you want a guide?", guide)
        sex = st.selectbox("Sex", sex)
        grade = st.selectbox("Choose difficulty level", grades)
        accomodation = st.selectbox("Choose type of accomodation", accomodations)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("Calculate cost and get Recommendations", key="recommend_button"):
        # Preprocess input
        X_user = np.array([[time, grade, accomodation, sex, age, group_size, guide]])
        X_user[:, 1] = le_grade.transform(X_user[:, 1].astype(str))          # 'Trip Grade'
        X_user[:, 2] = le_accomodation.transform(X_user[:, 2].astype(str))   # 'Accommodation'
        X_user[:, 3] = le_sex.transform(X_user[:, 3].astype(str))            # 'Sex'
        X_user[:, 6] = le_guide.transform(X_user[:, 6].astype(str))          # 'Guide'
        X_user = X_user.astype(float)

        # Predict cost
        predicted_cost = regressor.predict(X_user)
        st.subheader(f"The estimated cost is ${predicted_cost[0]:.2f}")

        # Include the predicted cost in user features
        X_user = np.append(X_user, predicted_cost)

        # Scale only the numerical features of the user input
        X_user_numerical = X_user[[0, 4, 5, 7]]  # 'Duration', 'Age', 'Group_Size', 'Cost'
        X_user_numerical_scaled = scaler.transform([X_user_numerical])

        # Reshape the categorical features into 2D
        X_user_categorical = X_user[[1, 2, 3, 6]].reshape(1, -1)  # 'Grade', 'Accommodation', 'Sex', 'Guide'

        # Now concatenate the numerical and categorical parts
        X_user_scaled = np.concatenate([X_user_numerical_scaled, X_user_categorical], axis=1)

        # Find the 5 most similar treks
        distances, indices = knn_model.kneighbors(X_user_scaled)

        st.markdown('<div class="section-title">Recommended Treks:</div>', unsafe_allow_html=True)
        for i in indices[0]:
            trek_name = df.iloc[i]['Trek']
            trek_cost = df.iloc[i]['Cost']
            satisfaction = df.iloc[i]['Review']

            st.markdown(
                f"""
                <div class="recommendation-card">
                    <h3>{trek_name}</h3>
                    <p><strong>Cost:</strong> ${trek_cost}</p>
                    <p><strong>Satisfaction:</strong> {satisfaction:.2f}/5</p>
                </div>
                """, 
                unsafe_allow_html=True
            )