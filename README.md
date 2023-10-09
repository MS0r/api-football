Hello, this is an api based on openfootball's database, specifically the champions league database from 2011 to 2023, but this api wil only cover the group stage season included from 2012-13 to 2019-20 because 2011-12 and 2022-23 dont have group stage information

API Information:

temp = 2012-13, 2013-14, 2014-15, 2015-16, 2016-17, 2017-18, 2018-19, 2019-20
- /"temp"/teams : temp is used to indicate the champions league season, use this to get all the 32 teams that compose the group stage
- /"temp"/groups : get all the groups formed
- /"temp"/matchdays: get all the dates when matchs would be played
- /"temp"/results/"matchday": get all the result from a specific matchday
- /"temp"/results/ : get all results

queries:

- goals = minimum number of goals made in the game
- team = team who has played the match either local or away
- stadium = stadium where the game has been played
- day = either day of the week, month or specific day

- /"temp"/"group"/group: group to indicate what group do you want to get information, get teams of the group
- /"temp"/"group"/results: get all the results from the specify group