import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import streamlit as st
import plotly.graph_objects as go


# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "../../Cleaned Sets/Aggregated_Table_Prevalence_Consumption_Abstention.csv"
    )
    df1 = pd.read_csv(
        "../../Cleaned Sets/consumption_and_prevalence_2005-2020.csv"
    )
    prev_avg = pd.read_csv('../../Cleaned Sets/prevalence_histogram.csv')
    con_avg = pd.read_csv('../../Cleaned Sets/consumption_histogram.csv')
    abs_avg = pd.read_csv('../../Cleaned Sets/abstention_histogram.csv')
    cluster_df1 = pd.read_csv('../../Ernestos_finds/clusters_with_name.csv')
    return df, df1, prev_avg, con_avg, abs_avg, cluster_df1

df, df1, prev_avg, con_avg, abs_avg, cluster_df1 = load_data()

# -----------------------------
# CLEAN DATA
# -----------------------------
df.rename(columns={
    "consumption_in_liters_per_capita": "Consumption",
    "location": "Country"
}, inplace=True)

df_clean = df.groupby(
    ["Country", "age", "year", "sex"],
    as_index=False
)["Consumption"].mean()

df1["Prevalence"] = df1["precent_of_prevalence"] * 100
df1.rename(columns={"location": "Country"}, inplace=True)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df_clean["Country"].unique()),
    default=["Germany", "France", "Italy", "Czechia", "Ireland"]
)

years = st.sidebar.slider(
    "Select Year Range",
    int(df_clean["year"].min()),
    int(df_clean["year"].max()),
    (2010, 2020)
)

ages = st.sidebar.multiselect(
    "Select Age Group",
    options=sorted(df_clean["age"].unique()),
    default=df_clean["age"].unique()
)

sex = st.sidebar.selectbox(
    "Select Sex",
    options=df_clean["sex"].unique()
)

# -----------------------------
# FILTER DATA (for each graph, include the specific dataframe and it's filters specifics)
# -----------------------------
df_filtered = df_clean[
    (df_clean["Country"].isin(countries)) &
    (df_clean["year"].between(years[0], years[1])) &
    (df_clean["age"].isin(ages)) &
    (df_clean["sex"] == sex)
]
df_plot = df_filtered.groupby(
    ["Country", "year"], as_index=False
)["Consumption"].mean()

df1_filtered = df1[
    (df1["Country"].isin(countries)) &
    (df1["year"].between(years[0], years[1])) &
    (df1["age"].isin(ages))
]

# Tabs for organized content:
# -----------------------------
# TABS
# -----------------------------
tab_home, tab_gen, tab_fun = st.tabs([
    "🏠 Home",
    "📊 Generational Comparison",
    "🎯 Fun Facts & Conclusions"
])

# NEWS - Main page

with tab_home:
    st.set_page_config(page_title="Alcohol Consumption Dashboard", layout="wide")

st.title("Alcohol Consumption in Europe")
st.markdown("### Generational Comparison")
"I'm a Millennial — am I an alcoholic? 👀"

"Is GenZ actually drinking less than Millenials and Boomers?"

st.header("What we found in the news")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
**Gen Z’s “sober curiosity” might be fading**  
Recent data suggests that abstinence is declining in parts of Europe.

[Read article](https://www.emarketer.com/content/gen-z-s-sober-streak-slipping-across-europe)

---

**Nearly half of young Germans don’t drink at all**  
A strong shift toward alcohol-free lifestyles is emerging.

[Read article](https://movendi.ngo/policy-updates/2022/07/25/undoing-the-alcohol-norm-almost-half-of-german-young-adults-live-alcohol-free/)
""")

with col2:
    st.markdown("""
**Young people in the UK: less drinking, but new risks**  
Lower consumption overall, but binge drinking still exists.

[Read article](https://www.theguardian.com/commentisfree/2026/jan/28/young-british-people-alcohol-drinking)

---

**Gen Z is redefining drinking culture globally**  
More intentional, mindful consumption patterns.

[Read article](https://worldcrunch.com/culture-society/gen-z-alcohol-consumption/)
""")

col1, col2, col3 = st.columns(3)

from PIL import Image

def crop_center(img):
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    return img.crop((left, top, right, bottom))

def process_image(path):
    img = Image.open(path)
    img = crop_center(img)
    return img.resize((300, 300))

with col1:
    st.image(process_image("matcha_Z.jpeg"))

with col2:
    st.image(process_image("sober_rave.jpg"))

with col3:
    st.image(process_image("therapy_Z.jpeg"))


# Details for presentation

st.header("Alright, but what do the numbers say?")
"Let's have a close look into the data"

st.info("""
Collected from:  
**World Health Organization**  
**Institute for Health Metrics and Evaluation**
""")

with st.container(border=True):
    st.subheader("Tools")

    col1, col2 = st.columns(2)

    with col1:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg", width=25)
        st.markdown("**Python:** Data wrangling, cleaning, EDA and all the charts")

    with col2:
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=25)
        st.markdown("**Streamlit:** This pretty page you see :)")

st.markdown("""
<div style="
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e1e5ea;
">

<h4>🤓 Some important definitions to help you understand our charts</h4>

<p style="text-align:center; font-weight: bold;">
<span style="color:#4a90e2;"><b>1965 ──── Gen X ──── 1980</b></span>&nbsp;&nbsp;|&nbsp;&nbsp;
<span style="color:#50c878;"><b>1981 ───── Millennials ───── 1996</b></span>&nbsp;&nbsp;|&nbsp;&nbsp;
<span style="color:#f5a623;"><b>1997 ──── Gen Z ──── 2012</b></span>
</p>

<ul>
<li><b>AUD</b> = Alcohol Use Disorders</li>
<li><b>Prevalence</b> = % of population with AUDs</li>
</ul>

</div>
""", unsafe_allow_html=True)

# Global line chart - consumption over the years:

fig1 = px.line(
    df_plot,
    x="year",
    y="Consumption",
    color="Country",
    title="Alcohol Consumption Over Time"
)
fig1.update_yaxes(rangemode="tozero")

st.plotly_chart(fig1, use_container_width=True)

# Consumption over the years - in Germany and Ireland:

countries = ["Germany", "Ireland"]

df_subset = df_clean[df_clean["Country"].isin(countries)]

fig3 = px.line(
    df_subset,
    x="year",
    y="Consumption",
    color="Country",
    title="Alcohol Consumption Over Time"
)
st.plotly_chart(fig3, use_container_width=True)

# Generational analysis

with tab_gen:

    st.header("📊 Generational Comparison")

    st.subheader("🌍 AUD Prevalence by Age")

fig4 = px.choropleth(
        df1_filtered,
        locations="Country",
        locationmode="country names",
        color="Prevalence",
        hover_name="Country",
        animation_frame="age",
        color_continuous_scale="RdYlBu"
    )

fig4.update_geos(
        projection_scale=2.5,
        center={"lat": 54, "lon": 15}
    )

st.plotly_chart(fig4, use_container_width=True)

#---
# Fun facts tab

with tab_fun:

    st.header("🎯 Fun Facts & Conclusions")

    st.markdown("""
### 🧠 Key Insights

- Younger generations drink **less frequently**
- But patterns differ across countries
- Cultural context matters more than age alone

---

### 📊 Conclusion

Gen Z isn’t simply drinking less —  
they are **drinking differently**.
""")

    st.info("➡️ Add fun charts here (top countries, extremes, rankings, etc.)")

# -----------------------------
# CHARTS
# -----------------------------

# Clusters preparation - make it make sense:

fig = make_subplots(rows=1, cols=3,
                    subplot_titles=['Distribution of Percentage of Population with Alcohol Use Disorders',
                                    'Liters/Capita Distribution',
                                    'Abstention Rate Distribution'])
fig.add_trace(go.Histogram(x=prev_avg['precent_of_prevalence'], nbinsx=10,marker_color='#4182D8'),row=1, col=1)
fig.add_trace(go.Histogram(x=con_avg['NumericValue'], nbinsx=10,marker_color='#C85C8E'), row=1, col=2)
fig.add_trace(go.Histogram(x=abs_avg['NumericValue'], nbinsx=10,marker_color='#4E9B30'), row=1, col=3)


fig.update_layout(
    title='Distribution of Key variables - European Drinking Patterns',
    plot_bgcolor='white',
    showlegend=False,
    bargap=0.05,
    height=400,
    width=1200
)
fig.update_xaxes(showgrid=False)
fig.update_xaxes(title_text= '% of population with AUD', row=1, col=1)
fig.update_xaxes(title_text='Liters of Pure Alcohol', row=1, col=2)
fig.update_xaxes(title_text='% of abstainers in Population', row=1, col=3)
fig.update_yaxes(showgrid=True, gridcolor='lightgrey', title_text='Count of Countries')

st.plotly_chart(fig, use_container_width=True)


# Clusters 3D chart
fig2 = px.scatter_3d(cluster_df1, 
                    x='liters/capita', 
                    y='abstention_rate', 
                    z='prevalence',
                    color='cluster',
                    hover_name='location',
                    title='The 4 Drinking Cultures of Europe (2019)',
                    template='plotly_dark',
                    width=1000,
                    height=1000,    
                    labels={'val': 'Prevalence (Disorders)', 
                            'liters': 'Liters per Capita', 
                            'abstention_rate': '% Abstainers'})
fig2.update_layout(
    scene=dict(
        yaxis=dict(autorange='reversed')
    )
)
st.plotly_chart(fig2, use_container_width=True)

# -------