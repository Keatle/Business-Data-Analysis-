import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt
from pathlib import Path

# Use visualizations and descriptive statistics to explore the dataset 

path = Path(r"..\Project\data\Q1_Output.db")

    # 1. Demographics and Roles
# 1. How has the number of users in each MainBranch category changed over three years?
                
# Users in MainBranch 

conn = sqlite3.connect(path)

    # Display X : num users in MainBranch , Y : Years ( 2022 , 2021 , 2023)

df = pd.read_sql_query("SELECT * FROM clean_data", conn)
df['Year']= df['Year'].astype(str)

df_graph = pd.crosstab(df['MainBranch'], df['Year'])
df_graph.plot(kind='bar', figsize=(10,7))

plt.title("MainBranch Count per Year")
plt.xlabel("Main Branch")
plt.ylabel("Count")
plt.legend(title="Year")
plt.tight_layout()
plt.show()

##  The mainbranch user count has improved over the years in the professional developer category going from less than 
## 20000 people to over 30000, selftaught and Occasional coder 
##  and for the former developer and the hobbyist.
## As for the student category it has decreased 


                # 2. What are the trends in users' Age, Country, EdLevel, and YearsCode 
                # across different MainBranch categories?

#          Age

# Ensure Year is treated as a string or int (based on your DB structure)
df['Age'] = df['Age'].astype(str)

age_graph = pd.crosstab(df['MainBranch'], df['Age'])
age_graph.plot(kind='bar', figsize=(10, 7))

plt.title("Age groups across MainBranch categories")
plt.xlabel('Users in MainBranch')
plt.ylabel('Count')
plt.legend(title="Age")
plt.tight_layout()
plt.show()

# There are more users in the Professional Developer branch overall, 
# with the 25–34 age group having the highest user count in that category.



#          Country 
country_graph =pd.crosstab(df['MainBranch'], df['Country'])
country_graph.plot(kind= 'bar', figsize=(10, 7))

plt.title("Countries across MainBranch categories")
plt.xlabel('Users in MainBranch')
plt.ylabel('Country')
plt.legend(title ='Age')
plt.tight_layout()
plt.show()

## Professional developer branch ,  has highest number of users across all countries ,
## and categories in comparison , with the highest number of professionals being from Italy .



#          EdLevel
edlevel_graph = pd.crosstab(df['MainBranch'], df['EdLevel'])
edlevel_graph.plot(kind='bar', figsize=(10,7))

plt.title("EdLevel indiduals across MainBranch categories")
plt.xlabel('Users in MainBranch')
plt.ylabel('Count')
plt.legend(title ='EdLevel')
plt.tight_layout()
plt.show()

## Professional developer branch ,  has highest number of users across all categoriries ,
## with Bachelor's degre being the highest with close to 30 000 users, followed by Master's Degree with just under 15 000 
##  and Tertiary Education with close to 10 000
## 



#         YearsCode

                         # Filter the years into categories of 10s

def clean_years_code(val):
    if val == 'Less than 1 year':
        return 0
    elif val == 'More than 50 years':
        return 51
    try:
        return float(val)
    except:
        return None

                        #clean the data set 
df['YearsCodeCleaned'] = df['YearsCode'].apply(clean_years_code)

bins = [0, 10, 20, 30, 40, 50, float('inf')]
ranges = ['0-9' , '10-19', '20-29','30-39','40-49','50+']

df['YearsCodeGroup'] = pd.cut(df['YearsCodeCleaned'], bins=bins , labels=ranges, right=False)


yearscode_graph =pd.crosstab(df['MainBranch'], df['YearsCodeGroup'])
yearscode_graph.plot(kind='bar', figsize=(10,7))


plt.title("YearsCode of indiduals across MainBranch categories")
plt.xlabel('MainBranch Category')
plt.ylabel('Count')
plt.legend(title='Years of coding experience')
plt.show()

##  The years of coding experience with the highest count ranges from 10-19 , followed by more than 20 000 of professionals 
##  with coding experience ranging between 0-9 years , with a drastic difference between professionals with a range pf 20- 29 years of experience.
##



    #  2. Technology Trends and Preferences

                # 1. What are the top 5 most popular databases and programming languages 
                # that GitHub users currently use and want to use in the future




       ### Databases ###

# top 5 currently used 
df['DatabaseHaveWorkedWith'] =(
                                df['DatabaseHaveWorkedWith']
                               .astype(str)
                               .str.replace(r"[\[\],]", "" , regex=True)
                               .str.split(";")
                            )

dbww_count = df.explode('DatabaseHaveWorkedWith')
dbww_count['DatabaseHaveWorkedWith'] = dbww_count['DatabaseHaveWorkedWith'].str.strip()

dbww_count = dbww_count['DatabaseHaveWorkedWith'].value_counts().head(5)
dbww_count.plot( kind='bar' , figsize= (10,7), color=('yellow'))

plt.title('Top 5 Databases worked with')
plt.xlabel('Database')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# top 5 want to use in future

df['DatabaseWantToWorkWith'] =(
                                df['DatabaseWantToWorkWith']
                               .astype(str)
                               .str.replace(r"[\[\],]", "" , regex=True)
                               .str.split(";")
                            )

db_count = df.explode('DatabaseWantToWorkWith')
db_count['DatabaseWantToWorkWith'] = db_count['DatabaseWantToWorkWith'].str.strip()

db_count = db_count['DatabaseWantToWorkWith'].value_counts().head(5)
db_count.plot(kind='bar', figsize=(10,7), color='red')

plt.title('Top 5 Databases desrired')
plt.xlabel('Database')
plt.ylabel('Count')
plt.xticks(rotation= 45, ha= 'right')
plt.tight_layout()
plt.show()


       ### LANGUAGES ###

# top 5 currently used 

df['LanguageHaveWorkedWith'] = df['LanguageHaveWorkedWith'].astype(str).str.split(';')

countTable = df.explode('LanguageHaveWorkedWith') # explode lists into seperate rows
countTable['LanguageHaveWorkedWith'] = countTable['LanguageHaveWorkedWith'].str.strip() # remove white space

language_counts = countTable['LanguageHaveWorkedWith'].head(5).value_counts()
language_counts.plot(kind="bar", figsize=(10,7) , color="skyblue")

plt.title("Popular language worked with ")
plt.xlabel('Language')
plt.ylabel('Count')
plt.xticks(rotation= 45, ha='right')
plt.tight_layout()
plt.show()

# top 5 want to use in future
df['LanguageWantToWorkWith'] = df['LanguageWantToWorkWith'].str.split(';')

countTable = df.explode('LanguageWantToWorkWith')
countTable['LanguageWantToWorkWith'] = countTable['LanguageWantToWorkWith'].str.strip()

lang_count = countTable['LanguageWantToWorkWith'].head(5).value_counts()
lang_count.plot(kind="bar" , figsize=(10,7), color="red")

plt.title("Popular language desired")
plt.xlabel('Lanuage')
plt.ylabel('Count')
plt.xticks(rotation= 45, ha='right')
plt.tight_layout()
plt.show()



                # 2. How have the usage trends of the top 5 databases and programming languages 
                # changed over three years?


       ### Databases ###
# top 5 currently used 
dbww = df.explode('DatabaseHaveWorkedWith')
dbww['DatabaseHaveWorkedWith'] = dbww['DatabaseHaveWorkedWith'].astype(str).str.strip()

dbww_top5_set = dbww['DatabaseHaveWorkedWith'].value_counts().head(5).index.tolist()

dbww_top5 = dbww[dbww['DatabaseHaveWorkedWith'].isin(dbww_top5_set)]
dbww_graph = pd.crosstab(dbww_top5['DatabaseHaveWorkedWith'], dbww_top5['Year'].astype(str))

dbww_graph.plot( kind='bar' , figsize= (10,7))

plt.title('Top 5 Databases worked with')
plt.xlabel('Database')
plt.ylabel('Count')
plt.xticks(rotation= 45, ha='right')
plt.tight_layout()
plt.show()


# In 2021, MySQL was the most used database with over 10,000 users. 
# In 2022, PostgreSQL took the lead with nearly 10,000 users. 
# By 2023, PostgreSQL remained the top choice, rising to over 17,500 users — 
# a clear increase across all three years.
# Otherwise in all top5 categories , the number users decreased from the year 2021 to the year 2022 , then drastically increased in the year 2023


       ### Languages ###
lww = df.explode('LanguageHaveWorkedWith')
lww['LanguageHaveWorkedWith'] = lww['LanguageHaveWorkedWith'].astype(str).str.strip()

lww_top5_set = lww['LanguageHaveWorkedWith'].value_counts().head(5).index.tolist()

lww_top5 = lww[lww['LanguageHaveWorkedWith'].isin(lww_top5_set)]
lww_graph = pd.crosstab(lww_top5['LanguageHaveWorkedWith'], lww_top5['Year'].astype(str))


lww_graph.plot( kind='bar' , figsize= (10,7))

plt.title('Top 5 Languages worked with')
plt.xlabel('Language')
plt.ylabel('Count')
plt.xticks(rotation= 45, ha='right')
plt.tight_layout()
plt.show()


#    3. Relationship Analysis

                # 1. How does YearsCode correlate with the use of the top 5 databases and programming languages currently in use?
                # Focus on clarity, relevance, and insightful analysis in your visualizations and interpretations

# YearsCode x Languages 

yclang_graph = pd.crosstab(dbww_top5['DatabaseHaveWorkedWith'],dbww_top5['YearsCodeGroup'])

yclang_graph.plot( kind='bar', figsize= (10,7))

plt.title('Correlation of Yearscode with Programming languages used')
plt.xlabel('Language')
plt.ylabel('Years Code')
plt.xticks(rotation= 45, ha= 'right')
plt.tight_layout()
plt.show()



#  2.2. Based on your above analysis, provide a short report detailing your findings / insights derived from the data that may be useful to GitHub to better understand their users.
#  Additionally, provide recommendations on
# improvements or ideas to maintain their current users and attract new ones. Ensure that your findings are relevant based on your analysis and visualizations, and that they are articulated well. Your recommendations should be
# innovative, detailed and actionable

"""
        # 1. Developer Roles & Demographics

            Over the three years, there has been a steady increase in the number of Professional Developers, rising from under 20,000 to over 30,000 users.

            The Student category showed a decline, suggesting either a transition into professional roles or reduced student participation.

            Most users fall within the 25–34 age range, especially in the Professional Developer category, highlighting a strong early-career demographic.

            The Professional Developer group is dominant across all countries surveyed, with Italy standing out with the highest number of professionals.

            Education-wise, users with a Bachelor’s Degree form the largest group (~30,000), followed by Master’s Degree holders and those with Tertiary Education.

            Most developers have 0–9 or 10–19 years of experience, indicating a solid mix of early-career and mid-level professionals.


        # 2. Technology Trends

            PostgreSQL has gained massive traction, overtaking MySQL as the most used database by 2023, with usage rising from under 10,000 in 2022 to over 17,500 in 2023.

            Despite fluctuations, PostgreSQL’s upward trend makes it a standout.

            For programming languages, the top 5 remain consistent, though exact rankings vary. User interest dipped in 2022 before rising again in 2023 across both languages and databases.


        # 3. Experience & Technology Use

            Most developers using top databases (e.g., PostgreSQL, MySQL) fall into the 0–19 years of coding experience range.

            This suggests newer generations are influencing tech stacks, especially in favor of open-source and flexible tools.
"""


"""
    Recommendations
            Create More Support for Early-Career Developers
            Since most users fall into the 0–9 and 10–19 years of coding experience range, GitHub could offer more beginner-friendly resources. This includes curated learning paths, 
            starter project templates, and beginner-focused community challenges that help newer developers build confidence and real-world skills.

            Re-engage the Student Community
            With a drop in student users over the years, it might help to introduce more attractive student perks. GitHub could partner with schools and tech societies to offer exclusive content
            , events, or internship pipelines that make staying on GitHub as a student more beneficial.

            Double Down on PostgreSQL Support
            PostgreSQL has clearly gained popularity—especially in 2023. GitHub can build on this by highlighting PostgreSQL in workflows, offering sample projects
            , and supporting integrations that make it easier for developers to use PostgreSQL in their repositories and deployments.
"""


