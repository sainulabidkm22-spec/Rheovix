"""
RheoVix — Launch Page
----------------------
A high-impact, immersive dark-themed landing page for the RheoVix rheology analysis suite.
Featuring a rich cosmic violet/midnight color grade, glowing glassmorphism surfaces,
and a crystal-clear vector logo integration.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Static SVG fragments & Vector Logo (Refined from logo_2.png)
# ---------------------------------------------------------------------------

def _rheovix_logo_svg(css_class: str = "rv-brand-logo") -> str:
    return f"""<svg viewBox="0 0 500 500" class="{css_class}" role="img" aria-label="RheoVix Brand Logo"><defs><linearGradient id="rvGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#38BDF8"/><stop offset="50%" stop-color="#7C3AED"/><stop offset="100%" stop-color="#C084FC"/></linearGradient><linearGradient id="rvPurpleGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#38BDF8"/><stop offset="50%" stop-color="#A78BFA"/><stop offset="100%" stop-color="#E879F9"/></linearGradient><filter id="rvShadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#38BDF8" flood-opacity="0.25"/></filter></defs><circle cx="250" cy="250" r="190" fill="none" stroke="url(#rvGrad)" stroke-width="12" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="80" filter="url(#rvShadow)"/><path d="M 220 110 L 315 110 C 355 110, 385 132, 385 172 C 385 208, 360 232, 325 240 L 395 325 L 340 325 L 280 248 L 220 248 L 220 325 L 170 325 L 170 110 Z M 220 148 L 220 210 L 310 210 C 332 210, 345 198, 345 179 C 345 160, 332 148, 310 148 Z" fill="#1E293B" opacity="0.95"/><path d="M 225 115 L 315 115 C 350 115, 378 136, 378 172 C 378 206, 352 228, 318 235 L 388 320 L 335 320 L 278 245 L 225 245 L 225 320 L 175 320 L 175 115 Z M 225 150 L 225 210 L 308 210 C 328 210, 340 198, 340 178 C 340 159, 328 150, 308 150 Z" fill="url(#rvPurpleGrad)" opacity="0.9"/><g transform="translate(130, 115)"><rect x="25" y="115" width="85" height="14" rx="4" fill="#38BDF8"/><ellipse cx="67" cy="115" rx="42" ry="7" fill="#0284C7"/><ellipse cx="67" cy="108" rx="35" ry="4.5" fill="#C084FC" opacity="0.6"/><ellipse cx="67" cy="108" rx="22" ry="2.5" fill="#38BDF8" opacity="0.8"/><rect x="63" y="50" width="8" height="60" rx="2" fill="#94A3B8"/><rect x="40" y="24" width="54" height="28" rx="4" fill="#0F172A"/><rect x="45" y="14" width="44" height="12" rx="3" fill="#334155"/><line x1="45" y1="20" x2="89" y2="20" stroke="#38BDF8" stroke-width="2.5"/></g><g><path d="M 310 235 L 410 235 M 410 120 L 410 235" fill="none" stroke="#475569" stroke-width="3" stroke-linecap="round"/><path d="M 240 250 C 280 240, 310 270, 350 250 C 370 238, 390 238, 410 235" fill="none" stroke="url(#rvPurpleGrad)" stroke-width="6" stroke-linecap="round"/><circle cx="310" cy="235" r="4.5" fill="#475569"/><circle cx="340" cy="220" r="5" fill="#38BDF8"/><circle cx="375" cy="175" r="6" fill="#A78BFA"/><circle cx="410" cy="120" r="7.5" fill="#E879F9"/><path d="M 310,235 C 330,225 355,195 375,175 C 388,162 400,135 410,120" fill="none" stroke="url(#rvPurpleGrad)" stroke-width="4.5" stroke-linecap="round"/></g></svg>"""


def _rheometer_svg() -> str:
    return """<svg viewBox="0 0 560 460" class="rv-hero-svg" role="img" aria-label="Animated parallel-plate rheometer diagram"><defs><linearGradient id="rvSampleGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#A78BFA" stop-opacity="0.25"/><stop offset="100%" stop-color="#38BDF8" stop-opacity="0.10"/></linearGradient></defs><g stroke="#2E2652" stroke-width="1.5"><line x1="60" y1="410" x2="520" y2="410"/><line x1="60" y1="410" x2="60" y2="80"/></g><rect x="90" y="300" width="380" height="18" rx="4" fill="#1E293B"/><rect x="94" y="176" width="372" height="124" fill="url(#rvSampleGrad)" stroke="#A78BFA" stroke-width="1.5"/><rect x="90" y="158" width="380" height="18" rx="4" fill="#38BDF8" class="rv-plate-top"/><g class="rv-flowlines" stroke-linecap="round" fill="none"><path d="M100,196 C 220,196 260,196 300,196" stroke="#38BDF8" stroke-width="3" opacity="0.85"/><path d="M100,220 C 210,220 270,220 320,220" stroke="#A78BFA" stroke-width="3" opacity="0.65"/><path d="M100,244 C 200,244 280,244 340,244" stroke="#C084FC" stroke-width="3" opacity="0.75"/><path d="M100,268 C 190,268 290,268 360,268" stroke="#E879F9" stroke-width="3" opacity="0.55"/><path d="M100,290 C 180,290 300,290 380,290" stroke="#38BDF8" stroke-width="3" opacity="0.4"/></g><g class="rv-label-shear"><text x="320" y="150" font-family="Space Grotesk" font-size="19" fill="#F8FAFC">shear rate&#160;</text><text x="422" y="150" font-family="Space Grotesk" font-size="19" font-style="italic" fill="#38BDF8">γ̇</text></g><g class="rv-label-stress"><text x="360" y="330" font-family="Space Grotesk" font-size="19" fill="#F8FAFC">shear stress&#160;</text><text x="140" y="360" font-family="Space Grotesk" font-size="19" font-style="italic" fill="#C084FC">τ</text></g><text x="185" y="400" font-family="Space Grotesk" font-size="16" fill="#94A3B8">η = τ / γ̇</text><g class="rv-particles" fill="#38BDF8"><circle cx="140" cy="188" r="3.5"/><circle cx="230" cy="210" r="3.5"/><circle cx="320" cy="232" r="3.5"/><circle cx="400" cy="254" r="3.5"/></g></svg>"""


def _flow_curve_svg(behavior: str) -> str:
    paths = {
        "Newtonian": "M30,45 L180,45",
        "Shear-thinning": "M30,20 C 70,22 100,45 180,82",
        "Shear-thickening": "M30,82 C 70,80 100,45 180,20",
    }
    d = paths.get(behavior, paths["Newtonian"])
    return f"""<svg viewBox="0 0 210 145" class="rv-mini-curve" role="img" aria-label="{behavior} viscosity curve">
    <line x1="30" y1="110" x2="195" y2="110" stroke="#2E2652" stroke-width="1.5"/>
    <line x1="30" y1="110" x2="30" y2="15" stroke="#2E2652" stroke-width="1.5"/>
    <path d="{d}" fill="none" stroke="#38BDF8" stroke-width="4" stroke-linecap="round"/>
    <text x="112" y="132" font-family="Inter" font-size="10" font-weight="600" fill="#94A3B8" text-anchor="middle">shear rate γ̇</text>
    <text x="-62" y="16" font-family="Inter" font-size="10" font-weight="600" fill="#94A3B8" transform="rotate(-90)" text-anchor="middle">viscosity η</text>
    </svg>"""


def _model_curve_svg(model: str) -> str:
    paths = {
        "Power Law": "M20,90 C 50,85 75,50 185,15",
        "Bingham": "M20,90 L65,90 C 95,75 140,35 185,15",
        "Herschel–Bulkley": "M20,90 L50,85 C 85,70 140,30 185,12",
    }
    d = paths.get(model, paths["Power Law"])
    return f"""<svg viewBox="0 0 200 120" class="rv-mini-curve" role="img" aria-label="{model} model curve"><line x1="20" y1="105" x2="192" y2="105" stroke="#2E2652" stroke-width="1.5"/><line x1="20" y1="105" x2="20" y2="12" stroke="#2E2652" stroke-width="1.5"/><path d="{d}" fill="none" stroke="#A78BFA" stroke-width="3.5" stroke-linecap="round" class="rv-draw-path"/></svg>"""


def _fit_demo_svg() -> str:
    pts = [(30, 92), (55, 78), (85, 58), (120, 40), (150, 26), (178, 16)]
    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="4.5" fill="#38BDF8" class="rv-fit-point" style="animation-delay:{0.15*i:.2f}s"/>'
        for i, (x, y) in enumerate(pts)
    )
    return f"""<svg viewBox="0 0 210 120" class="rv-fit-demo" role="img" aria-label="Illustrative data-to-model fitting animation"><line x1="22" y1="104" x2="200" y2="104" stroke="#2E2652" stroke-width="1.5"/><line x1="22" y1="104" x2="22" y2="8" stroke="#2E2652" stroke-width="1.5"/>{circles}<path d="M28,96 C 70,90 120,55 190,14" fill="none" stroke="#C084FC" stroke-width="3.5" stroke-linecap="round" class="rv-fit-curve"/></svg>"""


# ---------------------------------------------------------------------------
# Global CSS (High-Impact Dark Cosmic Grade)
# ---------------------------------------------------------------------------

def _inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        :root{
            --ink:#F8FAFC; 
            --ink-soft:#94A3B8; 
            --paper:#090616; 
            --surface:#130F26;
            --surface-hover:#1A1536;
            --line:#2A2250; 
            --accent:#A78BFA; 
            --accent-glow:#38BDF8;
            --accent-deep:#C084FC; 
            --accent-soft:rgba(167,139,250,0.12);
        }

        #MainMenu, footer, header{visibility:hidden;}
        [data-testid="stSidebar"]{display:none;}
        .block-container{padding-top:1.5rem; max-width:1180px;}
        .stApp{
            background: radial-gradient(circle at 15% 15%, #1F1247 0%, #090616 55%) !important;
            color: var(--ink) !important;
        }
        
        .stMarkdown p, .stMarkdown span, .stMarkdown label, div:not(.rv-cta-panel):not(.rv-cta-panel *) {
            font-family:'Inter',sans-serif !important; 
        }

        h1, h2, h3, h4, h5, h6, .rv-font-display{
            font-family:'Space Grotesk',sans-serif !important; 
            letter-spacing:-0.01em;
        }

        .rv-nav{
            display:flex; align-items:center; justify-content:space-between;
            padding:0.75rem 1.6rem; margin-bottom:2.6rem;
            background:rgba(19, 15, 38, 0.85); backdrop-filter:blur(16px);
            border:1px solid var(--line); border-radius:999px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);
        }
        .rv-nav-brand{display:flex; align-items:center; gap:0.6rem; font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.15rem; color:#F8FAFC !important;}
        .rv-brand-logo{width:32px; height:32px;}
        
        /* High-Impact Hero Logo Container with Glow */
        .rv-hero-logo-container {
            background: linear-gradient(135deg, rgba(31, 18, 71, 0.8) 0%, rgba(19, 15, 38, 0.9) 100%);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 24px;
            padding: 1.8rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 12px 40px rgba(124, 58, 237, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            margin-bottom: 1.8rem;
        }
        .rv-hero-logo {
            width: 120px;
            height: 120px;
            filter: drop-shadow(0 4px 12px rgba(56, 189, 248, 0.3));
        }

        .rv-nav-links a{color:var(--ink-soft) !important; text-decoration:none; font-size:0.92rem; font-weight:500; margin-left:1.6rem; transition:color .15s ease;}
        .rv-nav-links a:hover{color:var(--accent-glow) !important;}

        .rv-eyebrow{color:var(--accent-glow) !important; font-size:0.9rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.6rem;}
        .rv-hero-head{font-size:3.2rem; line-height:1.06; font-weight:700; color:#FFFFFF !important; margin:0 0 1.2rem 0;}
        .rv-hero-sub{font-size:1.1rem; color:var(--ink-soft) !important; max-width:34rem; line-height:1.6; margin-bottom:1.8rem;}
        .rv-trust{color:var(--ink-soft) !important; font-size:0.88rem; margin-top:1.2rem; font-weight:500;}
        
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #38BDF8 0%, #7C3AED 50%, #C084FC 100%) !important;
            border: none !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4) !important;
            transition: all 0.2s ease !important;
        }
        .stButton button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(56, 189, 248, 0.5) !important;
        }

        .rv-cta-secondary{
            display:inline-block; padding:0.65rem 1.4rem; border:1px solid var(--line);
            border-radius:12px; background:var(--surface); color:#F8FAFC !important; text-decoration:none; font-weight:600; font-size:0.95rem;
            box-shadow:0 4px 12px rgba(0,0,0,0.2);
            transition:all .15s ease;
        }
        .rv-cta-secondary:hover{border-color:var(--accent); background:var(--surface-hover); color: var(--accent-glow) !important; transform:translateY(-1px);}

        .rv-hero-svg{width:100%; height:auto;}
        .rv-plate-top{animation:rvShear 3.2s ease-in-out infinite;}
        @keyframes rvShear{
            0%,100%{transform:translateX(0);}
            50%{transform:translateX(34px);}
        }
        .rv-flowlines path{stroke-dasharray:10 8; animation:rvFlow 1.6s linear infinite;}
        .rv-flowlines path:nth-child(2){animation-duration:1.9s;}
        .rv-flowlines path:nth-child(3){animation-duration:1.4s;}
        .rv-flowlines path:nth-child(4){animation-duration:2.1s;}
        .rv-flowlines path:nth-child(5){animation-duration:2.6s;}
        @keyframes rvFlow{ to { stroke-dashoffset:-36; } }
        .rv-particles circle{animation:rvRise 3.2s ease-in-out infinite;}
        .rv-particles circle:nth-child(2){animation-delay:.5s;}
        .rv-particles circle:nth-child(3){animation-delay:1s;}
        .rv-particles circle:nth-child(4){animation-delay:1.5s;}
        @keyframes rvRise{
            0%{opacity:0; transform:translateY(0);}
            30%{opacity:1;}
            100%{opacity:0; transform:translateY(-70px);}
        }

        .rv-explore-caption{
            font-family:'Space Grotesk',sans-serif; font-size:0.98rem; font-weight:600; color:var(--accent-glow) !important;
            margin-top:0.6rem;
        }

        .rv-section{margin:5.5rem 0 2.5rem 0;}
        .rv-kicker{color:var(--accent-glow) !important; font-weight:700; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.4rem;}
        .rv-section-title{font-size:2.2rem; font-weight:700; color:#FFFFFF !important; margin:0 0 0.6rem 0;}
        .rv-section-sub{color:var(--ink-soft) !important; max-width:38rem; line-height:1.6; margin-bottom:2.2rem; font-size:1.02rem;}

        .rv-journey{display:flex; gap:0; border:1px solid var(--line); background:var(--surface); border-radius:16px; box-shadow:0 8px 30px rgba(0,0,0,0.3); overflow:hidden;}
        .rv-step{
            flex:1; padding:1.8rem 1.2rem 1.4rem 1.2rem; border-right:1px solid var(--line);
            transition:background .2s ease;
        }
        .rv-step:last-child{border-right:none;}
        .rv-step:hover{background:var(--surface-hover);}
        .rv-step-num{font-family:'Space Grotesk',sans-serif; font-weight:700; color:var(--accent-glow) !important; font-size:0.95rem;}
        .rv-step-title{font-family:'Space Grotesk',sans-serif; font-weight:700; color:#FFFFFF !important; font-size:1.08rem; margin:0.35rem 0 0.4rem 0;}
        .rv-step-desc{color:var(--ink-soft) !important; font-size:0.9rem; line-height:1.5;}

        .rv-card{
            background:var(--surface); border:1px solid var(--line); border-radius:16px;
            padding:1.8rem; height:100%; box-shadow:0 8px 30px rgba(0,0,0,0.25);
            display: flex; flex-direction: column; justify-content: space-between;
            transition:border-color .2s ease, transform .2s ease, box-shadow .2s ease;
        }
        .rv-card:hover{border-color:var(--accent); transform:translateY(-3px); box-shadow:0 12px 36px rgba(124,58,237,0.3);}
        .rv-card-title{font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.15rem; color:#FFFFFF !important; margin-bottom:0.3rem;}
        .rv-card-eq{font-family:'Space Grotesk',sans-serif; font-size:0.95rem; font-weight:600; color:var(--accent-glow) !important; margin:0.5rem 0;}
        .rv-card-desc{color:var(--ink-soft) !important; font-size:0.92rem; line-height:1.55; margin-bottom:0.8rem;}
        .rv-card-use{color:var(--ink-soft) !important; font-size:0.82rem; font-weight:500; border-top:1px solid var(--line); padding-top:0.6rem; margin-top:0.6rem;}
        .rv-mini-curve{width:100%; height:auto; margin:0.6rem 0;}

        .rv-fit-demo{width:100%; max-width:260px; height:auto;}
        .rv-fit-point{opacity:0; animation:rvPointIn 4.5s ease-in-out infinite;}
        @keyframes rvPointIn{
            0%{opacity:0;} 8%{opacity:1;} 70%{opacity:1;} 85%{opacity:0;} 100%{opacity:0;}
        }
        .rv-fit-curve{
            stroke-dasharray:230; stroke-dashoffset:230;
            animation:rvDraw 4.5s ease-in-out infinite;
        }
        @keyframes rvDraw{
            0%{stroke-dashoffset:230;} 55%{stroke-dashoffset:230;}
            85%{stroke-dashoffset:0;} 100%{stroke-dashoffset:0;}
        }
        .rv-illustrative{color:var(--ink-soft) !important; font-size:0.82rem; font-style:italic; margin-top:1rem; padding-top:0.5rem; border-top:1px dashed var(--line); text-align:center;}
        .rv-insight-chip{
            display:inline-block; background:rgba(56,189,248,0.1); color:var(--accent-glow) !important;
            border-radius:8px; padding:0.4rem 0.9rem; font-family:'Space Grotesk',sans-serif;
            font-size:0.88rem; font-weight:700; margin-top:0.8rem; border:1px solid rgba(56,189,248,0.3);
        }

        .rv-pipeline{border-left:2px solid var(--accent); margin-left:0.5rem; padding-left:1.5rem;}
        .rv-pipeline-item{position:relative; padding:0.6rem 0; color:#E2E8F0 !important; font-size:0.98rem;}
        .rv-pipeline-item::before{
            content:''; position:absolute; left:-1.61rem; top:0.95rem; width:10px; height:10px;
            border-radius:50%; background:var(--accent-glow); border:2px solid #130F26;
        }
        .rv-pipeline-item b{color:#FFFFFF !important; font-weight:600;}

        .rv-benefit-title{font-family:'Space Grotesk',sans-serif; font-weight:700; color:#FFFFFF !important; font-size:1.05rem; margin-bottom:0.4rem;}
        .rv-benefit-desc{color:var(--ink-soft) !important; font-size:0.9rem; line-height:1.55;}

        .rv-cta-panel{
            background:linear-gradient(135deg, #1E1247 0%, #2E1065 50%, #0F172A 100%); color:#F8FAFC !important; border-radius:20px; padding:3.5rem 3rem;
            box-shadow:0 16px 40px rgba(0,0,0,0.5); border:1px solid rgba(167,139,250,0.3);
        }
        .rv-cta-panel h2{color:#FFFFFF !important;}
        .rv-cta-panel p{color:#CBD5E1 !important;}

        .rv-footer{border-top:1px solid var(--line); margin-top:5rem; padding-top:2rem; color:var(--ink-soft) !important; font-size:0.88rem;}
        .rv-footer a{color:var(--ink-soft) !important; text-decoration:none; margin-right:1.5rem; font-weight:500;}
        .rv-footer a:hover{color:var(--accent-glow) !important;}

        @media (prefers-reduced-motion: reduce){
            .rv-plate-top, .rv-flowlines path, .rv-particles circle,
            .rv-fit-point, .rv-fit-curve{animation:none !important;}
        }

        .stRadio > label, .stSelectSlider > label{font-family:'Space Grotesk',sans-serif; font-weight:600; color:#FFFFFF !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def _render_nav():
    html = (
        '<div class="rv-nav">'
        f'<div class="rv-nav-brand">{_rheovix_logo_svg("rv-brand-logo")} <span>RheoVix Studio</span></div>'
        '<div class="rv-nav-links">'
        '<a href="#introduction">Introduction</a>'
        '<a href="#how-it-works">How It Works</a>'
        '<a href="#models">Models</a>'
        '<a href="#launch">Analysis</a>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def _render_hero():
    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown(
            f'<div class="rv-hero-logo-container">{_rheovix_logo_svg("rv-hero-logo")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="rv-eyebrow">Advanced Rheology Suite</div>
            <div class="rv-hero-head">Understand the flow.<br/>Model the behavior.</div>
            <div class="rv-hero-sub">
                RheoVix Studio helps researchers and students transform raw flow-curve
                measurements into interpretable rheological models, parameters, and
                publication-ready insights.
            </div>
            """,
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns([1, 1.1])
        with b1:
            if st.button("Launch Analysis →", type="primary", use_container_width=True):
                st.session_state["view"] = "app"
                st.rerun()
        with b2:
            st.markdown(
                '<a class="rv-cta-secondary" href="#introduction">Explore Rheology ↓</a>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="rv-trust">Built for researchers and students in rheology, '
            'materials science, food science, polymers, and related fields.</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(_rheometer_svg(), unsafe_allow_html=True)

        shear_state = st.select_slider(
            "Explore the flow — shear rate",
            options=["Low", "Moderate", "High"],
            value="Moderate",
            label_visibility="visible",
            key="hero_shear_slider",
        )
        captions = {
            "Low": "Low shear rate — the sample deforms gently between the plates.",
            "Moderate": "Flow response — streamlines move at a steady, measurable rate.",
            "High": "High shear — many structured fluids show shear-thinning here.",
        }
        st.markdown(
            f'<div class="rv-explore-caption">{captions[shear_state]}</div>',
            unsafe_allow_html=True,
        )


def _render_journey():
    st.markdown('<div id="how-it-works" class="rv-section"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rv-kicker">Workflow</div>
        <div class="rv-section-title">From measurement to meaning</div>
        <div class="rv-section-sub">A simple workflow for turning rheological measurements into interpretable models.</div>
        """,
        unsafe_allow_html=True,
    )

    steps = [
        ("01", "Prepare", "Bring your experimental flow-curve data — CSV, XLSX, or XLS exports from your rheometer."),
        ("02", "Measure", "Capture shear rate, shear stress, and viscosity behavior across replicates."),
        ("03", "Model", "Fit Power Law, Bingham, and Herschel–Bulkley equations to your data."),
        ("04", "Compare", "Evaluate adjusted R², RMSE, and fitted parameters across models and samples."),
        ("05", "Understand", "Identify flow behavior and export publication-ready figures and tables."),
    ]
    
    html = '<div class="rv-journey">'
    for num, title, desc in steps:
        html += (
            f'<div class="rv-step">'
            f'<div class="rv-step-num">{num}</div>'
            f'<div class="rv-step-title">{title}</div>'
            f'<div class="rv-step-desc">{desc}</div>'
            f'</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_introduction():
    st.markdown('<div id="introduction" class="rv-section"></div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="rv-kicker">Introduction to Rheology</div>
            <div class="rv-section-title">Matter, in motion</div>
            <div class="rv-section-sub" style="margin-bottom:1.2rem;">
                Every fluid responds to shear differently. Toggle between the three
                classic flow behaviors below to see how viscosity relates to shear rate
                in each case — the same relationship RheoVix fits to your own data.
            </div>
            """,
            unsafe_allow_html=True,
        )
        behavior = st.radio(
            "Flow behavior",
            ["Newtonian", "Shear-thinning", "Shear-thickening"],
            horizontal=True,
            label_visibility="collapsed",
            key="flow_behavior_radio",
        )
        descriptions = {
            "Newtonian": "Viscosity stays constant regardless of shear rate — think water or dilute oils.",
            "Shear-thinning": "Viscosity decreases as shear rate increases — common in polymer solutions, paints, and many food products.",
            "Shear-thickening": "Viscosity increases as shear rate increases — seen in dense suspensions such as cornstarch mixtures.",
        }
        st.markdown(
            f'<div style="color:var(--ink-soft); font-size:0.95rem; font-weight:500; margin-top:1rem; line-height:1.6;">{descriptions[behavior]}</div>',
            unsafe_allow_html=True,
        )

    with right:
        card_html = (
            f'<div class="rv-card">'
            f'<div>{_flow_curve_svg(behavior)}</div>'
            f'<div class="rv-illustrative">Illustrative relationship, not measured data.</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)


def _render_fit_demo():
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown(
            """
            <div class="rv-kicker">Data → Model</div>
            <div class="rv-section-title" style="font-size:1.7rem;">Experimental points become a fitted curve</div>
            <div class="rv-section-sub" style="margin-bottom:0.6rem;">
                RheoVix fits established rheological models to your measured points and
                reports how well each one explains the observed behavior.
            </div>
            <div class="rv-illustrative" style="text-align:left; border:none; padding:0; margin-top:0.4rem;">Values shown are illustrative demo values, not real results.</div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        card_html = (
            f'<div class="rv-card" style="text-align:center;">'
            f'<div>{_fit_demo_svg()}</div>'
            f'<div class="rv-insight-chip">Power Law · R² = 0.982 (illustrative)</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)


def _render_models():
    st.markdown('<div id="models" class="rv-section"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rv-kicker">Model Intelligence</div>
        <div class="rv-section-title">Choose the model that explains the flow</div>
        <div class="rv-section-sub">
            RheoVix fits the models below to your experimental data and compares them so
            you can judge which mathematical description best represents your material.
        </div>
        """,
        unsafe_allow_html=True,
    )

    models = [
        ("Power Law", "τ = K γ̇ⁿ",
         "Captures shear-dependent viscosity with a single exponent — the standard starting point for shear-thinning or shear-thickening fluids.",
         "Typical use: polymer melts, solutions, many suspensions."),
        ("Bingham", "τ = τ₀ + η_p γ̇",
         "Describes materials with a yield stress that flow linearly once that stress is exceeded.",
         "Typical use: pastes, drilling muds, some gels."),
        ("Herschel–Bulkley", "τ = τ₀ + K γ̇ⁿ",
         "Combines a yield stress with power-law shear-dependence for materials that both yield and shear-thin or thicken.",
         "Typical use: food products, cosmetics, structured suspensions."),
    ]

    cols = st.columns(3, gap="medium")
    for col, (name, eq, desc, use) in zip(cols, models):
        with col:
            card_html = (
                f'<div class="rv-card">'
                f'<div>'
                f'<div class="rv-card-title">{name}</div>'
                f'<div class="rv-card-eq">{eq}</div>'
                f'<div class="rv-card-desc">{desc}</div>'
                f'{_model_curve_svg(name)}'
                f'</div>'
                f'<div class="rv-card-use">{use}</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


def _render_launch_cta():
    st.markdown('<div id="launch" class="rv-section"></div>', unsafe_allow_html=True)
    
    cta_html = (
        '<div class="rv-cta-panel">'
        '<div style="display: flex; gap: 2rem; align-items: center; flex-wrap: wrap;">'
        '<div style="flex: 1.1; min-width: 280px;">'
        '<h2 style="font-size: 2rem; margin-top: 0; color: #FFFFFF !important;">Your data. Your rheology. One workspace.</h2>'
        '<p style="max-width: 32rem; line-height: 1.6; font-size: 1.02rem; color: #CBD5E1 !important;">'
        'Upload your experimental flow-curve data and move from raw measurements '
        'to model-based rheological insight.'
        '</p>'
        '</div>'
        '<div style="flex: 1; min-width: 280px;">'
        '<div class="rv-pipeline">'
        '<div class="rv-pipeline-item"><b>CSV · XLSX · XLS</b> — raw rheometer export</div>'
        '<div class="rv-pipeline-item"><b>Automatic organization</b> — sheets and sample groups</div>'
        '<div class="rv-pipeline-item"><b>Replicate handling</b> — grouped by sample</div>'
        '<div class="rv-pipeline-item"><b>Model fitting</b> — Power Law, Bingham, Herschel–Bulkley</div>'
        '<div class="rv-pipeline-item"><b>Statistical evaluation</b> — adjusted R², RMSE</div>'
        '<div class="rv-pipeline-item"><b>Publication-ready visualization</b> — export PNG, HTML, XLSX</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(cta_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Launch RheoVix Studio →", type="primary", key="launch_cta_main"):
        st.session_state["view"] = "app"
        st.rerun()


def _render_benefits():
    st.markdown('<div class="rv-section"></div>', unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    tiles = [
        ("Built for researchers", "Designed around real experimental workflows, from raw export to fitted parameters."),
        ("Built for students", "Learn rheological modeling by exploring real flow-curve behavior, not just formulas."),
        ("Reproducible", "Keep every analysis structured, model-based, and easy to retrace."),
        ("Clear", "Turn complex flow behavior into results you can explain and defend."),
    ]
    for col, (title, desc) in zip(cols, tiles):
        with col:
            card_html = (
                f'<div class="rv-card">'
                f'<div>'
                f'<div class="rv-benefit-title">{title}</div>'
                f'<div class="rv-benefit-desc">{desc}</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


def _render_final_cta():
    st.markdown('<div class="rv-section" style="text-align:left;">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rv-section-title">Ready to understand your flow?</div>
        <div class="rv-section-sub">
            Bring your experimental data. RheoVix will help you explore the behavior behind the curve.
        </div>
        """,
        unsafe_allow_html=True,
    )
    b1, b2 = st.columns([1, 1.2])
    with b1:
        if st.button("Launch RheoVix Studio →", type="primary", key="final_cta_btn"):
            st.session_state["view"] = "app"
            st.rerun()
    with b2:
        st.markdown('<a class="rv-cta-secondary" href="#introduction">Explore Rheology</a>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_footer():
    footer_html = (
        '<div class="rv-footer">'
        '<div style="display:flex; align-items:center; gap:0.6rem; font-family:\'Space Grotesk\',sans-serif; font-weight:700; color:#FFFFFF; margin-bottom:0.3rem;">'
        f'{_rheovix_logo_svg("rv-brand-logo")} RheoVix Studio'
        '</div>'
        '<div style="margin-bottom:0.8rem;">Scientific rheology analysis for researchers and students.</div>'
        '<a href="#introduction">Introduction</a>'
        '<a href="#launch">Analysis</a>'
        '<a href="#models">Models</a>'
        '</div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)


def render_landing_page():
    _inject_css()
    _render_nav()
    _render_hero()
    _render_journey()
    _render_introduction()
    _render_fit_demo()
    _render_models()
    _render_launch_cta()
    _render_benefits()
    _render_final_cta()
    _render_footer()