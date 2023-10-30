import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



#1 sedentary hours VS heart attack risk
#encoding the dataframe I'll be working with:
def loading_heart_attack_dataset():
    return pd.read_csv("C:/Users/mocid/Ironhack/labs/projects/Project-2/Data/heart_attack_prediction_dataset.csv")



# let's load it:
heart_attack_dataframe = loading_heart_attack_dataset()

#arranging my dataframe, grouping and plotting it:
def group_and_plot_sedent_hours_risk(heart_attack_dataframe):
    heart_attack_dataframe["Sedentary Hours Per Day Grouped"] = heart_attack_dataframe["Sedentary Hours Per Day"].apply(np.ceil)
    heart_att_sedent_hours = heart_attack_dataframe.groupby("Sedentary Hours Per Day Grouped").aggregate({"Heart Attack Risk": "mean"})
    sns.set_style("dark")
    sns.barplot(x=heart_att_sedent_hours.index, y=heart_att_sedent_hours["Heart Attack Risk"], color="skyblue")
    plt.title("Average heart attack risk per sedentary hours")
    plt.xlabel("Sedentary Hours Per Day Grouped")
    plt.ylabel("Mean Heart Attack Risk")
    plt.savefig("../Figures/Average heart attack risk per sedentary hours.png")
    plt.show()

#running it
group_and_plot_sedent_hours_risk(heart_attack_dataframe)



#2. doing the same thing but for stress levels:
def group_and_plot_stress_levels(heart_attack_dataframe):
    heart_att_stress_levels = heart_attack_dataframe.groupby("Stress Level").aggregate({"Heart Attack Risk":"mean"})
    sns.set_style("dark")
    sns.lineplot(x=heart_att_stress_levels.index, y=heart_att_stress_levels["Heart Attack Risk"], color="skyblue")
    plt.title("Average heart attack risk by stress levels")
    plt.xlabel("Stress Level")
    plt.ylabel("Mean Heart Attack Risk")
    plt.savefig("../Figures/Average heart attack risk by stress levels.png")
    plt.show()

#running it
group_and_plot_stress_levels(heart_attack_dataframe)



#3 samesies but for hours of sleep now:
def group_and_plot_hours_sleep(heart_attack_dataframe):
    heart_att_sleep_hours_day = heart_attack_dataframe.groupby("Sleep Hours Per Day").aggregate({"Heart Attack Risk":"mean"})
    sns.set_style("dark")
    sns.lineplot(x=heart_att_sleep_hours_day.index, y=heart_att_sleep_hours_day["Heart Attack Risk"], color="skyblue")
    plt.title("Average heart attack risk by sleep hours per day")
    plt.xlabel("Hours of sleep")
    plt.ylabel("Mean Heart Attack Risk")
    plt.savefig("../Figures/Average heart attack risk by sleep hours per day.png")
    plt.show()

#running it
group_and_plot_hours_sleep(heart_attack_dataframe)



#4. I also wanna see the risk prevalence per country:
def plotting_prevalence_risk_per_country(heart_attack_dataframe):
    heart_attacks_by_country = (heart_attack_dataframe.groupby("Country")["Heart Attack Risk"].sum() / heart_attack_dataframe.groupby("Country")["Heart Attack Risk"].count() * 100)
    sns.set_style("dark")
    heart_attacks_by_country_sorted = heart_attacks_by_country.sort_values(ascending=True)
    sns.barplot(x=heart_attacks_by_country_sorted.index.values, y=heart_attacks_by_country_sorted, color="skyblue")
    plt.title("Prevalence of people at risk of heart attack per country")
    plt.xlabel("Countries")
    plt.ylabel("Prevalence of '1' as a %")
    plt.xticks(rotation=90)
    plt.savefig("../Figures/Prevalence of people at risk of heart attack per country.png") 
    plt.show()

#running it
plotting_prevalence_risk_per_country(heart_attack_dataframe)


from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd
import requests
import re

def scrap_and_df_air_quality():
    """
a function that scrapes data from iqair.com website, namely a list of countries and another corresponding list
with these countries air quality scores (the bigger the number, the worse the air quality >> the bigger the polution)
merges the two lists into a dictionary and then transforms it into a dataframe
note: USA get replace with United States so I can then merge this dataframe with another one
    """    
    
    air_quality_url = "https://www.iqair.com/world-most-polluted-countries"
    airq_request = requests.get(air_quality_url)
    airq_soup = BeautifulSoup(airq_request.content, "html.parser")
    #list of countries
    airq_countries = airq_soup.find_all("div", {"class":"country-name"})
    airq_countries_cleaned =  [i.getText().strip() for i in airq_countries]
    #list of the air polution
    airq_score_quality = airq_soup.find_all("td", {"class":"mat-cell cdk-cell cdk-column-avg2022 mat-column-avg2022"})
    airq_score_quality_cleaned = [i.getText().strip() for i in airq_score_quality]
    #creating a dictionary
    airq_per_country_dict = {"Country":airq_countries_cleaned,"Air quality score":airq_score_quality_cleaned}
    #into a df
    airq_per_country_df = pd.DataFrame(airq_per_country_dict)
    #USA into United States
    airq_per_country_df.loc[airq_per_country_df['Country'] == 'USA', 'Country'] = 'United States'
    return airq_per_country_df

#running it
scrap_and_df_air_quality()



def create_df_sedent_hours_per_country():
    """a function to create a sedentary hours per day from the original dataframe heart_attack_dataframe """
    sedent_hours_per_country = heart_attack_dataframe.groupby("Country").aggregate({"Sedentary Hours Per Day":"mean"})
    return sedent_hours_per_country

create_df_sedent_hours_per_country()

def plotting_sedentarism_vs_airq():
    """a function to merge the two dataframes sedent_hours_per_country and airq_per_country_df
    and then plot the scatter for these two trying to identify a pattern
    """

    sedent_hours_per_country = create_df_sedent_hours_per_country()
    airq_per_country_df = scrap_and_df_air_quality()
    
    #merging them on the country keeping the values from left (sedent hours per country DF)
    merged_countries_airq = pd.merge(sedent_hours_per_country, airq_per_country_df, on="Country",how="left")
    #coercing the values into numbers so I can plot the trendline. At first I was not able to
    merged_countries_airq["Air quality score"] = pd.to_numeric(merged_countries_airq["Air quality score"], errors="coerce")
    merged_countries_airq["Sedentary Hours Per Day"] = pd.to_numeric(merged_countries_airq["Sedentary Hours Per Day"], errors="coerce")
    #plotting the chart
    sns.set_style("dark")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merged_countries_airq, x="Air quality score", y="Sedentary Hours Per Day", color="skyblue")
    sns.regplot(data=merged_countries_airq, x="Air quality score", y="Sedentary Hours Per Day", scatter=False, color="black")  # Adding a trend line cause it was not clear to me at first
    plt.title("Sedentary Hours vs Air Quality Score")
    plt.xlabel("Air polution score")
    plt.ylabel("Sedentary Hours Per Day")
    plt.savefig("../Figures/Sedentary Hours vs Air Quality Score.png")


    plt.show()

#run this!
plotting_sedentarism_vs_airq()


def scrap_and_df_countries_happiness():
    """
    a function to scrap from https://wisevoter.com/country-rankings/happiest-countries-in-the-world/#people's-republic-of-china
    information on happiness values per country
    """
    happines_country_url = "https://wisevoter.com/country-rankings/happiest-countries-in-the-world/"
    happines_country_request = requests.get(happines_country_url)
    happines_country_request_soup = BeautifulSoup(happines_country_request.content, "html.parser")
    #countries into a list
    happiness_countries = happines_country_request_soup.find_all("h3", {"class":"component3-state-names"})
    happiness_countries_cleaned = [i.getText().strip() for i in happiness_countries]
    #getting their values:
    happiness_countries_scores = happines_country_request_soup.find_all("p", {"class":"description-state-ban-metric-value-label"})
    happiness_countries_scores_cleaned = [i.getText().strip() for i in happiness_countries_scores]
    #into a dictionary so then into a DF:
    happiness_countries_dictionary = {"Country":happiness_countries_cleaned, "Happiness score":happiness_countries_scores_cleaned}
    #into a dataframe:
    happiness_countries_dataframe = pd.DataFrame(happiness_countries_dictionary)
    #renaming US and China:
    happiness_countries_dataframe.loc[happiness_countries_dataframe['Country'] == "United States of America",'Country'] = 'United States'
    happiness_countries_dataframe.loc[happiness_countries_dataframe['Country'] == "People's Republic of China",'Country'] = 'China'
    
    return happiness_countries_dataframe

#run it!
scrap_and_df_countries_happiness()


def create_df_avgs_sleep_stress_physical():
    """a function to create a dataframe with the averages per country of
    3 dimensions: Avg. Physical Activity Days Per Week, Avg. Sleep Hours Per Day and Avg. Stress Level
    """
    grouped_averages = heart_attack_dataframe.groupby("Country")[["Physical Activity Days Per Week", "Sleep Hours Per Day", "Stress Level"]].mean()
    #renamed columns:
    grouped_averages.columns = ["Avg. Physical Activity Days Per Week", "Avg. Sleep Hours Per Day", "Avg. Stress Level"]
    return grouped_averages

#who runs this muthaf*?
create_df_avgs_sleep_stress_physical()


def merge_happiness_averages():
    """
    a function to merge the two dataframes - happiness per country and the several averages we'll be lookin at
    """
    grouped_averages = create_df_avgs_sleep_stress_physical()
    happiness_countries_dataframe = scrap_and_df_countries_happiness()
    merged_happiness_countries = pd.merge(grouped_averages, happiness_countries_dataframe, on="Country",how="left")
    merged_happiness_countries["Avg. Physical Activity Days Per Week"] = pd.to_numeric(merged_happiness_countries["Avg. Physical Activity Days Per Week"], errors="coerce")
    merged_happiness_countries["Avg. Sleep Hours Per Day"] = pd.to_numeric(merged_happiness_countries["Avg. Sleep Hours Per Day"], errors="coerce")
    merged_happiness_countries["Avg. Stress Level"] = pd.to_numeric(merged_happiness_countries["Avg. Stress Level"], errors="coerce")
    merged_happiness_countries["Happiness score"] = pd.to_numeric(merged_happiness_countries["Happiness score"], errors="coerce")
    
    return merged_happiness_countries

#run run run
merge_happiness_averages()



def plot_phys_happiness():
    sns.set_style("dark")
    plt.figure(figsize=(10, 6))
    merged_happiness_countries = merge_happiness_averages()
    sns.scatterplot(data=merged_happiness_countries, x="Avg. Physical Activity Days Per Week", y="Happiness score", color="skyblue")
    sns.regplot(data=merged_happiness_countries, x="Avg. Physical Activity Days Per Week", y="Happiness score", scatter=False, color="black")  
    plt.title("Physical activity and happiness")
    plt.xlabel("Avg. Physical Activity Days Per Week")
    plt.ylabel("Happiness score")
    plt.savefig("../Figures/Physical activity and happiness.png")

    plt.show()

plot_phys_happiness()


def plot_sleep_happiness():
    sns.set_style("dark")
    plt.figure(figsize=(10, 6))
    merged_happiness_countries = merge_happiness_averages()
    sns.scatterplot(data=merged_happiness_countries, x="Avg. Sleep Hours Per Day", y="Happiness score", color="skyblue")
    sns.regplot(data=merged_happiness_countries, x="Avg. Sleep Hours Per Day", y="Happiness score", scatter=False, color="black")  
    plt.title("Sleeping schedule and happiness")
    plt.xlabel("Avg. Sleep Hours Per Day")
    plt.ylabel("Happiness score")
    plt.savefig("../Figures/Sleeping schedule and happiness.png")


    plt.show()

plot_sleep_happiness()


def plot_stress_happiness():
    sns.set_style("dark")
    plt.figure(figsize=(10, 6))
    merged_happiness_countries = merge_happiness_averages()
    sns.scatterplot(data=merged_happiness_countries, x="Avg. Stress Level", y="Happiness score", color="skyblue")
    sns.regplot(data=merged_happiness_countries, x="Avg. Stress Level", y="Happiness score", scatter=False, color="black")  
    plt.title("Stress levels and happiness")
    plt.xlabel("Stress levels")
    plt.ylabel("Happiness score")
    plt.savefig("../Figures/Stress levels and happiness.png")


    plt.show()

plot_stress_happiness()


