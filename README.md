# Metrics-based Google Play app rating system

*Team QuitGooglePlayingGamesWithMy<3*

Ian Kingsbury, Stanley Tang, Audrey Waschura,
Calvin Wong, Lawrence Zhu

## Overview

Our project goal was to create an alternative rating system for Android applications on the Google Play App store that leverages selected metrics and existing review data to expose meaningful indicators of application quality to prospective users in the form of separate ratings based on individual metrics.

These new ratings could help the user better understand how an app’s rating may differ (especially over time or in relation to the original rating) when focusing on specific metrics such as verbosity (review length), sentiment, spelling accuracy, and word frequency. We plan to visualize the ratings derived from these metrics with the original ratings on the same line graph over time. This will help users see historical trends of both original average ratings and average ratings based on specified metrics.

<b>Existing, original ratings on Google Play store:</b>

![](https://github.com/calvwng/app-rating-metrics/blob/master/demo_images/example_ratings.png)

<b>Example of historical sentiment trends vs original rating trends derived by our system:</b>

![](https://github.com/calvwng/app-rating-metrics/blob/master/demo_images/sentiment_chart.png)

<b>Example of word frequency trends displayed by our system using the wordcloud2 library:</b>

![](https://github.com/calvwng/app-rating-metrics/blob/master/demo_images/wordcloud_chart.png)

## Features and Requirements

The following is an overview of the features and corresponding requirements that we fulfilled through the completion of our project:

<table>
  <tr>
    <td>Features</td>
    <td>Requirements</td>
  </tr>
  <tr>
    <td>Present the user with alternative app ratings for an Android app on the Google Play App Store based on different app review/rating metrics</td>
    <td>The user should be able to specify what app to show results for
There should be a way for the user to specify review metrics with ranges to consider in new rating derivations</td>
  </tr>
  <tr>
    <td>Allow users to examine the new alternative ratings and alternative overall rating in comparison to the original rating associated with the target app
Optional: Allow users to examine the new ratings vs the original ratings over time 
Optional: Generate visualizations for rating data</td>
    <td>The user should be able to compare derived app ratings versus original app ratings
Optional: The user should be able to specify date ranges for review examination</td>
  </tr>
</table>


## System Design and Implementation

The following is an overview of our system design and the tools we used:


Client
* The Client (application or visualization interface) requests data from the API.
Metric-based Rating REST API

API
* The Python Flask API receives requests from the client and queries the Server for corresponding data, and returns it to the Client in JSON form.

Server: Metric-based Rating Agent(s)
* The Server retrieves review data from the MySQL DB (through SQLite) to process with its Python agents, and returns requested data to to the Client through the API.

SQLite DBMS
* SQLite is a database management system that the Server uses to interact with the MySQL database.

MySQL DB
* The MySQL DB contains review data for apps supported by our system.



## Relevance to A.I.

The project is relevant to artificial intelligence primarily due to its applications of feature matching and 
agents to process large amounts of review data to expose data (derived metric-scores) and relationships 
(historical trends in comparison with original data) that would otherwise be incredibly tedious for humans to 
produce manually. Although this particular system doesn’t learn or perform predictions like other forms of 
A.I., its domain-specific intelligence can be expanded to support more metrics, since that is its focus.

## Lessons Learned and Future Work

From completing this project, we mainly learned to be very wary tool limitations when designing systems. 
It seemed that every early tool/library/API that seemed to fulfill a role in our system was severely limited 
in free usage, and thus became less viable for us to use since we needed to process a lot of data. If we had 
repeated the project, maybe we could have reached out to the owners of these resources for more usage so that 
we didn’t have to develop our own, less sophisticated tools.

If we decide to move forward with the project, the next steps would be to filter out irrelevant words in the 
"wordcloud," to swap out components we developed with more sophisticated components (such as the sentiment 
analysis), and to make our front-end more intuitive for users.

