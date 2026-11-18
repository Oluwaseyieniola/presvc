# Farm-to-Fork Intelligence — Streamlit prototype

A clickable demonstration of the integrated Farm-to-Fork architecture.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, normally http://localhost:8501.

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, and this README.
2. Open https://share.streamlit.io/ and sign in.
3. Select the repository, branch, and `app.py`.
4. Deploy.

## Important

This is an interactive architecture prototype. All farms, lots, observations, safety statuses and nutrient values are illustrative. Form changes are held in Streamlit session state only. There is no production database, authentication, regulatory rules engine, laboratory integration, wearable connection or live sensor feed yet.

The prototype intentionally distinguishes safety assessment from release authority, and reference food composition from batch-specific laboratory measurements.
