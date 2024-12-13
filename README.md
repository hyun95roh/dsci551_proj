# DSCI 551 proj
DSCI_551 Database Management - CHATDB_39

## File Structure 
<details> 

#### 0) Root 
0.1) NLP folder - a folder containing core modules.

0.2) data folder - a folder storing raw data set.
    
0.3) images folder - a folder having images for readme and streamlit app.
    
0.4) readme 
    
0.5) environment.yml 
    
0.6) streamlit.py - the module for building streamlit app.

#### 1. NLP 
1.1) Deprecated - outdated files are sleeping in here.

1.2) NLQ_implmentation - Two python file for handling natural language query to database query:  ***nlq_to_fbquery.py*** and ***nlq_to_sql.py*** 

1.3) Script -
 -  ***mysql.py*** and ***firebase.py*** are modules for interacting with each database. Based on these two module, ***retrieve_data.py*** provides retriever that outputs table-like retrieval result for each database query. If your query has correct syntax, you are even allowed to add or delete tables in MySQL. In Firebase, we disabled DELETE to avoid accidental loss of data, while you can still add new data by using POST or PATCH. 
 -  ***example_query.py*** and ***dataexplore_query.py*** supports browsing database query examples and database itself. Please refer to ***How to use CHATDB*** in readme for further details.    

1.4) main.py - this module aggregates scripts under the NLP folder and provide gateway function named 'handle_user_input', which handles input from users and call the specific functions corresponding to the user demand.

#### 2) data - folder to store raw data(csv files)

#### 3) images - images for readme and streamlit are stored


</details>

----

## Archietecture 
<details>

![architecture_01](./images/architecture_01.png)

![architecture_02](./images/architecture_02.png)


![architecture_03](./images/architecture_03.png)


![architecture_04](./images/architecture_04.png)

</details>

---
## How to use CHATDB
#### Step 1 : Clone this github repository
#### Step 2 : Turn on your terminal, set your the root directory of this repository as your current directory(cd). 
#### Step 3 : Type 'streamlit run streamlit.py' and you will see the streamlit running as on a localhost.

#### Step 4 : Utilize navigational questions. 
If you successfuly launched the streamlit, now go to page 2 to see the chatbox where you can associate with our ChatDB.  

![snapshot](./images/snapshot.png)
Here is a snapshot that shows the flow of navigational questions from our ChatDB. By answering  specific keywords that match the pattern, users can move on to the next questions and get the result, whichever be database query or the retrieval outcome, at the end.

|Navigational Prompt|DB Exploration|Example DB Query|Natural Language to DB Language|
|---|---|---|---|
|Q1. Please choose an option: 1 (Database) 2 (Examples), 3 (NLQ)|Type one of: ***DB, database, 1***| Type one of : ***example(s), example query, 2*** | Type one of: ***nlq, 3*** |
|Q2. Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase| Type one of: ***(my)sql, fire(base)*** | Type one of: ***(my)sql, fire(base)*** | Type one of: ***(my)sql, fire(base)*** |
|Q3. Type available commands | Type one of the table/collection of interest: ***explore {CDC\|STOCK\|FRED}*** | Type specific query of interest: (SQL) ***example query {where \| groupby\| orderby\| having\|aggregation}*** (FIREBASE) ***example query {get \| orderby \| range}*** | Please refer to 'How to generate response from natural language' 

**( Note )** You can always go back to the first stage by typing ***initial***. 

---
## How to generate response from natural language
|DB Language|Natural Language Query(NLQ)|
| --------- | -------------------- |
| SELECT | 'find', 'display', 'show', 'list', 'identify', 'retrieve', 'tell', 'calculate', 'select' |
| FROM | name of actual dataset |
| GROUP BY | closest attribute near <pattern> |
| AGGREGATION | 'count', 'sum', 'avg', 'min', 'max' |
| ORDER BY | 'ordered by', 'sorted by' + {'ascending','asc','increasing','up','descedning','desc'} |
| LIMIT | 'top', 'highest', 'lowest', 'only', 'limit' |
| WHERE | 'is greater than', 'is bigger than', 'is smaller than' |


Providing a unbreakable database query should take various information into consideration, such as data type of attributes and value distribution of attributes. To avoid this complexity between the nature of attributes and faultless database query, we offer samples of executable list of validated natural language queries.  
<details>
<summary>List of Executable NLQ</summary>

**( Note )** Table names and attribute names are case-sensitive.

> MySQL
1. "Display the sum of ESTIMATE grouped by GROUP_NAME in CDC;"
2. "List all NOV values from STOCK LIMIT 10;"
3. "Show top 5 income values from FRED;"
4. "Show me LLY FROM STOCK"

> Firebase 
1. show highest 5 Real_Median_Household_Income startat 50000 endat 70000 from FRED
2. show LLY startat 50 from STOCK
3. show LLY startat 50 and endat 100 from STOCK
4. show REAL_Median_Household_Income from FRED
5. show highest 5 Estimate in CDC 
6. show first 10 time_period_id from dataset CDC 

</details>

---
## Tech Stacks 
|Category|Item|Subitems|
|---|---|---|
|Databse|SQL|MySQL|
|Databse|NoSQL|Firebase Realtime Database|
|Development|Python|Library: pandas, random, re, json, pprint, pymysql, requests, time|
|Deployment|Streamlit|Library: streamlit| 

---
## Contributors
|Name|Contact|
|---|---|
|Hyuntae Roh|hroh@usc.edu|
|Jing Chuang|cchuang8@usc.edu|
|Hayong Son|hayoungs@usc.edu|
