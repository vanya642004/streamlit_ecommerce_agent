```
# E-commerce Data Chatbot

A Streamlit app that uses a local Llama model to translate natural language questions into SQL, query your e-commerce datasets, and respond conversationally.

## Setup
1. Clone this repo.
2. Place your CSVs in `data/` as shown.
3. Download a GGML Llama model and place `ggml-model.bin` in `models/`.
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   streamlit run main.py
   ```

## Bonus
- Add Matplotlib/Plotly for charting within the chain’s response logic.
- Use `st.write()` or `st.plotly_chart()` when the SQL output is numeric for visual insights.
```

---
