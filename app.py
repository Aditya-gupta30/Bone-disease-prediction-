# # import streamlit as st
# # import numpy as np
# # import joblib
# # import pandas as pd

# # # Load models
# # model = joblib.load("models/logistic_model.pkl")
# # scaler = joblib.load("models/scaler.pkl")
# # kmeans = joblib.load("models/kmeans_model.pkl")
# # feature_names = joblib.load("models/feature_names.pkl")

# # # ── UI ──────────────────────────────────────────────────────────────────────
# # st.title("Osteoporosis Prediction System")
# # st.markdown("Fill in the details below and click **Predict** to assess risk.")

# # col1, col2 = st.columns(2)

# # with col1:
# #     age             = st.number_input("Age", min_value=1, max_value=120)
# #     gender          = st.selectbox("Gender", ["Female", "Male"])
# #     hormonal        = st.selectbox("Hormonal Changes", ["Normal", "Postmenopausal"])
# #     family_history  = st.selectbox("Family History of Osteoporosis", ["No", "Yes"])
# #     body_weight     = st.selectbox("Body Weight", ["Normal", "Underweight", "Overweight"])

# # with col2:
# #     calcium         = st.selectbox("Calcium Intake", ["Adequate", "Low"])
# #     vitamin_d       = st.selectbox("Vitamin D Intake", ["Sufficient", "Insufficient"])
# #     physical        = st.selectbox("Physical Activity", ["Active", "Sedentary"])
# #     smoking         = st.selectbox("Smoking", ["No", "Yes"])
# #     prior_fracture  = st.selectbox("Prior Fractures", ["No", "Yes"])

# # # ── Prediction ───────────────────────────────────────────────────────────────
# # if st.button("🔍 Predict"):

# #     # Build a dict with all raw values
# #     raw = {
# #         "Age":                age,
# #         "Gender":             gender,
# #         "Hormonal Changes":   hormonal,
# #         "Family History":     family_history,
# #         "Body Weight":        body_weight,
# #         "Calcium Intake":     calcium,
# #         "Vitamin D Intake":   vitamin_d,
# #         "Physical Activity":  physical,
# #         "Smoking":            smoking,
# #         "Prior Fractures":    prior_fracture,
# #     }

# #     input_df = pd.DataFrame([raw])

# #     # One-hot encode exactly like training did
# #     input_encoded = pd.get_dummies(input_df)

# #     # ── KEY FIX: align columns to what the scaler was trained on ─────────────
# #     input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)

# #     # Scale and predict
# #     input_scaled = scaler.transform(input_encoded)
# #     prediction   = model.predict(input_scaled)
# #     cluster      = kmeans.predict(input_scaled)
# #     proba        = model.predict_proba(input_scaled)[0]

# #     # ── Results ──────────────────────────────────────────────────────────────
# #     st.divider()
# #     st.subheader("📊 Results")

# #     risk_pct = round(proba[1] * 100, 1)

# #     if prediction[0] == 1:
# #         st.error(f"⚠️ **High Risk of Osteoporosis** — Confidence: {risk_pct}%")
# #         st.markdown("""
# #         **Recommended actions:**
# #         - Consult a doctor or bone specialist (rheumatologist / endocrinologist)
# #         - Get a DEXA bone density scan
# #         - Increase calcium and vitamin D intake
# #         - Begin weight-bearing exercise if physically able
# #         """)
# #     else:
# #         st.success(f"✅ **Low Risk of Osteoporosis** — Confidence: {round(proba[0]*100, 1)}%")
# #         st.markdown("""
# #         **Keep it up:**
# #         - Maintain a calcium-rich diet
# #         - Stay physically active
# #         - Schedule regular check-ups after age 50
# #         """)

# #     st.info(f"🔵 Cluster Group: **{cluster[0]}** &nbsp;|&nbsp; Risk Score: **{risk_pct}%**")

# #     # Debug expander — remove in production
# #     with st.expander("🛠 Debug: Encoded Input"):
# #         st.dataframe(pd.DataFrame([input_encoded.iloc[0]], columns=feature_names))
# import streamlit as st
# import numpy as np
# import joblib
# import pandas as pd

# # ── PAGE CONFIG ─────────────────────────────────────────
# st.set_page_config(
#     page_title="Osteoporosis Predictor",
#     page_icon="🦴",
#     layout="wide"
# )

# # ── LOAD MODELS ─────────────────────────────────────────
# model = joblib.load("models/logistic_model.pkl")
# scaler = joblib.load("models/scaler.pkl")
# kmeans = joblib.load("models/kmeans_model.pkl")
# feature_names = joblib.load("models/feature_names.pkl")

# # ── CUSTOM CSS (IMPORTANT FOR UI) ───────────────────────
# st.markdown("""
#     <style>
#         .main {
#             background-color: #f5f7fa;
#         }
#         .stButton>button {
#             background-color: #4CAF50;
#             color: white;
#             font-size: 18px;
#             border-radius: 10px;
#             padding: 10px;
#         }
#         .stButton>button:hover {
#             background-color: #45a049;
#         }
#         .card {
#             padding: 20px;
#             border-radius: 12px;
#             background-color: white;
#             box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ── TITLE ───────────────────────────────────────────────
# st.title("🦴 Osteoporosis Prediction System")
# st.markdown("### Smart AI-based Risk Assessment")

# # ── SIDEBAR INPUTS ──────────────────────────────────────
# st.sidebar.header("🧾 Patient Details")

# age = st.sidebar.slider("Age", 1, 120, 25)
# gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
# hormonal = st.sidebar.selectbox("Hormonal Changes", ["Normal", "Postmenopausal"])
# family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])
# body_weight = st.sidebar.selectbox("Body Weight", ["Normal", "Underweight", "Overweight"])

# calcium = st.sidebar.selectbox("Calcium Intake", ["Adequate", "Low"])
# vitamin_d = st.sidebar.selectbox("Vitamin D Intake", ["Sufficient", "Insufficient"])
# physical = st.sidebar.selectbox("Physical Activity", ["Active", "Sedentary"])
# smoking = st.sidebar.selectbox("Smoking", ["No", "Yes"])
# prior_fracture = st.sidebar.selectbox("Prior Fractures", ["No", "Yes"])

# # ── MAIN CONTENT LAYOUT ─────────────────────────────────
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown(f"<div class='card'><b>Age:</b> {age}</div>", unsafe_allow_html=True)

# with col2:
#     st.markdown(f"<div class='card'><b>Gender:</b> {gender}</div>", unsafe_allow_html=True)

# with col3:
#     st.markdown(f"<div class='card'><b>Activity:</b> {physical}</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ── PREDICT BUTTON ──────────────────────────────────────
# if st.button("🔍 Predict Risk"):

#     raw = {
#         "Age": age,
#         "Gender": gender,
#         "Hormonal Changes": hormonal,
#         "Family History": family_history,
#         "Body Weight": body_weight,
#         "Calcium Intake": calcium,
#         "Vitamin D Intake": vitamin_d,
#         "Physical Activity": physical,
#         "Smoking": smoking,
#         "Prior Fractures": prior_fracture,
#     }

#     input_df = pd.DataFrame([raw])

#     # Encoding
#     input_encoded = pd.get_dummies(input_df)
#     input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)

#     # Scaling
#     input_scaled = scaler.transform(input_encoded)

#     # Prediction
#     prediction = model.predict(input_scaled)[0]
#     cluster = kmeans.predict(input_scaled)[0]
#     proba = model.predict_proba(input_scaled)[0]

#     risk_pct = round(proba[1] * 100, 1)

#     st.markdown("## 📊 Prediction Results")

#     # ── METRICS DISPLAY ───────────────────────────────
#     col1, col2, col3 = st.columns(3)

#     col1.metric("Risk Score", f"{risk_pct}%")
#     col2.metric("Cluster Group", cluster)
#     col3.metric("Prediction", "High Risk" if prediction == 1 else "Low Risk")

#     st.markdown("---")

#     # ── PROGRESS BAR ───────────────────────────────
#     st.progress(int(risk_pct))

#     # ── RESULT BOX ───────────────────────────────
#     if prediction == 1:
#         st.error(f"⚠️ High Risk of Osteoporosis ({risk_pct}%)")

#         st.markdown("""
#         ### 🩺 Recommended Actions:
#         - Consult a specialist
#         - Take calcium & vitamin D
#         - Do weight-bearing exercises
#         - Get bone density test
#         """)

#     else:
#         st.success(f"✅ Low Risk of Osteoporosis ({round(proba[0]*100,1)}%)")

#         st.markdown("""
#         ### 💪 Maintain Healthy Lifestyle:
#         - Balanced diet
#         - Regular exercise
#         - Routine checkups
#         """)

#     # ── VISUAL INDICATOR ─────────────────────────────
#     if risk_pct > 70:
#         st.warning("🔴 Very High Risk")
#     elif risk_pct > 40:
#         st.info("🟡 Moderate Risk")
#     else:
#         st.success("🟢 Low Risk")

#     # ── DEBUG SECTION ───────────────────────────────
#     with st.expander("🛠 Debug Data"):
#         st.dataframe(input_encoded)