import pandas as pd
import plotly.express as px
import streamlit as st

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

with col1:
    st.image("matcha_Z.jpeg", use_container_width=True)

with col2:
    st.image("sober_rave.jpg", use_container_width=True)

with col3:
    st.image("therapy_Z.jpeg", use_container_width=True)

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
    return df, df1

df, df1 = load_data()

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
    default=["Germany", "France", "Italy"]
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



# -----------------------------
# CHARTS
# -----------------------------
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


fig1 = px.line(
    df_plot,
    x="year",
    y="Consumption",
    color="Country",
    title="Alcohol Consumption Over Time"
)
fig1.update_yaxes(rangemode="tozero")

st.plotly_chart(fig1, use_container_width=True)

#---
st.subheader("🌍 Alcohol Use Disorder (AUD) Prevalence")

#df1_filtered["age_year"] = (
 #   df1_filtered["age"] + " | " + df1_filtered["year"].astype(str)
  #  )

fig2 = px.choropleth(
        df1_filtered,
        locations="Country",
        locationmode="country names",
        color="Prevalence",
        hover_name="Country",
        animation_frame="age",
        color_continuous_scale="RdYlBu"
    )

fig2.update_geos(
        projection_scale=2.5,
        center={"lat": 54, "lon": 15}
    )

st.plotly_chart(fig2, use_container_width=True)

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

# -----------------------------
st.subheader("📊 Conclusions")

"Here we write what we understood of the analysis. It should look like a closing sentence."