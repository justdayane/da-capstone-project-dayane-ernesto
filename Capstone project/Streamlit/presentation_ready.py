import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

# -----------------------------
# PAGE CONFIG 
# -----------------------------
st.set_page_config(page_title="Alcohol Consumption Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../../Cleaned Sets/Aggregated_Table_Prevalence_Consumption_Abstention.csv")
    df1 = pd.read_csv("../../Cleaned Sets/consumption_and_prevalence_2005-2020.csv")
    prev_avg = pd.read_csv('../../Cleaned Sets/prevalence_histogram.csv')
    con_avg = pd.read_csv('../../Cleaned Sets/consumption_histogram.csv')
    abs_avg = pd.read_csv('../../Cleaned Sets/abstention_histogram.csv')
    cluster_df1 = pd.read_csv('../../Ernestos_finds/clusters_with_name.csv')
    snapshot = pd.read_csv('../../Cleaned Sets/2019_snapshot_prevalence_of_generations.csv')
    slope_chart = pd.read_csv('../../Cleaned Sets/slope_chart_df_clean.csv')
    beerdf = pd.read_csv('../../Cleaned Sets/prevalence_vs_beer_clean.csv')
    culturedf = pd.read_csv('../../Cleaned Sets/consumption_vs_prevalence.csv')
    gender_comparison = pd.read_csv('../../Cleaned Sets/consumption_males_vs_females.csv')
    return df, df1, prev_avg, con_avg, abs_avg, cluster_df1, snapshot, slope_chart, beerdf, culturedf, gender_comparison

df, df1, prev_avg, con_avg, abs_avg, cluster_df1, snapshot, slope_chart, beerdf, culturedf, gender_comparison = load_data()

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

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df_clean["Country"].unique()),
    default=["Germany", "Albania", "Italy", "Czechia", "Ireland"]
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


# -----------------------------
# FILTER DATA
# -----------------------------
df_filtered = df_clean[
    (df_clean["Country"].isin(selected_countries)) &
    (df_clean["year"].between(years[0], years[1])) &
    (df_clean["age"].isin(ages)) 
]

df_plot = df_filtered.groupby(
    ["Country", "year"], as_index=False
)["Consumption"].mean()

df1_filtered = df1[
    (df1["Country"].isin(selected_countries)) &
    (df1["year"].between(years[0], years[1])) &
    (df1["age"].isin(ages))
]

# -----------------------------
# IMAGE HELPERS
# -----------------------------
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

# -----------------------------
# GLOBAL TITLE
# -----------------------------
st.title("🍷 Alcohol Consumption in Europe")
st.markdown("### Generational Comparison")
st.write("I'm a Millennial — am I an alcoholic? 👀")

# -----------------------------
# TABS
# -----------------------------
tab_home, tab_gen, tab_fun = st.tabs([
    "Starting point",
    "Generational Comparison",
    "Fun Facts & Conclusions"
])

# =============================
# 🏠 HOME TAB
# =============================
with tab_home:

    st.header("📰 What we found in the news")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
**Gen Z’s “sober curiosity” might be fading**  
[Read article](https://www.emarketer.com/content/gen-z-s-sober-streak-slipping-across-europe)

---

**Nearly half of young Germans don’t drink at all**  
[Read article](https://movendi.ngo/policy-updates/2022/07/25/undoing-the-alcohol-norm-almost-half-of-german-young-adults-live-alcohol-free/)
""")

    with col2:
        st.markdown("""
**Young people in the UK: less drinking, but new risks**  
[Read article](https://www.theguardian.com/commentisfree/2026/jan/28/young-british-people-alcohol-drinking)

---

**Gen Z is redefining drinking culture globally**  
[Read article](https://worldcrunch.com/culture-society/gen-z-alcohol-consumption/)
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(process_image("matcha_Z.jpeg"))

    with col2:
        st.image(process_image("sober_rave.jpg"))

    with col3:
        st.image(process_image("therapy_Z.jpeg"))

    st.header("Alright, but what do the numbers say?")

    st.info("""
Data collected from:  
**World Health Organization**  
**Institute for Health Metrics and Evaluation**
""")
    
    st.markdown("""
<div style="
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e1e5ea;
">

<h4>🤓 Some important definitions to help you understand our charts</h4>

<p style="text-align:center; font-weight: bold;">
<span style="color:#4a90e2;"><b>1965 ───── Gen X ───── 1980</b></span>&nbsp;&nbsp;|&nbsp;&nbsp;
<span style="color:#50c878;"><b>1981 ───── Millennials ───── 1996</b></span>&nbsp;&nbsp;|&nbsp;&nbsp;
<span style="color:#f5a623;"><b>1997 ───── Gen Z ───── 2012</b></span>
</p>

<ul>
<li><b>AUD</b> = Alcohol Use Disorders</li>
<li><b>Consumption</b> = in Liters of pure alcohol per year</li>
<li><b>Prevalence</b> = % of population with AUDs</li>
</ul>

</div>
""", unsafe_allow_html=True)
    
    # Histogram: data overview for clusters
    fig = make_subplots(rows=1, cols=3,
                    subplot_titles=['Distribution of Population with Alcohol Use Disorders',
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
    fig.update_xaxes(title_text= '% of population with AUD', row=1, col=1,tickformat=".0%")
    fig.update_xaxes(title_text='Liters of Pure Alcohol', row=1, col=2)
    fig.update_xaxes(title_text='% of abstainers in Population', row=1, col=3,ticksuffix="%")
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey', title_text='Count of Countries')

    st.plotly_chart(fig, use_container_width=True)

     # Line chart - global
    fig1 = px.line(df_plot, x="year", y="Consumption", color="Country")
    fig1.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig1, use_container_width=True)

    # Clusters 3D
    fig2 = px.scatter_3d(cluster_df1,
        x='liters/capita',
        y='abstention_rate',
        z='prevalence',
        color='cluster',
        hover_name='location'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Focus countries
    focus_countries = ["Germany", "Ireland"]
    df_subset = df_plot[df_plot["Country"].isin(focus_countries)]

    fig3 = px.line(df_subset, x="year", y="Consumption", color="Country")
    st.plotly_chart(fig3, use_container_width=True)

# =============================
# 📊 GENERATIONAL TAB
# =============================
with tab_gen:

    st.header("Generational Comparison")

# World map with AUD info per age group
    fig4 = px.choropleth(
        df1_filtered,
        locations="Country",
        locationmode="country names",
        color="Prevalence",
        hover_name="Country",
        animation_frame="age",
        color_continuous_scale="sunset",
        title="AUD Prevalence per Age group"
    )
    fig4.update_geos(
        projection_scale=2.5,
        center={"lat": 54, "lon": 15}
    )

    st.plotly_chart(fig4, use_container_width=True)


# Data snapshot 2010 vs 2019. Millenials & GenZ
    fig5 = px.bar(
    snapshot,
    x = 'location',
    y = 'percent_of_prevalence',
    color='generation',
    barmode = 'group',
    category_orders={'generation': ['Gen_X', 'Millennial', 'Gen_Z']},  # ← add this
    color_discrete_sequence=px.colors.qualitative.Dark24,  # closest to 'Dark2'
    title = 'The Gen Z pivot: Snapshot 2019 - AUD prevalence by Generation',
    labels = {
        'location':'Countries',
        'percent_of_prevalence':'Average Prevalence of AUD (%)',
        'generation':'Generation' 
    }
)
    fig5.update_layout(
    yaxis_tickformat='.2f',
    yaxis_ticksuffix='%',
    bargap=0.15,
    bargroupgap=0.05,
    plot_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    legend=dict(
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1.15
    ),
    margin=dict(l=60, r=60, t=60, b=60),
    height=500,
    width=900
)

    fig5.update_traces(
    marker_line_width=0,
    marker_line_color='rgba(0,0,0,0)'
)
    fig5.for_each_trace(lambda t: t.update(name={
    'Gen_Z': 'Gen Z (1997-2012)',
    'Millennial': 'Millennial (1981-1996)',
    'Gen_X':'Gen X (1965-1980)'
}.get(t.name, t.name)))

    st.plotly_chart(fig5, use_container_width=True)

# Slope chart, generation snapshot for 2010 and 2019

    fig6 = go.Figure()
    offsets = {'Albania': -0.002, 'Czechia': 0.002}

    colors = {
    'Albania': '#1f77b4',
    'Czechia': '#ff7f0e',
    'Germany': '#2ca02c',
    'Ireland': '#d62728',
    'Italy': '#9467bd'
}

    for country in slope_chart['location'].unique():
        val_2010 = slope_chart.loc[slope_chart['location'] == country, '2010'].values[0]
        val_2019 = slope_chart.loc[slope_chart['location'] == country, '2019'].values[0]
        color = colors.get(country, 'grey')

    # Draw line
        fig6.add_trace(go.Scatter(
        x=[2010, 2019],
        y=[val_2010, val_2019],
        mode='lines+markers',
        name=country,
        line=dict(color=color, width=2),
        marker=dict(size=8),
        hovertemplate=f'<b>{country}</b><br>Year: %{{x}}<br>Prevalence: %{{y:.2%}}<extra></extra>'
    ))

    # Left label
        fig6.add_annotation(
        x=2009.8, y=val_2010,
        text=f'{country}: {val_2010*100:.2f}%',
        xanchor='right', showarrow=False,
        font=dict(size=11, color=color),
        yshift=offsets.get(country,0) *2000
    )

    # Right label
        fig6.add_annotation(
        x=2019.2, y=val_2019,
        text=f'{country}: {val_2019*100:.2f}%',
        xanchor='left', showarrow=False,
        font=dict(size=11, color=color),
        yshift=offsets.get(country,0) *2000
    )

        fig6.update_layout(
        title=dict(text="The '20-Year-Old' Risk Profile: 2010 (Millennial) vs. 2019 (Gen Z)", font=dict(size=14)),
        plot_bgcolor='white',
        showlegend=False,
        height=600,
        width=900,
        xaxis=dict(
        tickvals=[2010, 2019],
        ticktext=['Millennial (in 2010)', 'Gen Z (in 2019)'],
        showgrid=False,
        range=[2007, 2022]
    ),
        yaxis=dict(
        tickformat='.2%',
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dash',
        gridwidth=1,
        range=[0, slope_chart[['2010', '2019']].values.max() * 1.2],
        rangemode="tozero" 
    ),
        margin=dict(l=200, r=200, t=60, b=60)
)
       
    st.plotly_chart(fig6, use_container_width=True)

# =============================
# 🎯 FUN TAB
# =============================
with tab_fun:

    st.header("Fun Facts & Conclusions")

# Beer prices chart
    colors = {
    'Albania': '#1f77b4',
    'Czechia': '#ff7f0e',
    'Germany': '#2ca02c',
    'Ireland': '#d62728',
    'Italy': '#9467bd'
}
    fig7 = px.scatter(
    
    beerdf, x='beer_price_usd', 
    y='percent_of_prevalence',
    color='location',
    text='location',
    color_discrete_map=colors,
    title='Gen Z Alcohol Risk vs. Beer Price (2019)',
    labels={
        'location':'Country',
        'beer_price_usd': 'Price of 500ml Beer in US dollars',
        'percent_of_prevalence':'Gen Z Prevalence of Disorders (%)',
            },
    size_max=160,
    height=600,
    width=900
)
    fig7.update_traces(marker=dict(size=20), textposition='top center')
    fig7.update_traces(
    textposition='bottom center',
    selector={'name':'Albania'}
)
    fig7.update_layout(
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='lightgrey',griddash='solid'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey', griddash='solid',tickformat='.2%',title=dict(standoff=30)),
    showlegend=False,
    margin=dict(l=100, r=60,t=60, b=60)
)
    st.plotly_chart(fig7, use_container_width=True)   

    colors = {
    'Albania': '#1f77b4',
    'Czechia': '#ff7f0e',
    'Germany': '#2ca02c',
    'Ireland': '#d62728',
    'Italy': '#9467bd'
}
    fig8 = px.scatter(
    
    culturedf, x='liters_per_capita', 
    y='percent_of_prevalence',
    color='location',
    color_discrete_map=colors,
    text='location',
    title='Gen Z Population % with AUDs vs National Consumption in Liters of Pure Alcohol (2019)',
    labels={
        'location':'Country',
        'liters_per_capita': 'Liters of Pure Alcohol Consumed Percapita',
        'percent_of_prevalence':'Gen Z Prevalence of Disorders (%)',
            },
    size_max=160,
    height=600,
    width=900
)
    fig8.update_traces(marker=dict(size=20), textposition='top center')
    fig8.update_layout(
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='lightgrey',griddash='dash'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey', griddash='dash',tickformat='.2%',title=dict(standoff=30)),
    showlegend=True,
    margin=dict(l=100, r=60,t=60, b=60)
)
    st.plotly_chart(fig8, use_container_width=True)  

    # Gender comparison 
    colors = {
    'Albania': '#1f77b4',
    'Czechia': '#ff7f0e',
    'Germany': '#2ca02c',
    'Ireland': '#d62728',
    'Italy': '#9467bd'
}
    fig9 = px.line(
    gender_comparison,
    x='year',
    y='percent_of_prevalence',
    color='location',
    line_dash='sex',
    symbol='sex',
    title='Gen Z Prevalence : Who is leading the Charge',
    labels={
        'year':'Year',
        'percent_of_prevalence':'Prevalence of Alcohol Use Disorders(%)',
        'location':'Country',
        'sex':'Gender'},
    color_discrete_map=colors,
    markers=True,
    category_orders={'year':sorted(gender_comparison['year'].unique())}
)
    fig9.update_layout(
    plot_bgcolor='white',
    hovermode='closest',
    legend=dict(
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='left',
        x=1.02
    ),
    width=1000,
    height=600
)
    fig9.update_xaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5)
    fig9.update_yaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5, tickformat=".1%",title=dict(standoff=20))
    
    st.plotly_chart(fig9, use_container_width=True)  


    with st.container(border=True):
            st.subheader("Tools")

            col1, col2 = st.columns(2)

            with col1:
                st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg", width=25)
                st.markdown("**Python:** Data wrangling, cleaning, EDA and all the charts")

            with col2:
                st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=25)
                st.markdown("**Streamlit:** This pretty page you see :)")
    
    st.write("""
### 📊 Conclusions (for now)

Gen Z is not just drinking less — they are drinking differently.
The data doesn't allow us to confirm or deny, but poses questions for future research.  

Resilience: The countries leading the trend aren't the ones with the highest prices(policy) (Ireland), or have ingraned drinking culture (Germany), but the ones where the youth actively rejected the adult drinking culture (Czechia).
""")