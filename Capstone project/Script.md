# Alcohol Consumption in Europe: Generational Comparison (or I’m a Millennial, am I an alcoholic?)

## I. Introduction: (Dayane)
	 The main idea behind this reasearch came from our own empirical observations of how drinking patterns have shifted in mainstream culture.  
    We have felt a shift from the way people consume alcohol, and it has been something that we have experienced in our own lives. 
    Friend get toghethers no longer revolve around alcohol. it isn't any longer : let's meet up at the bar! Or: I'll bring a bottle of wine over to yours and we can chill. Consumption has dropped in our lives.
    So the questions started rising. Are we just getting old? Is it that we don't have time to drink anymore? Or are our bodies just not so keen on the aftermath of a night out? This begged the question to see if it was actually an age thing. Curiously enough, we also noticed younger people are distancing themselves from alcohol as well. The rise of Coffee Culture, Matcha Drinking, and overall excercise (Gym Culture) in Gen Z seems to be all over the news. 
### *Different news articles about the sober generation page*
    Seeing these articles gave us the idea for our reasearch. Can we prove, with data, that Gen Z is actually drinking less than other generations, specifically the Millenial generation as their immediate counter part. 
## II. Defintions, Data Sources & EDA (Ernesto)
We sourced our data from 2 different institutions. 
* 1. The WHO's Global Information Sustem on Alcohol and Health: We were able to download data on world wide alcohol consumption levels, alcohol consumption patterns, and economic    
    The data for consumption is measured in liters of Pure Alcohol Consumed Percapita in each country by adults. Adults are counted as people that are over the age of 15.
    The data for for consumption patterns is the percentage of the population that abstain from drinking alcohol. Basically they are teetotalers.
* 2. The Institute for Health Metrics and Evaluation of the University of Washington in Seattle : Global Health Data Exchange.  
     From this source we were able to dowlaod data on the Prevalence of Alcohol Use Disorders in the population. Prevalence is the percentage of the population that lives with a specific diseas or disorder. 
     This data was key for our research because it was the only data that we could find that was actually disagreggated by year and age cohorts which allowed our generational Comparison
* For ourt study we've defined some parameters for generations so that we are clear which age cohorts we will use. *Describe generations*
* Previously we've talked about Alcohol use disorders. We'll refer them as AUD's and it will be the main metric we will use to determine impact of alcohol consumption. Since we weren't able to get the actual consumption broken down by age, the Prevalence of AUD will be the factor that will let us know if our age cohorts are drinking more, or less, in comparison to each other. 
* For our EDA, we saw that we had a lot of data and worldwide it might have been too much. Therefor since our original idea came from observations in our environment, we decided to focus on Europe.  
We looked at how each of the data sets we had, behaved and noticed that the diustribution was multimodal, and not normally distributed. This is why we did a clustering analysis. (***Histograms***)
We also saw that in time, the consumption of alcohol for Europe has been dissimilar but with some interesting groupings. (***line chart***)
We took the 3 variables (prevalence of AUD in population, Consumption in Liters Pure Alcohol, Abstention rates in popuation) and see if we could group them. Doing a K means analysis we saw that we have 4 different clusters, that we denominated the 4 EuropeanDrinking Cultures. (***Cluster Chart***)
We decided to focus on 4 countries that represent each of the clusters to limit our data analysis, and add Germany, as it is where we live and where we made our empirical observations. 
## III. Generational Comparison (Ernesto)
How have these age groups behaved historically? Let's take a look at European data for the past +/- 20 years(2010-2019). So it seems that Western European Countries have higher % of AUD in younger generations, but the east has a higher percentage in older generations. This shift is a bit reflective of the drinking cultures we came up with in our clustering but would also say that perhaps younger people are experimenting with drink, and are actually drinking more? (***MAP*** When showing map, switch the side Countries filter to "Select all")
Well, then, we would have to actually look at the comparison of different generations as a snapshot in time. Let's look at a 2019 snapshot of Gen X, Millennial, and Gen Z. 
This chart shows that Gen Z's seem to suffer less with AUD than their 2 immediate generational counterparts. But this is a snapshot of a moment in time, where each generation is at different points in their social, economic, and health development. (***Gen Z Snapshot chart 2019***). 
That's why we decided to look at Millenials and GenZ in a shnap shot of when they were both 20-24 years old. One year where technically they would have similar standards in personal wealth, social, and health factors. (***Slope Chart***)
## IV Conclusions and Interesting Facts. (Dayane)
* These charts we've shown, clearly lead us to believe that Gen Z is actually suffering less of issues with alcohol; than their generational predecesors. If you drink less, your struggles with alcohol will be less. 
* That led us to ask, are there factors that would influence this? Due to scope limitations, we decided to chose 2
* 1. Economic: Does the price of the most accesible alcoholic drink (beer), have an influence on prevalence? The idea here would be that the lower the cost more drinking, thus more prevalence of AUD in the younger generation (***Bubble Chart: Prevalence vs Beer***)
The cases to call out here are Ireland and Czechia. Ireland with higher prices has a higher prevalence of AUD, and Czechia, with a lower economic barrier to consumption, has lower prevalence.
* 2. Cultural: If a country's adult population has high consumption of alcohol, does it mean that they are more culturally "Drunk" nation? The hypothesis here would be that if. country has an overall higher consumption of liters/capita in their adult population, the prevalence of Alcohol Use Disorders would be higher. (***Cultural Chart***)
Again, Czechia and Ireland tend to disprove this theory, Ireland drinks less than both Germany and Czechia, but still has a higher prevalence in AUDs. So the drinking 'Culture' of a nation, doesn't necessarily mean that a younger geneation will drink more.
* 3. So if we establish that Culture and Price doesn't affect drinking prevalence of disease. Why is this going down? We don't have enough data to understand the phenomenon, but there is something that we did notice: We ran a quick analysis in terms of the prevalence divided into age groups. and we do see that Men are drinking quite a bit less than previous generations. If in 2010 a 20 year old man was struggling more with Alcohol Disorders (meaning disorders due to consumption), than a 20 year old man in 2019, but women have remained relatively in the same levels It can be inferred that this observed decrease can be attributed to men following the consumption patterns of women.

## V. Conclusion (Dayane)
Gen Z is not just drinking less — they are drinking differently. The data doesn't allow us to confirm or deny, but poses questions for future research.

Resilience: The countries leading the trend aren't the ones with the highest prices(policy) (Ireland), or have ingraned abstention culture (Albania), but the ones where the youth actively rejected the adult drinking culture (Czechia).




