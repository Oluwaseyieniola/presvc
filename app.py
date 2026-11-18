import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

st.set_page_config(
    page_title="Farm-to-Fork Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Demo data: illustrative only ----------
FARMS = [
    {"id": "FARM-UAE-001", "name": "Al Ain Greenhouse Collective", "location": "Al Ain, Abu Dhabi", "type": "Greenhouse", "area": 12.5, "water": "Recycled + groundwater", "status": "Active"},
    {"id": "FARM-UAE-002", "name": "Desert Bloom Farms", "location": "Al Wathba, Abu Dhabi", "type": "Hydroponic", "area": 4.2, "water": "Recycled water", "status": "Active"},
    {"id": "FARM-UAE-003", "name": "Oasis Date Palm Estate", "location": "Al Dhafra, Abu Dhabi", "type": "Orchard", "area": 28.0, "water": "Groundwater", "status": "Onboarding"},
]
LOTS = [
    {"lot_id": "LOT-UAE-00081", "food": "Spinach", "variety": "Savoy", "farm": "Al Ain Greenhouse Collective", "crop_cycle": "CYCLE-008", "harvest_date": "2026-11-17", "quantity": 500, "unit": "kg", "safety": "Passed", "composition": "Measured + reference", "custody": "Distributor"},
    {"lot_id": "LOT-UAE-00082", "food": "Cherry tomato", "variety": "Sweet 100", "farm": "Desert Bloom Farms", "crop_cycle": "CYCLE-014", "harvest_date": "2026-11-18", "quantity": 240, "unit": "kg", "safety": "Pending", "composition": "Reference only", "custody": "Farm"},
    {"lot_id": "LOT-UAE-00083", "food": "Cucumber", "variety": "Beit Alpha", "farm": "Al Ain Greenhouse Collective", "crop_cycle": "CYCLE-009", "harvest_date": "2026-11-16", "quantity": 320, "unit": "kg", "safety": "On hold", "composition": "Not assessed", "custody": "Processor"},
]
READINGS = pd.DataFrame([
    ["2026-11-18 08:00", "Air temperature", 31.2, "°C"],
    ["2026-11-18 09:00", "Air temperature", 32.4, "°C"],
    ["2026-11-18 10:00", "Air temperature", 34.1, "°C"],
    ["2026-11-18 08:00", "Relative humidity", 61, "%"],
    ["2026-11-18 09:00", "Relative humidity", 58, "%"],
    ["2026-11-18 10:00", "Relative humidity", 55, "%"],
], columns=["Time", "Metric", "Value", "Unit"])

if "lots" not in st.session_state:
    st.session_state.lots = [x.copy() for x in LOTS]
if "farm_notes" not in st.session_state:
    st.session_state.farm_notes = {}

# ---------- Styling ----------
st.markdown("""
<style>
    .block-container {padding-top: 1.3rem; padding-bottom: 2rem; max-width: 1500px;}
    [data-testid="stMetric"] {background: #f7faf8; border: 1px solid #e3ebe5; padding: 14px 16px; border-radius: 12px;}
    .hero {padding: 22px 24px; border-radius: 16px; background: linear-gradient(120deg,#123d32,#1d6650); color: white; margin-bottom: 18px;}
    .hero h1 {font-size: 2rem; margin: 0 0 5px 0;}
    .hero p {margin: 0; color: #d9eee3;}
    .small-muted {color: #64748b; font-size: .86rem;}
    .section-note {background:#f6f8f7; border-left:4px solid #39866a; padding:12px 14px; border-radius:6px;}
    div[data-testid="stTabs"] button {font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌱 Farm-to-Fork")
    st.caption("Integrated Food Intelligence Platform")
    page = st.radio(
        "Workspace",
        ["Executive overview", "Agricultural intelligence", "Harvest & traceability",
         "Food safety & quality", "Food composition", "Personal nutrition", "System blueprint"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("**Environment**")
    st.info("Demonstration workspace\n\nSample records only. No live farm, laboratory, wearable or regulatory integrations are connected.")
    st.caption("Prototype • Architecture exploration")

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <h1>Farm-to-Fork Intelligence</h1>
  <p>One connected record from agricultural production to food quality, traceability and personal nutrition.</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Workspace date: {date.today().strftime('%d %B %Y')}  ·  Data mode: illustrative demonstration")

# ---------- Helpers ----------
def status_badge(value):
    colors = {"Passed": "🟢", "Pending": "🟠", "On hold": "🔴", "Failed": "🔴", "Released": "🟢"}
    return f"{colors.get(value, '⚪')} {value}"

def lot_df():
    return pd.DataFrame(st.session_state.lots)

# ---------- Executive overview ----------
if page == "Executive overview":
    st.subheader("Platform overview")
    st.markdown("A shared intelligence layer connects farm operations, food evidence, supply-chain events and individual nutrition.")
    lots = lot_df()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Connected farms", len(FARMS), "2 active")
    c2.metric("Traceable food lots", len(lots), "Demo records")
    c3.metric("Safety passed", int((lots["safety"] == "Passed").sum()), "of 3 lots")
    c4.metric("Lots requiring attention", int(lots["safety"].isin(["Pending", "On hold", "Failed"]).sum()), "Pending / hold")

    st.markdown("### End-to-end intelligence flow")
    stages = [
        ("01", "Agriculture", "Farm, plot, crop cycle, water, soil, inputs and harvest"),
        ("02", "Food safety & quality", "Samples, laboratory evidence, assessments and release decisions"),
        ("03", "Food composition", "Reference, measured and model-estimated nutrient profiles"),
        ("04", "Supply chain", "Processing, packaging, shipment, custody and retail"),
        ("05", "Personal nutrition", "Food intake, portions, dietary profile and wearable context"),
        ("06", "Outcomes", "Farm performance, nutrition progress and sustainability"),
    ]
    cols = st.columns(3)
    for i, (num, title, desc) in enumerate(stages):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border:1px solid #e2e8e4;border-radius:12px;padding:16px;margin-bottom:12px;min-height:135px">
              <div style="color:#39866a;font-weight:700;font-size:13px">{num}</div>
              <div style="font-weight:700;font-size:17px;margin:5px 0">{title}</div>
              <div style="color:#64748b;font-size:13px">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("### Current traceability register")
    view = lots[["lot_id", "food", "farm", "harvest_date", "quantity", "unit", "safety", "custody"]].copy()
    view["safety"] = view["safety"].apply(status_badge)
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.markdown('<div class="section-note"><b>Design rule:</b> the harvest lot is the bridge between agricultural production and every downstream food, safety, supply-chain and nutrition record.</div>', unsafe_allow_html=True)

# ---------- Agricultural intelligence ----------
elif page == "Agricultural intelligence":
    st.subheader("Agricultural intelligence")
    st.write("Operational view of farms, production units, crop cycles, farm observations and resource performance.")
    farm_names = [f["name"] for f in FARMS]
    selected = st.selectbox("Select farm", farm_names)
    farm = next(f for f in FARMS if f["name"] == selected)
    a, b, c, d = st.columns(4)
    a.metric("Farm area", f'{farm["area"]} ha')
    b.metric("Production system", farm["type"])
    c.metric("Water source", farm["water"])
    d.metric("Operational status", farm["status"])
    st.markdown("### Farm profile")
    st.write(f'**Farm ID:** {farm["id"]}  ·  **Location:** {farm["location"]}')
    st.markdown("### Example environmental observations")
    st.dataframe(READINGS, use_container_width=True, hide_index=True)
    chart = px.line(READINGS[READINGS["Metric"] == "Air temperature"], x="Time", y="Value",
                    markers=True, title="Greenhouse air temperature (illustrative)")
    st.plotly_chart(chart, use_container_width=True)
    st.markdown("### Record a farm observation")
    with st.form("observation_form"):
        x, y, z = st.columns(3)
        metric = x.selectbox("Metric", ["Soil moisture", "Air temperature", "Relative humidity", "Water EC", "Soil pH"])
        value = y.number_input("Observed value", value=25.0)
        unit = z.selectbox("Unit", ["%", "°C", "mS/cm", "pH", "mg/L"])
        observed = st.date_input("Observation date", value=date.today())
        source = st.selectbox("Source", ["Manual entry", "Sensor", "Laboratory"])
        submitted = st.form_submit_button("Save demonstration observation", type="primary")
        if submitted:
            st.success(f"Captured {metric}: {value} {unit} on {observed} from {source}. This is held in the demo session only.")

# ---------- Harvest and traceability ----------
elif page == "Harvest & traceability":
    st.subheader("Harvest and traceability")
    st.write("Create harvest lots, inspect their origin and follow transformations through the supply chain.")
    lots = lot_df()
    selected_lot_id = st.selectbox("Choose a food lot", lots["lot_id"].tolist())
    lot = next(x for x in st.session_state.lots if x["lot_id"] == selected_lot_id)
    left, right = st.columns([1, 1])
    with left:
        st.markdown("### Lot identity")
        st.markdown(f"**{lot['food']} — {lot['variety']}**")
        st.code(lot["lot_id"])
        st.write(f"Origin farm: **{lot['farm']}**")
        st.write(f"Crop cycle: **{lot['crop_cycle']}**")
        st.write(f"Harvest date: **{lot['harvest_date']}**")
        st.write(f"Quantity: **{lot['quantity']} {lot['unit']}**")
    with right:
        st.markdown("### Current state")
        st.metric("Safety assessment", lot["safety"])
        st.metric("Current custodian", lot["custody"])
        st.metric("Composition evidence", lot["composition"])
    st.markdown("### Lot lineage")
    lineage = pd.DataFrame([
        ["Farm", lot["farm"], "Origin"],
        ["Production cycle", lot["crop_cycle"], "Growing history"],
        ["Harvest event", "HARVEST-" + lot["lot_id"][-3:], lot["harvest_date"]],
        ["Food lot", lot["lot_id"], f'{lot["quantity"]} {lot["unit"]}'],
        ["Current custodian", lot["custody"], "Latest recorded stage"],
    ], columns=["Stage", "Record", "Details"])
    st.dataframe(lineage, use_container_width=True, hide_index=True)
    st.markdown("### Register a new harvest lot")
    with st.form("new_lot"):
        x, y = st.columns(2)
        food = x.text_input("Food name", "Romaine lettuce")
        variety = y.text_input("Variety", "Green Towers")
        x, y, z = st.columns(3)
        farm_name = x.selectbox("Origin farm", farm_names if (farm_names := [f["name"] for f in FARMS]) else [])
        qty = y.number_input("Harvest quantity (kg)", min_value=0.1, value=100.0)
        harvest_date = z.date_input("Harvest date", value=date.today())
        cycle = st.text_input("Crop cycle ID", "CYCLE-NEW-001")
        create = st.form_submit_button("Create demo lot", type="primary")
        if create:
            new_id = f"LOT-DEMO-{len(st.session_state.lots)+1:04d}"
            st.session_state.lots.append({
                "lot_id": new_id, "food": food, "variety": variety, "farm": farm_name,
                "crop_cycle": cycle, "harvest_date": str(harvest_date), "quantity": qty,
                "unit": "kg", "safety": "Pending", "composition": "Not assessed", "custody": "Farm"
            })
            st.success(f"Created {new_id}. Safety status is Pending until required evidence is assessed.")
            st.rerun()

# ---------- Safety and quality ----------
elif page == "Food safety & quality":
    st.subheader("Food safety and quality")
    st.markdown('<div class="section-note"><b>Safety is a release gate, not a farm score.</b> Missing evidence must remain pending; it must never be treated as a pass.</div>', unsafe_allow_html=True)
    lots = lot_df()
    selected = st.selectbox("Select lot for assessment", lots["lot_id"].tolist())
    lot = next(x for x in st.session_state.lots if x["lot_id"] == selected)
    st.markdown(f"### {lot['food']} · {lot['lot_id']}")
    st.write(f"Current assessment: **{status_badge(lot['safety'])}**")
    st.markdown("### Example evidence checklist")
    checks = [
        ("Pesticide residue result", "Pending"),
        ("Microbiological result", "Pending"),
        ("Water-quality evidence", "Available"),
        ("Input application / pre-harvest interval review", "Available"),
        ("Storage and handling record", "Pending"),
    ]
    for label, state in checks:
        st.write(f"{'📄' if state == 'Available' else '⏳'} **{label}** — {state}")
    st.caption("These are illustrative checklist entries, not verified results for the selected lot.")
    st.markdown("### Record an assessment decision (demo only)")
    decision = st.selectbox("Assessment status", ["Pending", "Passed", "On hold", "Failed"])
    rationale = st.text_area("Evidence summary / rationale", placeholder="Describe the evidence and applicable requirement.")
    if st.button("Update demo assessment", type="primary"):
        for item in st.session_state.lots:
            if item["lot_id"] == selected:
                item["safety"] = decision
        st.success("Demo status updated for this session. A production system would require evidence references, rule version, assessor identity and an authorised release workflow.")
    st.markdown("### Assessment design")
    st.write("A production assessment should record the standard and version, applicable requirements, laboratory result references, units, method, detection limits, evidence completeness, assessor and decision history.")

# ---------- Food composition ----------
elif page == "Food composition":
    st.subheader("Food composition intelligence")
    st.write("Keep reference values, laboratory measurements and model estimates visibly distinct.")
    lots = lot_df()
    selected = st.selectbox("Select food lot", lots["lot_id"].tolist(), key="composition_lot")
    lot = next(x for x in st.session_state.lots if x["lot_id"] == selected)
    st.markdown(f"### {lot['food']} · {selected}")
    st.info(f"Current evidence classification: {lot['composition']}")
    nutrients = pd.DataFrame([
        ["Energy", 23, "kcal", "Reference"],
        ["Protein", 2.9, "g", "Reference"],
        ["Carbohydrate", 3.6, "g", "Reference"],
        ["Fibre", 2.2, "g", "Reference"],
        ["Vitamin C", 28.1, "mg", "Reference"],
        ["Iron", 2.7, "mg", "Reference"],
    ], columns=["Nutrient", "Value", "Unit", "Evidence type"])
    st.caption("Illustrative spinach reference values per 100 g raw edible portion. Not measured for the selected lot.")
    st.dataframe(nutrients, use_container_width=True, hide_index=True)
    st.markdown("### Evidence types")
    x, y, z = st.columns(3)
    x.metric("Reference", "Food tables", "General food identity")
    y.metric("Measured", "Laboratory", "Specific sample / batch")
    z.metric("Estimated", "Validated model", "Prediction + uncertainty")
    st.warning("Do not attribute generic reference values to a specific harvest lot as though they were batch-tested results.")

# ---------- Personal nutrition ----------
elif page == "Personal nutrition":
    st.subheader("Personal nutrition intelligence")
    st.write("Connect food identity and composition evidence to portion size, dietary profile and personal goals.")
    x, y = st.columns(2)
    with x:
        st.markdown("### Example consumer profile")
        age = st.number_input("Age", min_value=1, max_value=110, value=32)
        goal = st.selectbox("Primary goal", ["Balanced nutrition", "Increase fibre intake", "Support active lifestyle", "Manage sodium intake"])
        dietary = st.selectbox("Dietary pattern", ["No declared restriction", "Vegetarian", "Vegan", "Other"])
    with y:
        st.markdown("### Food intake")
        food = st.selectbox("Food", ["Spinach", "Cherry tomato", "Cucumber", "Beans"])
        portion = st.number_input("Portion (g)", min_value=1, max_value=2000, value=100)
        basis = st.selectbox("Composition basis", ["Reference values", "Laboratory measured", "Model estimated"])
    if st.button("Generate illustrative nutrition view", type="primary"):
        st.markdown("### Intake summary")
        st.metric("Recorded portion", f"{portion} g")
        st.write(f"Food: **{food}** · Goal: **{goal}** · Dietary profile: **{dietary}**")
        st.write(f"Composition basis: **{basis}**")
        st.info("This prototype demonstrates the workflow only. It does not calculate personalised clinical requirements or infer absorption, metabolism or health outcomes.")
    st.markdown("### Wearable context")
    st.write("A future integration may display activity, sleep and heart-rate trends with source, timestamp and measurement quality. These signals provide context; they do not directly measure nutrient absorption.")

# ---------- System blueprint ----------
elif page == "System blueprint":
    st.subheader("System blueprint")
    st.write("Logical architecture and initial implementation boundaries.")
    st.markdown("### Domain modules")
    modules = pd.DataFrame([
        ["Identity & tenancy", "Organisations, users, memberships, farms and permissions", "Foundation"],
        ["Agricultural intelligence", "Production units, crop cycles, observations, inputs and irrigation", "Milestone 1"],
        ["Harvest & food identity", "Harvest events, lots, samples and lot lineage", "Milestone 1"],
        ["Safety & quality", "Standards, requirements, lab results, assessments and release decisions", "Milestone 2"],
        ["Food composition", "Nutrient definitions, reference profiles and measured results", "Milestone 2"],
        ["Supply chain", "Processing, packaging, shipments and custody", "Milestone 3"],
        ["Personal nutrition", "Profiles, intake, portions, goals and assessments", "Milestone 3"],
        ["Wearable integration", "Devices, consent and observations", "Milestone 3"],
        ["Outcomes & sustainability", "Farm, nutrition and environmental outcomes", "Later expansion"],
    ], columns=["Domain", "Responsibilities", "Delivery"])
    st.dataframe(modules, use_container_width=True, hide_index=True)
    st.markdown("### Recommended technical foundation")
    stack = pd.DataFrame([
        ["Frontend", "Streamlit prototype; later React/Next.js + Flutter"],
        ["Backend", "Go modular monolith with versioned REST APIs"],
        ["Database", "PostgreSQL + PostGIS"],
        ["Time series", "PostgreSQL initially; TimescaleDB if justified"],
        ["IoT", "MQTT + HTTP ingestion"],
        ["Files", "S3-compatible object storage"],
        ["Analytics", "Python services and analytical pipelines"],
        ["Events", "Transactional outbox; broker as scale requires"],
    ], columns=["Layer", "Technology direction"])
    st.dataframe(stack, use_container_width=True, hide_index=True)
    st.markdown("### Core build sequence")
    st.code("Identity → Farm & Production → Harvest & Lots → Safety & Quality → Composition → Traceability → Personal Nutrition → Outcomes", language="text")
    st.caption("This Streamlit app is a clickable architecture demonstration. It is not yet connected to a production API or database.")

st.divider()
st.caption("Farm-to-Fork Intelligence • Prototype interface • All displayed operational records and nutrient figures are illustrative demo data.")
