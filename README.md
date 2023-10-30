# Project-2 

![It's all about the heart](https://media.giphy.com/media/GR8YxC3C7SOiUFlDYI/giphy.gif)

## Intro

In this project I am working on top of [a dataset that can be found in Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/heart-attack-prediction-dataset).

The dataset is comprised of a list of 8000+ inquired anonymized people on their general health and lyfestyle which assesses the risk of having a heart attack. We have information on wheter the person smokes or not, their BMI, Triglycerides, sedentarism and activity hours amognst others, and lastly these provide a binary 1 - Yes, risk of heart attack or 0 - no risk.

Unfortunately we do not have access to the equation producing the final binary.

I will then enrich this dataset with scrapped information the happiness index per country and the air quality per country, relating the first with several dimensions provided in the original data set and the later with the sedentarism, also provided in Kaggle's dataset.

_Disclaimer: main purpose of this project was, at least for me, to train profficiency in pipelines and importing+managing data from external sources, in my case, by scrapping the web. Even tough in other contexts I would try to come up with the most realistic possible analysis, I will be working with averages, which on their own remove a substantial amount of information but I wil also isolate the variables that give us the final binary, jeopardizing the results._ 

## The approach

![The approach](https://media.giphy.com/media/adXwYTDvQNOMCggg8i/giphy.gif)

### 1. The libraries used
Pandas

Numpy

Seaborn

Matplotlib.pyplot 

BeautifulSoup


### 2. The method
The working file can be found in the Notebooks folder with the title Working notebook.

The downloaded and converted into a dataframe dataset was quite clean already. Some functions were applied to assess whether it should be scrutinized and cleaned (namely - checking column types, check for nulls and duplicates).

**Sedentarism** was groupped into clusters of sedentary hours per day and aggregated by the mean of the heart attack risk. 
Following was the plot of this risk per cluster, expecting to find that the more the sedentary hours, the bigger the heart attack risk (given by the binary 1).

**Stress Levels** were subject to the same process as sedentarism. Stress levels were assessed in the dataset on a scale of 1-10 (10 being most stressed).

**Sleep Hours Per Day** were subject to the same process as both. These were given as a Float where the values range from 4 to 10.

Deepening my interest in the data I had cleaned and ready to drive conclusions from, I crossed sedentarism with Air Quality per country.

**Air Quality** was scrapped from [the IQAir website](https://www.iqair.com/world-most-polluted-countries) as an index where the bigger the value, the more polluted (worse qualuty) the air is in that country. _BeautifulSoup_ and _Requests_ were imported to do so.

A new Dataframe was created with the information on sedentarism and airquality via a left merge procedure where I kept the countries in the first dataframe (20 countries).

Scatter plots were driven using Seaborn to visually check the correlation between these two variables per country.

**Happiness per country** was scrapped from [the WiseVoter website](https://wisevoter.com/country-rankings/happiest-countries-in-the-world/#people's-republic-of-china) as an index where the bigger the value, the happier the country. This variable was subject to the same procedure as Air Quality, in this instance however, I've created a new dataframe with this dimension but also _Avg. Physical Activity Days Per Week_, _Avg. Sleep Hours Per Day_ and _Avg. Stress Level_. 

Following this I've plotted my results in a scatter diagram. 

## The conclusions 

![The conclusions](https://media.giphy.com/media/QYjBjXLiF6I0i0WZH1/giphy.gif)

###### I need to stress out again that I am deconstructing a model that gives us a YES - risk of heart attack / NO - and via an equation I don't have access to - by correlating in an isolated manner, the variables that compose this model, with some other external variables. Also I am applying averages to group the results per country, which on it's own is not the best procedure when we want a high level of correctness of data, but once again, my personal goal with this project was to train data management and include data from external sources.

The top 3 countries where the risk of having a heart attack is the most prevalent are:

    1. South Korea
    2. Nigeria
    3. United States

One could only wonder, speaking in a macro way, why South Korea would figure in the first place given they follow a relatively well balanced diet and have a good healthcare system. Having a high pressure on the economic classic role in society translating into extremely high standards for education and the job could possibly justify this. 

The countries where the prevalence was the lowest were:

    18. Japan
    19. Italy
    20. India

**Air pollution and sedentarism** - the correlation is very broad and weak. One could expect for the most polluted countries to be largely more sedentary than the other way around which is not true.

**Happiness and...**

_Physical activity_: we see, to a very slight degree that the more people engage in physical activity, the happier they are. Once again, we are talking about 20 observations (unique countries in the original dataset) and we are groupping all the results to a national level.

_Sleeping schedule_: ironically we see that, **on average** after 6h54 of sleep, the happiness indices do not increase. 

_Stress levels_: plotting this correlation suggests there's actually not a link between the two. One could expect stressed out people to feel sadder, but that's not what the data suggests.



###### The human heart has the ability to squirt blood up to 30 feet. That's roughly the length of a small bus! This remarkable feat allows your blood to circulate throughout your entire body, delivering oxygen and nutrients to your cells.

###### Research suggests that happiness can be contagious. A study published in the British Medical Journal found that when one person becomes happier, the happiness of a friend living close by increases by 25%. So, spreading joy not only benefits you but also those around you!






