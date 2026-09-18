# Industrial Accident History Explorer

A beginner-friendly Streamlit + Groq API project for studying major
industrial accidents in:

- Refineries / downstream oil & gas
- Upstream and offshore oil & gas
- Chemical process industries
- Petrochemical industries
- Storage tanks and terminals

## Project files

```text
industrial_accident_history_app/
├── app.py
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## 1. Run locally

Install Python packages:

```bash
pip install -r requirements.txt
```

Create this file:

```text
.streamlit/secrets.toml
```

Add your Groq API key:

```toml
GROQ_API_KEY = "your_real_key_here"
```

Then run:

```bash
streamlit run app.py
```

## 2. Test in Google Colab

Install packages:

```python
!pip install streamlit groq
```

For learning/testing only, set the key temporarily:

```python
import os
os.environ["GROQ_API_KEY"] = "YOUR_KEY_HERE"
```

Do NOT upload a notebook containing your real API key to GitHub.

You can first test the Python syntax with:

```python
!python -m py_compile app.py
```

A successful syntax check normally returns no error message.

## 3. Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload:
   - app.py
   - requirements.txt
   - .gitignore
3. Do NOT upload your real `.streamlit/secrets.toml`.
4. In Streamlit Community Cloud, create a new app from the repository.
5. Set the main file path to `app.py`.
6. Open the app's Secrets settings.
7. Add:

```toml
GROQ_API_KEY = "your_real_groq_key"
```

8. Deploy the app.

## 4. Add another accident

In `app.py`, find the `ACCIDENTS` dictionary.

Example:

```python
"Refinery / Downstream Oil & Gas": [
    "BP Texas City Refinery Explosion (USA, 2005)",
    "Your New Accident (Country, Year)"
]
```

No other code needs to change.

## Important engineering note

The app uses an LLM to explain historical accidents. The accident names are
curated, but generated details can still contain errors. For professional,
academic, or safety-critical use, verify casualty data, investigation findings,
and recommendations against official sources such as CSB, HSE, OSHA,
government commissions, regulatory agencies, and official investigation reports.
