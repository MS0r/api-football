## Hello, this is an api based on openfootball's database, specifically the champions league database from 2011 to 2023, but this api wil only cover the group stage season included from 2012-13 to 2019-20 because 2011-12 and 2022-23 dont have group stage information

### API Information:

#### Authentication

First of all you have to get a bearer token, to do that, you have to register using
```
[POST] /auth/register
```
and request body
```json
{
    "username" : "<your_username>",
    "password" : "<your_password>"
}
```
after you register in the api you have to get the token from your user
```plain
[POST] /auth/login
```
using the same json schema from /auth/register, from that you will get your token as
```json
{
    "Success" : "True",
     "token" : "<your_token>"
}
```
therefore, before any requests you are going to do to the api, you must put on your request headers:
Authorization =  bearer "your_token"

#### variables:
- temp = 2012-13, 2013-14, 2014-15, 2015-16, 2016-17, 2017-18, 2018-19, 2019-20
- matchday = 1,2,3,4,5,6
- group = A, B, C, D, E, F, G, H

#### URL
```plain
http://{host:port}/api/v1
```
All requests to the api with the url prefix
```plain
[GET] /<temp>/teams
```
Get all the 32 teams that compose the group stage
```plain
[GET] /<temp>/groups
```
Get all the groups formed
```plain
[GET] /<temp>/matchdays
```
Get all the dates when matchs would be played
```plain
[GET] /<temp>/results/<matchday>
```
Get all the result from a specific matchday
```plain
[GET] /<temp>/results
```
Get all results
```plain
[GET] /<temp>/<group>/group
```
Get teams of the group
```plain
[GET] /<temp>/<group>/results
```
Get all the results from the specify group

#### parameters for results
```plain
[GET] /<temp>/results?goals=2
```
minimum number of goals made in the game
```plain
[GET] /<temp>/results?team=Arsenal
```
team who has played the match either local or away
```plain
[GET] /<temp>/results?stadium=Bernabeu
```
stadium where the game has been played
```plain
[GET] /<temp>/results?day=Tue

[GET] /<temp>/results?day=Sep

[GET] /<temp>/results?day=16
```
either day of the week, month or specific day


