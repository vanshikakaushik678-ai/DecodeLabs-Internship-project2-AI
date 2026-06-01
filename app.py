import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

st.title("AI Classification Dashboard")
st.markdown("""
### Objective
Predict target classes using supervised learning algorithms and compare model performance.
""")
uploaded = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded:

    df = pd.read_csv(uploaded)

    st.write(df.head())

    target = st.selectbox(
        "Choose Target Column",
        df.columns
    )

    X = df.drop(
        target,
        axis=1
    )

    y = df[target]

    for col in X.columns:

        if X[col].dtype == "object":

            X[col] = (
                LabelEncoder()
                .fit_transform(X[col])
            )

    if y.dtype == "object":

        y = (
            LabelEncoder()
            .fit_transform(y)
        )

    X_train,X_test,y_train,y_test=(
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    model = (
        RandomForestClassifier()
    )

    model.fit(
        X_train,
        y_train
    )

    prediction = (
        model.predict(
            X_test
        )
    )

    acc = (
        accuracy_score(
            y_test,
            prediction
        )
    )

    st.success(
        f"Accuracy: {acc:.2f}"
    )