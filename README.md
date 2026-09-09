# RheoVix

## Files

- `app.py` — entry point. Run this with `streamlit run app.py`. Sets page config once and switches between the two views below via `st.session_state["view"]`.
- `landing.py` — the new premium launch page (hero, animated rheometer diagram, flow-behavior toggle, model cards, CTA panel, footer).
- `analysis_app.py` — your original analysis suite (Steps 1–3: upload, header/column mapping, model fitting & plots), unchanged in logic, just wrapped in `render_analysis_suite()`.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How the handoff works

- The app opens on the landing page (`st.session_state["view"] = "landing"`).
- Any "Launch Analysis" / "Launch RheoVix Studio" button sets `view = "app"` and reruns — this mounts your existing analysis suite exactly as it was, sidebar and all.
- A "← Back to RheoVix Home" button is now the first item in the analysis suite's sidebar, so users can return to the landing page without losing their uploaded data (it stays cached in `st.session_state` either way).

## Logo

Both `landing.py` and `analysis_app.py` try to load `logo.png` from the working directory (same behavior as your original code) and fall back to a text wordmark if it isn't found. Drop your actual `logo.png` next to `app.py` to use it.

## Notes on the landing page content

- The model cards only list **Power Law, Bingham, and Herschel–Bulkley** — the three models actually fitted in `analysis_app.py`. Casson and a standalone Newtonian fit aren't implemented in the analysis engine, so they aren't advertised.
- The file-format pipeline graphic lists **CSV · XLSX · XLS** only, matching the actual `st.file_uploader` types (the original design brief mentioned `.txt`, which isn't currently accepted).
- The "data → fitted curve" animation and its R² value are explicitly labeled illustrative/demo, not real results, per the brief's instruction not to fabricate scientific claims.
- All flow/rheometer animation is pure CSS/SVG (no extra JS dependency), respects `prefers-reduced-motion`, and won't trigger Streamlit reruns on its own — only the shear-rate slider and the flow-behavior radio buttons trigger reruns, and both are cheap.
