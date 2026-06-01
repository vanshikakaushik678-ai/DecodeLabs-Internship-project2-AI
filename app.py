import streamlit as st
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# Page Configuration
st.set_page_config(
    page_title="Advanced AI Classification Dashboard",
    layout="wide"
)

st.title("🧠 Advanced AI Classification Dashboard")

st.markdown("""
### Objective
Upload a CSV dataset, select a target column, train multiple classification models, and compare their performance.
""")

# File Upload
uploaded_file = st.file_uploader(
    "📂 Upload CSV Dataset",
    type=["csv"]
)

# Main App
if uploaded_file is not None:

    try:
        # Read Dataset
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Dataset Preview")
        st.dataframe(df.head())

        st.subheader("📈 Dataset Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        st.subheader("Statistics")
        st.write(df.describe(include="all"))

        # Target Column Selection
        target = st.selectbox(
            "🎯 Select Target Column",
            df.columns
        )

        X = df.drop(columns=[target])
        y = df[target]

        # Encode categorical features
        for col in X.columns:
            if X[col].dtype == "object":
                encoder = LabelEncoder()
                X[col] = encoder.fit_transform(X[col].astype(str))

        # Encode target column
        if y.dtype == "object":
            y = LabelEncoder().fit_transform(y.astype(str))

        # Train-Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        st.subheader("🔀 Train/Test Split")
        st.write(f"Training Samples: {len(X_train)}")
        st.write(f"Testing Samples: {len(X_test)}")

        # Models
        models = {
            "Random Forest": RandomForestClassifier(
                n_estimators=300,
                random_state=42
            ),
            "Decision Tree": DecisionTreeClassifier(),
            "SVM": SVC()
        }

        scores = []
        best_accuracy = 0
        best_model_name = ""
        best_model = None
        best_prediction = None

        # Train Models
        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            accuracy = accuracy_score(
                y_test,
                predictions
            )

            scores.append([name, accuracy])

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model_name = name
                best_model = model
                best_prediction = predictions

        # Save Best Model
        os.makedirs("models", exist_ok=True)

        joblib.dump(
            best_model,
            "models/best_model.pkl"
        )

        # Results Table
        result_df = pd.DataFrame(
            scores,
            columns=["Model", "Accuracy"]
        )

        st.subheader("🏆 Model Leaderboard")
        st.dataframe(result_df)

        st.metric(
            "Best Accuracy",
            f"{best_accuracy:.2%}"
        )

        st.success(
            f"Best Model: {best_model_name}"
        )

        # Confusion Matrix
        st.subheader("📉 Confusion Matrix")

        cm = confusion_matrix(
            y_test,
            best_prediction
        )

        st.write(cm)

        # Prediction Sample
        st.subheader("🔍 Prediction Sample")

        prediction_df = pd.DataFrame({
            "Actual": y_test,
            "Predicted": best_prediction
        })

        st.dataframe(prediction_df.head(20))

        # Feature Importance
        if best_model_name == "Random Forest":

            st.subheader("⭐ Top Feature Importance")

            importance_df = pd.DataFrame({
                "Feature": X.columns,
                "Importance": best_model.feature_importances_
            })

            importance_df = importance_df.sort_values(
                by="Importance",
                ascending=False
            )

            st.bar_chart(
                importance_df.head(10).set_index("Feature")
            )

        # Download Results
        csv_data = result_df.to_csv(index=False)

        st.download_button(
            "⬇ Download Results",
            csv_data,
            file_name="model_results.csv",
            mime="text/csv"
        )

        st.balloons()

        st.success("✅ Project Completed Successfully")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV dataset to begin.")