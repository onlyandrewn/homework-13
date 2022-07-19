#!/usr/bin/env python
# coding: utf-8

# # Parsing PDFs Homework
# 
# With the power of pdfminer, pytesseract, Camelot, and Tika, let's analyze some documents!
# 
# > If at any point you think, **"I'm close enough, I'd just edit the rest of it in Excel"**: that's fine! Just make a note of it.
# 
# ## A trick to use again and again
# 
# ### Approach 1
# 
# Before we get started: when you want to take the first row of your data and set it as the header, use this trick.

# In[1]:


import pandas as pd


# In[2]:


df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[3]:


# Set the first column as the columns
df.columns = df.loc[0]

# Drop the first row
df = df.drop(0)

df


# 🚀 Done!
# 
# ### Approach 2
# 
# Another alternative is to use `.rename` on your columns and just filter out the columns you aren't interested in. This can be useful if the column name shows up multiple times in your data for some reason or another.

# In[4]:


# Starting with the same-ish data...
df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'fruit name', 'likes' ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[5]:


df = df.rename(columns={
    0: 'fruit name',
    1: 'likes'
})
df = df[df['fruit name'] != 'fruit name']
df


# 🚀 Done!
# 
# ### Useful tips about coordinates
# 
# If you want to grab only a section of the page [Kull](https://jsoma.github.io/kull/#/) might be helpful in finding the coordinates.
# 
# > **Alternatively** run `%matplotlib notebook` in a cell. Afterwards, every time you use something like `camelot.plot(tables[0]).show()` it will get you nice zoomable, hoverable versions that include `x` and `y` coordinates as you move your mouse.
# 
# Coordinates are given as `"left_x,top_y,right_x,bottom_y"` with `(0,0)` being in the bottom left-hand corner.
# 
# Note that all coordinates are strings, for some reason. It won't be `[1, 2, 3, 4]` it will be `['1,2,3,4']`
# 
# # Camelot questions
# 
# The largest part of this assignment is **mostly Camelot work**. As tabular data is usually the most typical data you'll be working with, it's what I'm giving you!
# 
# It will probably be helpful to read through [Camelot's advanced usage tips](https://camelot-py.readthedocs.io/en/master/user/advanced.html), along with the notebook I posted in the homework assignment.
# 
# ## Prison Inmates
# 
# Working from [InmateList.pdf](InmateList.pdf), save a CSV file that includes every inmate.
# 
# * Make sure your rows are *all data*, and you don't have any people named "Inmate Name."
# 

# In[6]:


import requests
from bs4 import BeautifulSoup


# In[7]:


# !pip install "camelot-py[base]"


# In[8]:


import camelot


# In[9]:


# !pip install opencv-python


# In[268]:


tables = camelot.read_pdf("InmateList.pdf", flavor="stream", pages="all")

for table in tables:    
    if table.df.shape[0] == 47:
        table.df = table.df \
            .drop([0, 1, 2, 46])
        
        if table.df.shape[1] == 6:
            table.df = table.df \
                .drop([2, 5], axis=1) \
                .rename(columns={
                    0: "ICN #",
                    1: "Inmate Name",
                    3: "Facility",
                    4: "Booking Date"
                })
        elif table.df.shape[1] == 5:
            table.df = table.df \
                .drop([4], axis=1) \
                .rename(columns={
                    0: "ICN #",
                    1: "Inmate Name",
                    2: "Facility",
                    3: "Booking Date"
                })

    if table.df.shape[0] == 42:
        table.df = table.df \
            .drop([0, 1, 2]) \
            .rename(columns={
                0: "ICN #",
                1: "Inmate Name",
                2: "Facility",
                3: "Booking Date"
            })


# In[270]:


dfs = [table.df for table in tables]

combined_dfs = pd.concat(dfs, ignore_index=True)
combined_dfs.to_csv("combined.csv", index=False)


# ## WHO resolutions
# 
# Using [A74_R13-en.pdf](A74_R13-en.pdf), what ten member countries are given the highest assessments?
# 
# * You might need to have two separate queries, and combine the results: that last page is pretty awful!
# * Always rename your columns
# * Double-check that your sorting looks right......
# * You can still get the answer even without perfectly clean data

# In[272]:


tables = camelot.read_pdf("A74_R13-en.pdf", flavor="stream", pages="all")

tables[5].df = tables[5].df \
    .drop([0, 1, 2, 3, 6, 7, 8, 9]) \
    .drop([0, 2, 4], axis=1) \
    .rename(columns={
        1: "Members and Associate Members",
        3: "WHO scale for 2022–2023 %"
    })

for table in tables[:5]:
    table.df = table.df \
        .drop([0, 1, 2]) \
        .rename(columns={
            0: "Members and Associate Members",
            1: "WHO scale for 2022–2023 %"
        })


# In[273]:


dfs_who = [table.df for table in tables]
combined_dfs = pd.concat(dfs_who, ignore_index=True)
combined_dfs.to_csv("combined_who.csv")


# In[281]:


combined_dfs.dtypes


# In[282]:


combined_dfs.sort_values(by="WHO scale for 2022–2023 %", ascending=False).head(10)


# ## The Avengers
# 
# Using [THE_AVENGERS.pdf](THE_AVENGERS.pdf), approximately how many lines does Captain America have as compared to Thor and Iron Man?
# 
# * Character names only: we're only counting `IRON MAN` as Iron Man, not `TONY`.
# * Your new best friend might be `\n`
# * Look up `.count` for strings

# In[285]:


from pdfminer.high_level import extract_text


# In[286]:


text = extract_text("THE_AVENGERS.pdf")


# In[287]:


text[:1000]


# In[307]:


print(text.count("IRON MAN"))
print(text.count("THOR"))
print(text.count("CAPTAIN AMERICA"))


# ## COVID data
# 
# Using [covidweekly2721.pdf](covidweekly2721.pdf), what's the total number of tests performed in Minnesota? Use the Laboratory Test Rates by County of Residence chart.
# 
# * You COULD pull both tables separately OR you could pull them both at once and split them in pandas.
# * Remember you can do things like `df[['name','age']]` to ask for multiple columns

# In[340]:


tables = camelot.read_pdf("covidweekly2721.pdf", flavor="stream", pages="6")

tables[0].df = tables[0].df \
    .drop([0, 1, 2, 3, 4, 6, 7, 12, 52, 53]) \
    .drop(0, axis=1)

table_1 = tables[0].df[[1, 2, 3]] \
    .rename(columns={
        1: "County",
        2: "Number of Tests",
        3: "Cumulative Rate"
    })

table_2 = tables[0].df[[4, 5, 6]] \
    .rename(columns={
        4: "County",
        5: "Number of Tests",
        6: "Cumulative Rate"
    })


table_1.iloc[4, table_1.columns.get_loc('Cumulative Rate')] = "19,574"

merged = pd.concat([table_1, table_2], ignore_index=True)
merged


# ## Theme Parks
# 
# Using [2019-Theme-Index-web-1.pdf](2019-Theme-Index-web-1.pdf), save a CSV of the top 10 theme park groups worldwide.
# 
# * You can clean the results or you can restrict the area the table is pulled from, up to you

# In[366]:


tables = camelot.read_pdf("2019-Theme-Index-web-1.pdf", flavor="stream", pages="11")

tables[0].df = tables[0].df \
    .drop([10, 11]) \
    .rename(columns={
        0: "Rank",
        1: "Group Name",
        2: "% Change",
        3: "Attendance 2019",
        4: "Attendance 2018"
    })

tables[0].df.loc[0, "Rank": "Attendance 2018"] = ["1", "WALT DISNEY ATTRACTIONS", "0.8%", "155,991,000", "157,311,000"]


# ## Hunting licenses
# 
# Using [US_Fish_and_Wildlife_Service_2021.pdf](US_Fish_and_Wildlife_Service_2021.pdf) and [a CSV of state populations](http://goodcsv.com/geography/us-states-territories/), find the states with the highest per-capita hunting license holders.

# In[370]:


tables = camelot.read_pdf("US_Fish_and_Wildlife_Service_2021.pdf")

tables[0].df \
    .drop([0, 57]) \
    .rename(columns={
        0: "State",
        1: "Paid Hunting License Holders",
        2: "Resident Hunting Licenses, Tags, Permits and Stamps",
        3: "Non-Resident Hunting Licenses, Tags, Permits and Stamps",
        4: "Total Hunting License, Tags,Permits & Stamps",
        5: "Cost - Resident Hunting Licenses, Tags, Permits and Stamps",
        6: "Cost - Non-Resident Hunting Licenses, Tags, Permits and Stamps",
        7: "Gross Cost - Hunting Licenses"
    })


# In[399]:


df = pd.read_csv("us-states-territories.csv", encoding_errors="ignore")

df = df.rename(columns={
    "Abbreviation": "State"
})

df

# MERGE DATAFRAMES TOGETHER BASED ON COMMON COLUMN
# merged = df.merge(tables[0].df, left_on="State", right_on="Population (2019)")
# merged


# In[ ]:


# merged["Per capita"] = merged["Paid Hunting License Holders"] / merged["Population (2019)"]


# # Not-Camelot questions
# 
# You can answer these without using Camelot.

# ## Federal rules on assault weapons
# 
# Download all of the PDFs from the Bureau of Alcohol, Tobacco, Firearms and Explosives's [Rules and Regulations Library](https://www.atf.gov/rules-and-regulations/rules-and-regulations-library). Filter for a list of all PDFs that contain the word `assault weapon` or `assault rifle`.
# 
# > If you're having trouble scraping, maybe someone will be kind enough to drop a list of PDF urls in Slack?

# In[21]:


import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[390]:


response = requests.get("https://www.atf.gov/rules-and-regulations/rules-and-regulations-library")
doc = BeautifulSoup(response.text)
doc


# In[401]:


pdfs = []

table = doc.select("table tr", class_="views-table cols-4")
base_url = "https://www.atf.gov"

for row in table[1:]:
    if row.a != None:
        url = base_url + row.a.get("href")
        
        pdfs.append(url)
        
print(pdfs)


# In[402]:


file_content = '\n'.join(pdfs)

with open("pdfs.txt", "w") as f:
    f.write(file_content)


# In[404]:


get_ipython().system('wget -i pdfs.txt')


# In[ ]:


# for pdf in pdfs:
#     pdf.find("assault weapon")
# pdf.find("assault rifle")

# pdfs.find("assault weapon")
# # FILTER PDFS FOR ASSAULT WEAPON OR ASSAULT RIFLE


# ## New immigration judge training materials
# 
# Extract the text from [this 2020 guide for new immigration judges](2020-training-materials-2a-201-300.pdf) and save it as a file called `training-material.txt`.
# 
# > I took this PDF from [a FOIA request](https://www.muckrock.com/foi/united-states-of-america-10/most-recent-new-immigration-judge-training-materials-120125/#comms) – but the unfortunate thing is *I actually had to remove the OCR layer to make it part of this assignment*. By default everything that goes through Muckrock gets all of the text detected!

# In[24]:


get_ipython().system('pip install pytesseract')


# In[25]:


# !pip install Pillow
# !pip install pytesseract
# !pip install pdf2image


# In[26]:


from PIL import Image
import pytesseract
from pdf2image import convert_from_path


# In[27]:


# https://www.gcptutorials.com/post/python-extract-text-from-pdf-files
# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052

# poppler_path = ""
# pdf_path = "2020-training-materials-2a-201-300.pdf"

# images = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)

# for count, img in enumerate(images):
#   img_name = f"page_{count}.png"  
#   img.save(img_name, "PNG")

# text = pytesseract.image_to_string('TKTK')
# print(text)


# In[28]:


# with open(writePath, 'a') as f:
#     dfAsString = df.to_string(header=False, index=False)
#     f.write(dfAsString)

# df.to_string('training-material.txt', index = False)
# f = open("training-material.txt",'w')  # write in text mode

