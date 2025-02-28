# Riley Wagner

![Riley Wagner](../images/riley.wagner.png)

## About Me

I enjoy running and hiking.

## Research Interests And/Or Favorite Three Topics Covered In Other Classes
- Machine Learning
- Quanitative Finance
- Portfolio Management


## XML to xarray Challenge

Within this challenge, we parsed information from the XML file using xml.etree.ElementTree to extract relevant race and entry-level details. I iterate through each Race and Entry element, collecting attributes such as race date, race number, horse names, jockeys, trainers, finishing positions, and odds.This data was stored in a list of dictionaries, then converted into a Pandas DF before being transformed into an xarray.Dataset.

Here's how I ran a query to find the top 3 horses in each race:
def get_top_3(ds):
    # Convert xarray Dataset to DataFrame and reset index
    df = ds.to_dataframe().reset_index()
    
    # Group by trackID, trackName, raceDate, and raceNumber, then sort and take top 3 per group
    top_3 = (
        df.groupby(["trackID", "trackName", "raceDate", "raceNumber"], group_keys=False)
        [["horse", "finishingPosition", "odds", "purse", "distance", "trackCondition"]]
        .apply(lambda x: x.nsmallest(3, "finishingPosition"))
        .reset_index(drop=True)
    )

    return top_3

# Call the function and get top 3 horses
top_3_horses = get_top_3(ds)

print(top_3_horses)


Sample output from query:

                 horse  finishingPosition  odds     purse  distance trackCondition
0           Insouciant                1.0   2.3   21000.0     500.0             FT
1              Amorica                2.0   2.4   21000.0     500.0             FT
2      Princess Peanut                3.0   6.1   21000.0     500.0             FT