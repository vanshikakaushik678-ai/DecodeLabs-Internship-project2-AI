import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix
)

from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.tree import (
    DecisionTreeClassifier
)

from sklearn.svm import (
    SVC
)

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Advanced AI Classification Dashboard",
    layout="wide"
)

st.title(
    "🧠 Advanced AI Classification Dashboard"
)

st.markdown("""
### Objective
Predict target classes using supervised learning algorithms and compare model performance.
""")

# -------------------------
# FILE UPLOAD
# -------------------------

uploaded = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

# -------------------------
# MAIN
# -------------------------

if uploaded:

    df = pd.read_csv(uploaded)

    st.subheader(
        "Dataset Preview"
    )

    st.dataframe(
        df.head()
    )

    st.subheader(
        "Dataset Statistics"
    )

    st.write(
        df.describe()
    )

    st.subheader(
        "Dataset Shape"
    )

    st.write(
        f"Rows: {df.shape[0]}"
    )

    st.write(
        f"Columns: {df.shape[1]}"
    )

    # -------------------------
    # TARGET COLUMN
    # -------------------------

    target = st.selectbox(
        "Select Target Column",
        df.columns
    )

    st.write(
        f"Selected Target: {target}"
    )

    X = df.drop(
        columns=[target]
    )

    y = df[target]

    # -------------------------
    # ENCODING
    # -------------------------

    for col in X.columns:

        if X[col].dtype == "object":

            encoder = LabelEncoder()

            X[col] = (
                encoder.fit_transform(
                    X[col]
                    .astype(str)
                )
            )

    if y.dtype == "object":

        y = (
            LabelEncoder()
            .fit_transform(
                y.astype(str)
            )
        )

    # -------------------------
    # TRAIN TEST SPLIT
    # -------------------------

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42

        )

    )

    st.subheader(
        "Train Test Split"
    )

    st.write(
        f"Train Rows: {len(X_train)}"
    )

    st.write(
        f"Test Rows: {len(X_test)}"
    )

    # -------------------------
    # MODELS
    # -------------------------

    models = {

        "Random Forest":

        RandomForestClassifier(
            n_estimators=300,
            random_state=42
        ),

        "Decision Tree":

        DecisionTreeClassifier(),

        "SVM":

        SVC()

    }

    scores = []

    best_accuracy = 0

    best_model_name = ""

    best_prediction = None

    best_model = None

    # -------------------------
    # TRAINING
    # -------------------------

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        pred = (
            model.predict(
                X_test
            )
        )

        acc = (
            accuracy_score(
                y_test,
                pred
            )
        )

        scores.append(
            [
                name,
                acc
            ]
        )

        if acc > best_accuracy:

            best_accuracy = acc

            best_model_name = name

            best_prediction = pred

            best_model = model

    result = (

        pd.DataFrame(

            scores,

            columns=[

                "Model",

                "Accuracy"

            ]

        )

    )

    # -------------------------
    # LEADERBOARD
    # -------------------------

    st.subheader(
        "🏆 Model Leaderboard"
    )

    st.dataframe(
        result
    )

    st.metric(
        "Best Accuracy",
        f"{best_accuracy:.2%}"
    )

    st.success(
        f"Best Model → {best_model_name}"
    )

    # -------------------------
    # CONFUSION MATRIX
    # -------------------------

    st.subheader(
        "Confusion Matrix"
    )

    cm = (

        confusion_matrix(

            y_test,

            best_prediction

        )

    )

    st.write(
        cm
    )

    # -------------------------
    # PREDICTIONS
    # -------------------------

    st.subheader(
        "Prediction Sample"
    )

    prediction_df = (

        pd.DataFrame({

            "Actual":

            y_test,

            "Predicted":

            best_prediction

        })

    )

    st.dataframe(

        prediction_df

        .head(20)

    )

    # -------------------------
    # FEATURE IMPORTANCE
    # -------------------------

    if best_model_name == "Random Forest":

        st.subheader(
            "Top Feature Importance"
        )

        importance = (

            pd.DataFrame({

                "Feature":
                X.columns,

                "Importance":

                best_model
                .feature_importances_

            })

        )

        importance = (

            importance

            .sort_values(

                by="Importance",

                ascending=False

            )

        )

        st.bar_chart(

            importance

            .head(10)

            .set_index(
                "Feature"
            )

        )

    # -------------------------
    # DOWNLOAD
    # -------------------------

    csv = (

        result

        .to_csv(

            index=False

        )

    )

    st.download_button(

        "⬇ Download Results",

        csv,

        "model_results.csv",

        "text/csv"

    )

    st.balloons()

    st.success(
        "Project Completed Successfully"
    )