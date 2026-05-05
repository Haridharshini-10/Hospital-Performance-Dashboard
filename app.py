import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(page_title="Hospital Performance Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FOR SINGLE PAGE FIT ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow: hidden !important;
        background-color: #0d1117;
    }
    .stApp {
        background-color: #0d1117;
        color: white;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100%;
        height: 100vh;
        overflow: hidden;
    }
    [data-testid="collapsedControl"] {display: none;}
    header[data-testid="stHeader"] {display: none;}
    footer {display: none;}
    
    .header-title {
        color: #38bdf8;
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }
    .kpi-container {
        background-color: #0f4b5b;
        border-radius: 8px;
        padding: 5px 10px;
        text-align: center;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 16px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: 900;
        color: white;
    }
    [data-testid="column"] {
        padding: 0 10px;
    }
    </style>
""", unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv('perfect_hospital_dataset.csv')
    df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
    df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Error loading perfect dataset.")
    st.stop()

filtered_df = df

# --- HEADER ROW ---
st.markdown(f"<div class='header-title'>Hospital Performance Dashboard</div>", unsafe_allow_html=True)

# --- KPI ROW (4 Cards) ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_patients = filtered_df['Patient_ID'].nunique()
total_admissions = len(filtered_df)
avg_cost = filtered_df['Treatment_Cost'].mean() if not filtered_df.empty else 0
avg_los = filtered_df['Length_of_Stay'].mean() if not filtered_df.empty else 0

def render_kpi(title, value):
    return f"""<div class="kpi-container">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>"""

kpi1.markdown(render_kpi("Total Patients", f"{total_patients:,}"), unsafe_allow_html=True)
kpi2.markdown(render_kpi("Total Admissions", f"{total_admissions:,}"), unsafe_allow_html=True)
kpi3.markdown(render_kpi("Avg Treatment Cost", f"${avg_cost:,.0f}"), unsafe_allow_html=True)
kpi4.markdown(render_kpi("Avg Length of Stay", f"{avg_los:.1f} Days"), unsafe_allow_html=True)

# --- CHARTS SECTION ---
chart_height = 280
dark_layout = dict(
    plot_bgcolor="#161b22",
    paper_bgcolor="#161b22",
    font=dict(color="white", size=12, family="Inter, sans-serif"),
    margin=dict(t=50, b=20, l=10, r=10), 
    xaxis=dict(showgrid=False, visible=False),
    yaxis=dict(showgrid=False),
    height=chart_height,
    title=dict(font=dict(size=18, color="#38bdf8"), x=0.5, xanchor='center')
)

if not filtered_df.empty:
    # --- MIDDLE ROW (3 Charts) ---
    mid1, mid2, mid3 = st.columns(3)

    with mid1:
        # 1. HORIZONTAL BAR CHART
        dept_df = filtered_df.groupby('Department').size().reset_index(name='Count').sort_values('Count', ascending=True).tail(5)
        fig_dept = px.bar(dept_df, x='Count', y='Department', orientation='h', title="Top Departments", text='Count', color_discrete_sequence=["#00b4d8"])
        fig_dept.update_traces(textposition='inside', textfont_size=16, textfont_color="white")
        dept_layout = dark_layout.copy()
        dept_layout['margin'] = dict(t=50, b=20, l=10, r=30)
        dept_layout['xaxis'] = dict(showgrid=False, visible=False, range=[0, dept_df['Count'].max() * 1.15])
        dept_layout['bargap'] = 0.25
        fig_dept.update_layout(**dept_layout)
        st.plotly_chart(fig_dept, use_container_width=True)

    with mid2:
        # 2. LINE CHART
        trend_df = filtered_df.groupby(filtered_df['Admission_Date'].dt.to_period("M")).size().reset_index(name='Admissions')
        trend_df['Admission_Date'] = trend_df['Admission_Date'].dt.to_timestamp()
        fig_trend = px.line(trend_df, x='Admission_Date', y='Admissions', title="Admissions Trend", markers=True, color_discrete_sequence=["#38bdf8"])
        
        line_layout = dark_layout.copy()
        line_layout['xaxis'] = dict(showgrid=False, visible=True, title="")
        line_layout['yaxis'] = dict(showgrid=True, gridcolor="#334155", visible=True, title="")
        fig_trend.update_layout(**line_layout)
        st.plotly_chart(fig_trend, use_container_width=True)

    with mid3:
        # 3. CHOROPLETH MAP
        loc_df = filtered_df.groupby('Location').size().reset_index(name='Count')
        state_map = {'California': 'CA', 'Texas': 'TX', 'New York': 'NY', 'Florida': 'FL', 'Illinois': 'IL', 'Pennsylvania': 'PA', 'Ohio': 'OH', 'Georgia': 'GA'}
        loc_df['State'] = loc_df['Location'].map(state_map)
        
        fig_loc = px.choropleth(loc_df, locations='State', locationmode="USA-states", color='Count', scope="usa",
                                color_continuous_scale="Blues", title="Patients by State")
        map_layout = dark_layout.copy()
        map_layout['geo'] = dict(bgcolor='#161b22', lakecolor='#161b22')
        map_layout['margin'] = dict(t=50, b=0, l=0, r=0)
        fig_loc.update_layout(**map_layout, coloraxis_showscale=False)
        st.plotly_chart(fig_loc, use_container_width=True)

    # --- BOTTOM ROW (4 Charts) ---
    bot1, bot2, bot3, bot4 = st.columns(4)

    with bot1:
        # 4. VERTICAL BAR CHART
        diag_df = filtered_df.groupby('Diagnosis').size().reset_index(name='Count').sort_values('Count', ascending=False).head(5)
        fig_diag = px.bar(diag_df, x='Diagnosis', y='Count', title="Top Diagnoses", text='Count', color_discrete_sequence=["#0077b6"])
        fig_diag.update_traces(textposition='inside', textfont_size=16, textfont_color="white")
        
        vert_layout = dark_layout.copy()
        vert_layout['yaxis'] = dict(visible=False, range=[0, diag_df['Count'].max() * 1.15])
        vert_layout['xaxis'] = dict(showgrid=False, visible=True, title="")
        vert_layout['bargap'] = 0.25
        fig_diag.update_layout(**vert_layout)
        st.plotly_chart(fig_diag, use_container_width=True)

    with bot2:
        # 5. SCATTER PLOT
        # Plotting a subset to avoid overplotting (random 500 records)
        scatter_df = filtered_df.sample(n=min(500, len(filtered_df)), random_state=42)
        fig_scatter = px.scatter(scatter_df, x='Length_of_Stay', y='Treatment_Cost', color='Admission_Type', 
                                 title="Cost vs Stay Duration", color_discrete_sequence=["#00b4d8", "#90e0ef", "#03045e"])
        
        scatter_layout = dark_layout.copy()
        scatter_layout['xaxis'] = dict(showgrid=True, gridcolor="#334155", visible=True, title="Days")
        scatter_layout['yaxis'] = dict(showgrid=True, gridcolor="#334155", visible=True, title="$ Cost")
        scatter_layout['showlegend'] = False
        fig_scatter.update_layout(**scatter_layout)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with bot3:
        # 6. DONUT CHART
        type_df = filtered_df.groupby('Admission_Type').size().reset_index(name='Count')
        fig_type = px.pie(type_df, names='Admission_Type', values='Count', title="Admission Types", hole=0.5, color_discrete_sequence=["#00b4d8", "#90e0ef", "#03045e"])
        
        pie_layout = dark_layout.copy()
        pie_layout['margin'] = dict(t=50, b=10, l=10, r=10)
        fig_type.update_layout(**pie_layout)
        fig_type.update_layout(showlegend=False)
        fig_type.update_traces(textinfo='percent+label', textposition='inside', textfont_size=14, textfont_color="white")
        st.plotly_chart(fig_type, use_container_width=True)

    with bot4:
        # 7. FUNNEL CHART
        outcome_df = filtered_df.groupby('Outcome').size().reset_index(name='Count').sort_values('Count', ascending=False)
        fig_funnel = px.funnel(outcome_df, x='Count', y='Outcome', title="Patient Outcomes", color_discrete_sequence=["#00b4d8"])
        fig_funnel.update_traces(textinfo="value+percent initial")
        
        funnel_layout = dark_layout.copy()
        funnel_layout['yaxis'] = dict(visible=True, title="")
        fig_funnel.update_layout(**funnel_layout)
        st.plotly_chart(fig_funnel, use_container_width=True)
