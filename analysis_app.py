"""
RheoVix — Analysis Suite (with PDF Export & Unicode-Safe Header)
----------------------------------------------------------------
"""

import streamlit as st

# ---------------------------------------------------------------------------
# NumPy 2.0 Compatibility Patch (Must be at the absolute top)
# ---------------------------------------------------------------------------
import numpy as np
if not hasattr(np, "long"):
    np.long = int
if not hasattr(np, "ulong"):
    np.ulong = int
if not hasattr(np, "float_"):
    np.float_ = float
if not hasattr(np, "int_"):
    np.int_ = int
# ---------------------------------------------------------------------------

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
from scipy.optimize import curve_fit

# PDF Generation Import
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "RheoVix - Rheological Analysis Report", 0, 1, "C")
        self.set_font("helvetica", "I", 9)
        self.cell(0, 5, "Automated Model Fitting & Parameter Summary", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def render_analysis_suite():
    # -----------------------------------------------------------------------
    # Session State Initialization
    # -----------------------------------------------------------------------

    if "step" not in st.session_state:
        st.session_state["step"] = "1. Upload & Sheets"
    if "uploaded_files_cache" not in st.session_state:
        st.session_state["uploaded_files_cache"] = {}
    if "file_sheets_available" not in st.session_state:
        st.session_state["file_sheets_available"] = {}
    if "selected_file_sheets" not in st.session_state:
        st.session_state["selected_file_sheets"] = {}
    if "sheet_purpose" not in st.session_state:
        st.session_state["sheet_purpose"] = "Upward & Downward Curves (Loop Analysis)"
    if "mapping" not in st.session_state:
        st.session_state["mapping"] = {}
    if "skiprows" not in st.session_state:
        st.session_state["skiprows"] = 0

    # -----------------------------------------------------------------------
    # Helper Functions
    # -----------------------------------------------------------------------

    def parse_sample_name(filename: str) -> str:
        base = re.sub(r'\.(xlsx|xls|csv)$', '', filename, flags=re.IGNORECASE)
        base_clean = re.sub(r'[\s_\-]*(rep|r)?\d+$', '', base, flags=re.IGNORECASE)
        return base_clean if base_clean else base

    def calculate_goodness_of_fit(y_true, y_pred, num_params):
        n = len(y_true)
        if n <= num_params + 1:
            return {"r2": 0.0, "adj_r2": 0.0, "rmse": 0.0, "chi_sq": 0.0}
        residuals = y_true - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_true - np.mean(y_true))**2)
        r2 = max(0.0, 1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0
        adj_r2 = 1.0 - ((1.0 - r2) * (n - 1) / (n - num_params - 1))
        rmse = np.sqrt(np.mean(residuals**2))
        chi_sq = np.sum((residuals**2) / np.maximum(np.abs(y_pred), 1e-8))
        return {"r2": r2, "adj_r2": adj_r2, "rmse": rmse, "chi_sq": chi_sq}

    def add_curve_with_sparse_markers(fig, x, y, name, color, shape, size, showlegend=True, row=None, col=None):
        line_kwargs = dict(
            x=x, y=y, mode="lines",
            name=name, line=dict(width=2.5, color=color),
            showlegend=showlegend
        )
        if row is not None and col is not None:
            fig.add_trace(go.Scatter(**line_kwargs), row=row, col=col)
        else:
            fig.add_trace(go.Scatter(**line_kwargs))

        if shape != "none":
            step_size = max(1, len(x) // 14)
            idx_slice = slice(0, len(x), step_size)
            marker_kwargs = dict(
                x=x[idx_slice], y=y[idx_slice], mode="markers",
                name=f"{name} (markers)",
                marker=dict(symbol=shape, size=size, color=color),
                showlegend=False
            )
            if row is not None and col is not None:
                fig.add_trace(go.Scatter(**marker_kwargs), row=row, col=col)
            else:
                fig.add_trace(go.Scatter(**marker_kwargs))

    # -----------------------------------------------------------------------
    # Sidebar Navigation
    # -----------------------------------------------------------------------

    with st.sidebar:
        if st.button("← Back to RheoVix Home", use_container_width=True):
            st.session_state["view"] = "landing"
            st.rerun()

        try:
            st.image("logo.png", use_container_width=True)
        except Exception:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 2rem;">🔬</span>
                    <div>
                        <h2 style="margin: 0; line-height: 1.1; font-size: 1.5rem;">RHEOVIX</h2>
                        <span style="font-size: 0.75rem; opacity: 0.8;">Advanced Suite</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.caption("v2.14.2-PublicationReady")
        st.markdown("---")

        steps = ["1. Upload & Sheets", "2. Headers & Mapping", "3. Analytics & Advanced Plots"]
        for s in steps:
            if st.button(s, use_container_width=True, type="primary" if st.session_state["step"] == s else "secondary"):
                st.session_state["step"] = s

        st.markdown("---")
        st.markdown("**Workflow Status**")
        if st.session_state["uploaded_files_cache"]:
            st.success(f"📁 {len(st.session_state['uploaded_files_cache'])} file(s) active.")
        else:
            st.info("No files loaded.")

    # -----------------------------------------------------------------------
    # Step 1: Upload & Batch Sheet Selection
    # -----------------------------------------------------------------------

    if st.session_state["step"] == "1. Upload & Sheets":
        st.header("1. File Upload & Multi-Sheet Configuration")
        st.caption("Upload raw rheometer exports. State is fully cached so you can navigate freely without data loss.")

        uploaded_files = st.file_uploader(
            "Choose file(s) (.xlsx, .xls, .csv)",
            type=["xlsx", "xls", "csv"],
            accept_multiple_files=True
        )

        if uploaded_files:
            for f in uploaded_files:
                if f.name not in st.session_state["uploaded_files_cache"]:
                    st.session_state["uploaded_files_cache"][f.name] = f.getvalue()
                    if f.name.endswith((".xlsx", ".xls")):
                        try:
                            xls = pd.ExcelFile(f)
                            sheets = xls.sheet_names
                            st.session_state["file_sheets_available"][f.name] = sheets
                            st.session_state["selected_file_sheets"][f.name] = sheets[:1]
                            st.session_state[f"manual_sheet_{f.name}"] = sheets[:1]
                        except Exception as e:
                            st.error(f"Could read sheets for {f.name}: {e}")
                    else:
                        st.session_state["file_sheets_available"][f.name] = ["CSV Data"]
                        st.session_state["selected_file_sheets"][f.name] = ["CSV Data"]
                        st.session_state[f"manual_sheet_{f.name}"] = ["CSV Data"]

        if st.session_state["uploaded_files_cache"]:
            st.markdown("---")
            st.markdown("### 🧬 Multi-Sheet Purpose Selection")

            st.session_state["sheet_purpose"] = st.selectbox(
                "What do multiple sheets represent in your workbooks?",
                options=[
                    "Upward & Downward Curves (Thixotropic Loop Analysis)",
                    "Independent Test Replicates / Separate Runs",
                    "Sequential Flow Segments / Multi-step Protocols"
                ],
                index=0 if "Loop" in st.session_state["sheet_purpose"] else 0,
            )

            st.markdown("---")
            st.markdown("### ⚡ Sheet Selection Manager")

            all_sheets_sets = [set(sheets) for sheets in st.session_state["file_sheets_available"].values()]
            common_sheets = list(set.intersection(*all_sheets_sets)) if all_sheets_sets else ["Sheet1"]

            col_glob1, col_glob2 = st.columns([2, 1])
            with col_glob1:
                global_choice = st.multiselect(
                    "Target sheet(s) to apply across files:",
                    options=common_sheets if common_sheets else ["Sheet1"],
                    default=common_sheets[:1] if common_sheets else ["Sheet1"]
                )
            with col_glob2:
                st.write("")
                st.write("")
                if st.button("Apply to All Files", type="secondary"):
                    for fname in st.session_state["file_sheets_available"].keys():
                        st.session_state["selected_file_sheets"][fname] = global_choice
                        st.session_state[f"manual_sheet_{fname}"] = global_choice
                    st.success("Applied globally and synced!")

            with st.expander("🛠️ Manual Override: Inspect or change individual files"):
                updated_selections = {}
                for filename, available_sheets in st.session_state["file_sheets_available"].items():
                    current_sel = st.session_state["selected_file_sheets"].get(filename, global_choice)
                    chosen = st.multiselect(
                        f"Sheets for `{filename}`:",
                        options=available_sheets,
                        default=current_sel,
                        key=f"manual_sheet_{filename}"
                    )
                    updated_selections[filename] = chosen
                st.session_state["selected_file_sheets"] = updated_selections

            st.write("")
            if st.button("Proceed to Headers & Mapping →", type="primary"):
                total_selected = sum(len(sheets) for sheets in st.session_state["selected_file_sheets"].values())
                if total_selected == 0:
                    st.error("Please select at least one sheet to analyze.")
                else:
                    st.session_state["step"] = "2. Headers & Mapping"
                    st.rerun()

    # -----------------------------------------------------------------------
    # Step 2: Headers & Column Mapping
    # -----------------------------------------------------------------------

    elif st.session_state["step"] == "2. Headers & Mapping":
        st.header("2. Configure Headers & Map Columns")

        cache = st.session_state["uploaded_files_cache"]
        selected_file_sheets = st.session_state["selected_file_sheets"]

        if not cache:
            st.warning("No files found in session cache. Please upload files in Step 1.")
            if st.button("← Back to Upload"):
                st.session_state["step"] = "1. Upload & Sheets"
                st.rerun()
            st.stop()

        header_row = st.number_input(
            "Row number where actual column headers start (skips instrument metadata):",
            min_value=1, value=st.session_state.get("skiprows", 0) + 1, step=1,
        )
        skiprows = header_row - 1
        st.session_state["skiprows"] = skiprows

        ref_cols = []
        ref_info = ""
        for filename, sheets in selected_file_sheets.items():
            if sheets:
                first_sheet = sheets[0]
                try:
                    file_bytes = cache[filename]
                    if filename.endswith(".csv"):
                        temp_df = pd.read_csv(io.BytesIO(file_bytes), skiprows=skiprows)
                    else:
                        temp_df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=first_sheet, skiprows=skiprows)
                    ref_cols = list(temp_df.columns)
                    ref_info = f"{filename} (Sheet: {first_sheet})"
                    break
                except Exception as e:
                    st.error(f"Error previewing {filename}: {e}")

        if not ref_cols:
            st.error("Could not load columns. Verify header row index.")
            st.stop()

        st.markdown("---")
        st.caption(f"Mapping columns using reference structure from: **{ref_info}**")

        col1, col2, col3 = st.columns(3)
        with col1:
            sr_col = st.selectbox("Shear Rate column", options=["None"] + ref_cols)
        with col2:
            eta_col = st.selectbox("Viscosity column", options=["None"] + ref_cols)
        with col3:
            stress_col = st.selectbox("Shear Stress column (Recommended)", options=["None"] + ref_cols)

        col_nav1, col_nav2 = st.columns([1, 1])
        with col_nav1:
            if st.button("← Back to Sheets"):
                st.session_state["step"] = "1. Upload & Sheets"
                st.rerun()
        with col_nav2:
            if st.button("Confirm Mapping & Analyze →", type="primary"):
                if sr_col == "None" or (eta_col == "None" and stress_col == "None"):
                    st.error("You must map at least Shear Rate and either Viscosity or Shear Stress.")
                else:
                    st.session_state["mapping"] = {
                        "shear_rate": sr_col,
                        "viscosity": None if eta_col == "None" else eta_col,
                        "stress": None if stress_col == "None" else stress_col,
                    }
                    st.session_state["step"] = "3. Analytics & Advanced Plots"
                    st.rerun()

    # -----------------------------------------------------------------------
    # Step 3: Analytics & Advanced Plots Module
    # -----------------------------------------------------------------------

    elif st.session_state["step"] == "3. Analytics & Advanced Plots":
        st.header("3. Per-Sample Analytics, Model Fitting & Publication Visualizations")

        cache = st.session_state["uploaded_files_cache"]
        selected_file_sheets = st.session_state["selected_file_sheets"]
        mapping = st.session_state["mapping"]
        skiprows = st.session_state.get("skiprows", 0)
        sheet_purpose = st.session_state.get("sheet_purpose", "")

        sr_col = mapping.get("shear_rate")
        eta_col = mapping.get("viscosity")
        tau_col = mapping.get("stress")

        if not sr_col or not cache:
            st.warning("Please complete mapping first.")
            if st.button("Back to Mapping"):
                st.session_state["step"] = "2. Headers & Mapping"
                st.rerun()
            st.stop()

        combined_list = []
        for filename, sheets in selected_file_sheets.items():
            file_bytes = cache[filename]
            sample_group = parse_sample_name(filename)

            for sheet in sheets:
                try:
                    if filename.endswith(".csv"):
                        df = pd.read_csv(io.BytesIO(file_bytes), skiprows=skiprows)
                    else:
                        df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet, skiprows=skiprows)

                    has_sr = sr_col in df.columns
                    has_eta = eta_col in df.columns if eta_col else False
                    has_tau = tau_col in df.columns if tau_col else False

                    if has_sr and (has_eta or has_tau):
                        sub = pd.DataFrame()
                        sub[sr_col] = pd.to_numeric(df[sr_col], errors="coerce")

                        if has_tau:
                            sub["Stress"] = pd.to_numeric(df[tau_col], errors="coerce")
                        elif has_eta:
                            visc = pd.to_numeric(df[eta_col], errors="coerce")
                            sub["Stress"] = visc * sub[sr_col]

                        if has_eta:
                            sub["Viscosity"] = pd.to_numeric(df[eta_col], errors="coerce")
                        else:
                            sub["Viscosity"] = sub["Stress"] / sub[sr_col]

                        sub = sub[(sub[sr_col] > 0) & (sub["Viscosity"] > 0) & (sub["Stress"] >= 0)].dropna()

                        sub["File Name"] = filename
                        sub["Sample Group"] = sample_group
                        sub["Sheet"] = sheet
                        sub["Dataset Label"] = f"{sample_group} | {filename} [{sheet}]"

                        combined_list.append(sub)
                except Exception as e:
                    st.error(f"Error processing {filename} (Sheet: {sheet}): {e}")

        if not combined_list:
            st.error("No valid numeric data found matching your mappings.")
            st.stop()

        analysis_df = pd.concat(combined_list, ignore_index=True)

        st.info(f"📌 **Active Sheet Interpretation Mode:** {sheet_purpose}")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("← Modify Sheets or Upload"):
                st.session_state["step"] = "1. Upload & Sheets"
                st.rerun()
        with col_btn2:
            if st.button("← Modify Column Mapping"):
                st.session_state["step"] = "2. Headers & Mapping"
                st.rerun()

        st.markdown("---")
        unique_samples = sorted(analysis_df["Sample Group"].unique())

        selected_samples = st.multiselect(
            "Select Sample Group(s) to Include:",
            options=unique_samples,
            default=unique_samples
        )

        if not selected_samples:
            st.warning("Please select at least one sample group.")
            st.stop()

        # -----------------------------------------------------------------------
        # Model Fitting Range Configuration (Analysis Range)
        # -----------------------------------------------------------------------
        st.markdown("### 📐 Step A: Model Fitting Range (Analysis)")
        st.caption("Select the shear rate range to be used when fitting rheological models (Power Law, Bingham, Herschel-Bulkley). This excludes wall slip or high-shear noise from parameter estimation.")

        global_min_sr = float(analysis_df[sr_col].min())
        global_max_sr = float(analysis_df[sr_col].max())

        fit_col1, fit_col2 = st.columns(2)
        with fit_col1:
            fit_min_sr = st.number_input("Min Shear Rate for Fitting (1/s)", value=global_min_sr, min_value=0.0, step=0.01)
        with fit_col2:
            fit_max_sr = st.number_input("Max Shear Rate for Fitting (1/s)", value=global_max_sr, min_value=0.0, step=0.1)

        fitted_source_df = analysis_df[
            (analysis_df["Sample Group"].isin(selected_samples)) &
            (analysis_df[sr_col] >= fit_min_sr) &
            (analysis_df[sr_col] <= fit_max_sr)
        ]

        # -----------------------------------------------------------------------
        # Color mapping for distinct samples
        # -----------------------------------------------------------------------
        palette = px.colors.qualitative.Plotly + px.colors.qualitative.Dark24 + px.colors.qualitative.Bold
        sample_color_map = {sample: palette[i % len(palette)] for i, sample in enumerate(unique_samples)}

        # -----------------------------------------------------------------------
        # Per-Sample Model Fitting Dictionary & Detailed Parameters Storage
        # -----------------------------------------------------------------------
        per_sample_results = {}
        replicate_fitted_curves = {}

        for sample in selected_samples:
            s_df = fitted_source_df[fitted_source_df["Sample Group"] == sample]
            per_sample_results[sample] = {}
            replicate_fitted_curves[sample] = {"Power Law": [], "Bingham": [], "Herschel-Bulkley": [], "rep_details": []}

            if len(s_df) > 0:
                sr_min, sr_max = s_df[sr_col].min(), s_df[sr_col].max()
                sr_smooth = np.logspace(np.log10(sr_min), np.log10(sr_max), 200)
                replicate_fitted_curves[sample]["sr_smooth"] = sr_smooth

                for (fname, sheet), rep_df in s_df.groupby(["File Name", "Sheet"]):
                    sr_r = rep_df[sr_col].values
                    tau_r = rep_df["Stress"].values

                    if len(sr_r) < 3:
                        continue

                    rep_record = {"file": fname, "sheet": sheet, "sr_smooth": sr_smooth}

                    # Power Law
                    try:
                        def power_law(sr, K, n):
                            return K * (sr**n)
                        popt_pl, _ = curve_fit(power_law, sr_r, tau_r, p0=[1.0, 0.5], bounds=([0, 0], [np.inf, 2.0]))
                        eta_pl_curve = power_law(sr_smooth, *popt_pl) / sr_smooth
                        replicate_fitted_curves[sample]["Power Law"].append(eta_pl_curve)
                        rep_record["PL_Viscosity"] = eta_pl_curve
                    except Exception:
                        pass

                    # Bingham
                    try:
                        def bingham(sr, tau0, etap):
                            return tau0 + etap * sr
                        popt_bi, _ = curve_fit(bingham, sr_r, tau_r, p0=[0.1, 0.1], bounds=([0, 0], [np.inf, np.inf]))
                        eta_bi_curve = bingham(sr_smooth, *popt_bi) / sr_smooth
                        replicate_fitted_curves[sample]["Bingham"].append(eta_bi_curve)
                        rep_record["Bingham_Viscosity"] = eta_bi_curve
                    except Exception:
                        pass

                    # Herschel-Bulkley
                    try:
                        def hb(sr, tau0, K, n):
                            return tau0 + K * (sr**n)
                        popt_hb, _ = curve_fit(hb, sr_r, tau_r, p0=[0.1, 1.0, 0.5], bounds=([0, 0, 0], [np.inf, np.inf, 2.0]), maxfev=5000)
                        eta_hb_curve = hb(sr_smooth, *popt_hb) / sr_smooth
                        replicate_fitted_curves[sample]["Herschel-Bulkley"].append(eta_hb_curve)
                        rep_record["HB_Viscosity"] = eta_hb_curve
                    except Exception:
                        pass

                    replicate_fitted_curves[sample]["rep_details"].append(rep_record)

            sr_s = s_df[sr_col].values
            tau_s = s_df["Stress"].values
            if len(sr_s) >= 3:
                try:
                    popt_pl, _ = curve_fit(lambda sr, K, n: K * (sr**n), sr_s, tau_s, p0=[1.0, 0.5], bounds=([0, 0], [np.inf, 2.0]))
                    pred_pl = popt_pl[0] * (sr_s**popt_pl[1])
                    per_sample_results[sample]["Power Law"] = {
                        "params": {"K": popt_pl[0], "n": popt_pl[1]},
                        "metrics": calculate_goodness_of_fit(tau_s, pred_pl, num_params=2)
                    }
                except Exception:
                    pass

                try:
                    popt_bi, _ = curve_fit(lambda sr, tau0, etap: tau0 + etap * sr, sr_s, tau_s, p0=[0.1, 0.1], bounds=([0, 0], [np.inf, np.inf]))
                    pred_bi = popt_bi[0] + popt_bi[1]*sr_s
                    per_sample_results[sample]["Bingham"] = {
                        "params": {"tau_0": popt_bi[0], "eta_plastic": popt_bi[1]},
                        "metrics": calculate_goodness_of_fit(tau_s, pred_bi, num_params=2)
                    }
                except Exception:
                    pass

                try:
                    popt_hb, _ = curve_fit(lambda sr, tau0, K, n: tau0 + K * (sr**n), sr_s, tau_s, p0=[0.1, 1.0, 0.5], bounds=([0, 0, 0], [np.inf, np.inf, 2.0]), maxfev=5000)
                    pred_hb = popt_hb[0] + popt_hb[1]*(sr_s**popt_hb[2])
                    per_sample_results[sample]["Herschel-Bulkley"] = {
                        "params": {"tau_0": popt_hb[0], "K": popt_hb[1], "n": popt_hb[2]},
                        "metrics": calculate_goodness_of_fit(tau_s, pred_hb, num_params=3)
                    }
                except Exception:
                    pass

        # -----------------------------------------------------------------------
        # Summary Section: Automated Best-Fit & Detailed Parameters Summary
        # -----------------------------------------------------------------------
        st.markdown("### 🏆 Automated Model Suggestions & Detailed Parameter Summary")

        summary_data = []
        for sample, models in per_sample_results.items():
            if models:
                best_model_name, best_model_data = max(models.items(), key=lambda x: x[1]["metrics"]["adj_r2"])
                row_data = {
                    "Sample Group": sample,
                    "Recommended Best Fit": best_model_name,
                    "Adjusted R²": round(best_model_data["metrics"]["adj_r2"], 4),
                    "RMSE (Pa)": round(best_model_data["metrics"]["rmse"], 4)
                }
                summary_data.append(row_data)

        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            model_counts = summary_df["Recommended Best Fit"].value_counts()
            count_str = " | ".join([f"**{model}**: {count} sample(s)" for model, count in model_counts.items()])
            st.markdown(f"📊 **Model Distribution:** {count_str}")
            st.dataframe(summary_df, use_container_width=True)

            # -----------------------------------------------------------------------
            # PDF Report Download Feature
            # -----------------------------------------------------------------------
            def generate_pdf_report(summary_table):
                pdf = PDFReport(orientation='P', unit='mm', format='A4')
                pdf.add_page()
                pdf.set_font("helvetica", "", 10)
                
                pdf.cell(0, 8, "Summary of Fitted Rheological Models", 0, 1, "L")
                pdf.set_font("helvetica", "B", 9)
                
                # Table Header
                col_widths = [50, 50, 40, 45]
                headers = ["Sample Group", "Best Fit Model", "Adjusted R^2", "RMSE (Pa)"]
                for i, h in enumerate(headers):
                    pdf.cell(col_widths[i], 7, h, 1, 0, "C")
                pdf.ln()
                
                # Table Rows
                pdf.set_font("helvetica", "", 9)
                for index, row in summary_table.iterrows():
                    pdf.cell(col_widths[0], 6, str(row["Sample Group"]), 1, 0, "L")
                    pdf.cell(col_widths[1], 6, str(row["Recommended Best Fit"]), 1, 0, "C")
                    pdf.cell(col_widths[2], 6, str(row["Adjusted R²"]), 1, 0, "C")
                    pdf.cell(col_widths[3], 6, str(row["RMSE (Pa)"]), 1, 0, "C")
                    pdf.ln()
                    
                return bytes(pdf.output())

            pdf_bytes = generate_pdf_report(summary_df)
            st.download_button(
                label="📄 Download PDF Summary Report",
                data=pdf_bytes,
                file_name="RheoVix_Analysis_Report.pdf",
                mime="application/pdf"
            )

            st.markdown("#### 🔬 Detailed Fitted Parameters per Model & Sample")

            param_model_filter = st.selectbox(
                "Select Model to View Parameters:",
                options=["All Models", "Power Law", "Bingham", "Herschel-Bulkley"],
                key="param_model_selector"
            )

            detail_rows = []
            for sample, models in per_sample_results.items():
                for m_name, m_info in models.items():
                    p_dict = m_info["params"]
                    m_mets = m_info["metrics"]
                    detail_rows.append({
                        "Sample Group": sample,
                        "Model": m_name,
                        "Param 1 (K or tau_0)": round(p_dict.get("K", p_dict.get("tau_0", 0.0)), 4),
                        "Param 2 (n or eta_p)": round(p_dict.get("n", p_dict.get("eta_plastic", 0.0)), 4),
                        "Param 3 (n for HB)": round(p_dict.get("n", 0.0) if m_name == "Herschel-Bulkley" else 0.0, 4),
                        "Adj. R²": round(m_mets["adj_r2"], 4),
                        "RMSE (Pa)": round(m_mets["rmse"], 4)
                    })

            if detail_rows:
                detail_df = pd.DataFrame(detail_rows)
                if param_model_filter != "All Models":
                    detail_df = detail_df[detail_df["Model"] == param_model_filter]
                st.dataframe(detail_df, use_container_width=True)
        else:
            st.info("Insufficient data for automated suggestions.")

        # -----------------------------------------------------------------------
        # Visualization & Publication Styling Options
        # -----------------------------------------------------------------------
        st.markdown("---")
        st.markdown("### 🎨 Step B: Figure Styling & Manual Plotting Range")

        with st.expander("⚙️ Customize Figure Styling (Fonts, Grid & Markers)", expanded=True):
            c_p1, c_p2, c_p3, c_p4 = st.columns(4)
            with c_p1:
                font_family = st.selectbox("Font Family", ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana"], index=0)
            with c_p2:
                font_size = st.selectbox("Base Font Size", options=[10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24], index=4)
            with c_p3:
                marker_shape = st.selectbox("Marker Shape", options=["circle", "diamond", "square", "triangle-up", "none"], index=0)
            with c_p4:
                marker_size = st.slider("Marker Size", min_value=2, max_value=14, value=7)

            show_grid = st.checkbox("Show Gridlines", value=True)

        bg_hex = "#FFFFFF"

        v_col1, v_col2, v_col3 = st.columns(3)
        with v_col1:
            x_scale_type = st.selectbox("X-Axis Scale", ["Logarithmic", "Linear"], index=0)
        with v_col2:
            y_scale_type = st.selectbox("Y-Axis Scale", ["Logarithmic", "Linear"], index=0)
        with v_col3:
            plot_layout_mode = st.selectbox(
                "Figure Layout Mode",
                [
                    "All Samples Together (Single Plot)",
                    "Single Sample Detail View",
                    "3x3 Subplot Grid",
                    "Individual Sample Carousel / Cards"
                ]
            )

        is_log_x = (x_scale_type == "Logarithmic")
        is_log_y = (y_scale_type == "Logarithmic")

        overlay_model = st.selectbox(
            "Model for Averaged Replicate Curve:",
            options=["Power Law", "Bingham", "Herschel-Bulkley"],
            index=0
        )

        # -----------------------------------------------------------------------
        # Manual Plotting Range Controls (Figure Range)
        # -----------------------------------------------------------------------
        st.markdown("#### 📐 Manual Plotting Range (Visualization Limits)")
        st.caption("Manually adjust the shear rate (X-axis) and viscosity (Y-axis) boundaries displayed on your figures, independent of the model fitting range.")

        all_x_vals = analysis_df[sr_col].values if len(analysis_df) > 0 else [1, 100]
        all_y_vals = analysis_df["Viscosity"].values if len(analysis_df) > 0 else [0.01, 10]

        def_xmin, def_xmax = float(max(1e-4, np.min(all_x_vals))), float(np.max(all_x_vals))
        def_ymin, def_ymax = float(max(1e-6, np.min(all_y_vals))), float(np.max(all_y_vals))

        c_r1, c_r2 = st.columns(2)
        with c_r1:
            plot_xmin = st.number_input("Plot Min Shear Rate (X-axis)", value=def_xmin, format="%.4g", key="plot_xmin_input")
            plot_xmax = st.number_input("Plot Max Shear Rate (X-axis)", value=def_xmax, format="%.4g", key="plot_xmax_input")
        with c_r2:
            plot_ymin = st.number_input("Plot Min Viscosity (Y-axis)", value=def_ymin, format="%.4g", key="plot_ymin_input")
            plot_ymax = st.number_input("Plot Max Viscosity (Y-axis)", value=def_ymax, format="%.4g", key="plot_ymax_input")

        def apply_publication_layout(fig, title_text, x_title="Shear Rate (1/s)", y_title="Viscosity (Pa·s)", is_grid=False) -> go.Figure:
            def get_strict_decade_ticks_and_bounds(min_val, max_val):
                if min_val <= 0 or max_val <= 0:
                    return min_val, max_val, None, None

                bound_min = min_val
                bound_max = max_val

                lower_exp = int(np.floor(np.log10(min_val)))
                upper_exp = int(np.ceil(np.log10(max_val)))

                tick_vals = []
                tick_text = []

                for i in range(lower_exp, upper_exp + 1):
                    major = 10.0 ** i
                    if bound_min <= major <= bound_max:
                        tick_vals.append(major)
                        if major >= 1:
                            tick_text.append(f"{int(major)}" if major.is_integer() else f"{major}")
                        else:
                            tick_text.append(f"{major:g}")

                    for sub in range(2, 10):
                        sub_val = sub * (10.0 ** i)
                        if bound_min <= sub_val <= bound_max:
                            tick_vals.append(sub_val)
                            tick_text.append("")

                return bound_min, bound_max, tick_vals, tick_text

            xaxis_type = "log" if is_log_x else "linear"
            yaxis_type = "log" if is_log_y else "linear"

            xaxis_kwargs = dict(
                title=dict(text=x_title, font=dict(family=font_family, size=font_size + 2, color="black")),
                type=xaxis_type,
                showgrid=show_grid,
                gridcolor="rgba(211,211,211,0.5)" if show_grid else "transparent",
                zeroline=False,
                showline=True,
                linewidth=1.5,
                linecolor="black",
                ticks="inside",
                tickfont=dict(family=font_family, size=font_size, color="black")
            )

            if is_log_x and plot_xmin > 0 and plot_xmax > 0:
                xmin_b, xmax_b, xtick_v, xtick_t = get_strict_decade_ticks_and_bounds(plot_xmin, plot_xmax)
                xaxis_kwargs["range"] = [np.log10(xmin_b), np.log10(xmax_b)]
                if xtick_v:
                    xaxis_kwargs["tickvals"] = xtick_v
                    xaxis_kwargs["ticktext"] = xtick_t
            else:
                xaxis_kwargs["range"] = [plot_xmin, plot_xmax]

            yaxis_kwargs = dict(
                title=dict(text=y_title, font=dict(family=font_family, size=font_size + 2, color="black")),
                type=yaxis_type,
                showgrid=show_grid,
                gridcolor="rgba(211,211,211,0.5)" if show_grid else "transparent",
                zeroline=False,
                showline=True,
                linewidth=1.5,
                linecolor="black",
                ticks="inside",
                tickfont=dict(family=font_family, size=font_size, color="black")
            )

            if is_log_y and plot_ymin > 0 and plot_ymax > 0:
                ymin_b, ymax_b, ytick_v, ytick_t = get_strict_decade_ticks_and_bounds(plot_ymin, plot_ymax)
                yaxis_kwargs["range"] = [np.log10(ymin_b), np.log10(ymax_b)]
                if ytick_v:
                    yaxis_kwargs["tickvals"] = ytick_v
                    yaxis_kwargs["ticktext"] = ytick_t
            else:
                yaxis_kwargs["range"] = [plot_ymin, plot_ymax]

            fig.update_layout(
                title=dict(text=title_text, font=dict(family=font_family, size=font_size + 4, color="black"), x=0.5, xanchor="center"),
                xaxis=xaxis_kwargs,
                yaxis=yaxis_kwargs,
                plot_bgcolor=bg_hex,
                paper_bgcolor=bg_hex,
                font=dict(family=font_family, size=font_size, color="black"),
                legend=dict(
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="rgba(0,0,0,0.2)",
                    borderwidth=1,
                    font=dict(family=font_family, size=font_size, color="black")
                ),
                margin=dict(l=80, r=50, t=80, b=80)
            )
            return fig

        # Render figures based on layout mode
        if plot_layout_mode == "All Samples Together (Single Plot)":
            fig = go.Figure()
            for sample in selected_samples:
                s_df = analysis_df[analysis_df["Sample Group"] == sample]
                color = sample_color_map[sample]
                if len(s_df) > 0:
                    add_curve_with_sparse_markers(
                        fig, s_df[sr_col].values, s_df["Viscosity"].values,
                        name=f"{sample} (Raw)", color=color, shape=marker_shape, size=marker_size
                    )
                if sample in replicate_fitted_curves and "sr_smooth" in replicate_fitted_curves[sample]:
                    curves_list = replicate_fitted_curves[sample][overlay_model]
                    if curves_list:
                        mean_curve = np.mean(curves_list, axis=0)
                        sr_smooth = replicate_fitted_curves[sample]["sr_smooth"]
                        fig.add_trace(go.Scatter(
                            x=sr_smooth, y=mean_curve, mode="lines",
                            name=f"{sample} ({overlay_model} fit)",
                            line=dict(width=3, color=color, dash="dash")
                        ))

            fig = apply_publication_layout(fig, "Viscosity vs. Shear Rate (All Samples)")
            st.plotly_chart(fig, use_container_width=True)

        elif plot_layout_mode == "Single Sample Detail View":
            chosen_sample = st.selectbox("Select Sample for Detail View", options=selected_samples)
            if chosen_sample:
                fig = go.Figure()
                s_df = analysis_df[analysis_df["Sample Group"] == chosen_sample]
                color = sample_color_map[chosen_sample]
                for (fname, sheet), rep_df in s_df.groupby(["File Name", "Sheet"]):
                    add_curve_with_sparse_markers(
                        fig, rep_df[sr_col].values, rep_df["Viscosity"].values,
                        name=f"{fname} [{sheet}]", color=color, shape=marker_shape, size=marker_size
                    )
                if chosen_sample in replicate_fitted_curves and "sr_smooth" in replicate_fitted_curves[chosen_sample]:
                    curves_list = replicate_fitted_curves[chosen_sample][overlay_model]
                    if curves_list:
                        mean_curve = np.mean(curves_list, axis=0)
                        sr_smooth = replicate_fitted_curves[chosen_sample]["sr_smooth"]
                        fig.add_trace(go.Scatter(
                            x=sr_smooth, y=mean_curve, mode="lines",
                            name=f"Mean ({overlay_model})",
                            line=dict(width=3.5, color="black", dash="dash")
                        ))
                fig = apply_publication_layout(fig, f"Detailed Replicates: {chosen_sample}")
                st.plotly_chart(fig, use_container_width=True)

        elif plot_layout_mode == "3x3 Subplot Grid":
            n_samples = len(selected_samples)
            if n_samples > 0:
                rows = min(3, (n_samples + 2) // 3)
                cols = min(3, n_samples)
                fig = make_subplots(rows=rows, cols=cols, subplot_titles=selected_samples[:9])
                for idx, sample in enumerate(selected_samples[:9]):
                    r = (idx // 3) + 1
                    c = (idx % 3) + 1
                    s_df = analysis_df[analysis_df["Sample Group"] == sample]
                    color = sample_color_map[sample]
                    if len(s_df) > 0:
                        add_curve_with_sparse_markers(
                            fig, s_df[sr_col].values, s_df["Viscosity"].values,
                            name=sample, color=color, shape=marker_shape, size=marker_size,
                            showlegend=False, row=r, col=c
                        )
                fig = apply_publication_layout(fig, "Multi-Sample Subplot Grid")
                st.plotly_chart(fig, use_container_width=True)

        elif plot_layout_mode == "Individual Sample Carousel / Cards":
            for sample in selected_samples:
                st.markdown(f"#### Sample: {sample}")
                fig = go.Figure()
                s_df = analysis_df[analysis_df["Sample Group"] == sample]
                color = sample_color_map[sample]
                if len(s_df) > 0:
                    add_curve_with_sparse_markers(
                        fig, s_df[sr_col].values, s_df["Viscosity"].values,
                        name=sample, color=color, shape=marker_shape, size=marker_size
                    )
                fig = apply_publication_layout(fig, f"Analysis: {sample}")
                st.plotly_chart(fig, use_container_width=True)
