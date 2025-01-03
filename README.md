#  Linking Financial Mindsets to National Income and Democratic Health: A Clustering Approach

## Project Overview
This project explores the relationship between financial mindsets and macroeconomic indicators such as income levels and democracy classifications using the World Bank's Findex database.

## Objectives
- To cluster countries based on financial attitudes and behaviors.
- To compare these clusters with World Bank income classifications and democracy indices.

## Repository Structure
- `Data/Processed`: Preprocessed datasets used for further analysis.
- `Notebooks/`: Jupyter notebooks for each analysis step.
- `Src/`: Python scripts for data preprocessing and analysis helpers.
- `Results/`: Generated figures, tables, and final cluster assignments.

## Data Sources
- [World Bank Global Financial Inclusion Database](https://databank.worldbank.org/source/global-financial-inclusion)
- [World Bank Income Classification](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups)
- [Democracy Index](https://www.eiu.com/topic/democracy-index)

## Data Setup
1. Download the World Bank data from the Global Financial Inclusion Database. The specific variables and their division into files utilized in this project are listed below.
2. Place the downloaded files in the "Data/" directory.

## Data Description

### Processed Data

### Data Processing

The raw data was cleaned and processed as follows:
1. Eliminated rows that lacked a country name or a series code.
2. Ordered the data to cluster related series together.
3. Transformed the data by indexing it with country names. The columns represent series codes, and the values correspond to the most recent survey wave for each series.
4. Removed all rows (excluded all countries) with no data available.
5. Removed all columns that had more than 50% missing values. This step excluded data related to rural/urban stratification.

### Global Financial Inclusion Database (Global Findex Database)

The Global Findex database provides comprehensive data on financial attitudes and behaviours across countries.

For this project, the following variables were utilized:
worried_data.csv

| Series Code                | Series Name                                                    |
|------------------------------|----------------------------------------------------------------|
| fin44b3.d | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all (% age 15+) |
| fin44b3.d.1 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, female (% age 15+) |
| fin44b3.d.12 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, in labor force (% age 15+) |
| fin44b3.d.7 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, income, poorest 40% (% ages 15+) |
| fin44b3.d.8 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, income, richest 60% (% ages 15+) |
| fin44b3.d.2 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, male (% age 15+) |
| fin44b3.d.4 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, older (% age 25+) |
| fin44b3.d.11 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, out of labor force (% age 15+) |
| fin44b3.d.5 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, primary education or less (% ages 15+) |
| fin44b3.d.9 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, rural (% age 15+) |
| fin44b3.d.6 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, secondary education or more (% ages 15+) |
| fin44b3.d.10 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, urban (% age 15+) |
| fin44b3.d.3 | Worried about not being able to pay for medical costs in case of a serious illness or accident: not worried at all, young (% ages 15-24) |
| fin44b2.d | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried (% age 15+) |
| fin44b2.d.1 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, female (% age 15+) |
| fin44b2.d.12 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, in labor force (% age 15+) |
| fin44b2.d.7 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, income, poorest 40% (% ages 15+) |
| fin44b2.d.8 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, income, richest 60% (% ages 15+) |
| fin44b2.d.2 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, male (% age 15+) |
| fin44b2.d.4 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, older (% age 25+) |
| fin44b2.d.11 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, out of labor force (% age 15+) |
| fin44b2.d.5 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, primary education or less (% ages 15+) |
| fin44b2.d.9 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, rural (% age 15+) |
| fin44b2.d.6 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, secondary education or more (% ages 15+) |
| fin44b2.d.10 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, urban (% age 15+) |
| fin44b2.d.3 | Worried about not being able to pay for medical costs in case of a serious illness or accident: somewhat worried, young (% ages 15-24) |
| fin44b1.d | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried (% age 15+) |
| fin44b1.d.1 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, female (% age 15+) |
| fin44b1.d.12 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, in labor force (% age 15+) |
| fin44b1.d.7 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, income, poorest 40% (% ages 15+) |
| fin44b1.d.8 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, income, richest 60% (% ages 15+) |
| fin44b1.d.2 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, male (% age 15+) |
| fin44b1.d.4 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, older (% age 25+) |
| fin44b1.d.11 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, out of labor force (% age 15+) |
| fin44b1.d.5 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, primary education or less (% ages 15+) |
| fin44b1.d.9 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, rural (% age 15+) |
| fin44b1.d.6 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, secondary education or more (% ages 15+) |
| fin44b1.d.10 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, urban (% age 15+) |
| fin44b1.d.3 | Worried about not being able to pay for medical costs in case of a serious illness or accident: very worried, young (% ages 15-24) |
| fin44d3.d | Worried about not being able to pay school fees or fees for education: not worried at all (% age 15+) |
| fin44d3.d.1 | Worried about not being able to pay school fees or fees for education: not worried at all, female (% age 15+) |
| fin44d3.d.12 | Worried about not being able to pay school fees or fees for education: not worried at all, in labor force (% age 15+) |
| fin44d3.d.7 | Worried about not being able to pay school fees or fees for education: not worried at all, income, poorest 40% (% ages 15+) |
| fin44d3.d.8 | Worried about not being able to pay school fees or fees for education: not worried at all, income, richest 60% (% ages 15+) |
| fin44d3.d.2 | Worried about not being able to pay school fees or fees for education: not worried at all, male (% age 15+) |
| fin44d3.d.4 | Worried about not being able to pay school fees or fees for education: not worried at all, older (% age 25+) |
| fin44d3.d.11 | Worried about not being able to pay school fees or fees for education: not worried at all, out of labor force (% age 15+) |
| fin44d3.d.5 | Worried about not being able to pay school fees or fees for education: not worried at all, primary education or less (% ages 15+) |
| fin44d3.d.9 | Worried about not being able to pay school fees or fees for education: not worried at all, rural (% age 15+) |
| fin44d3.d.6 | Worried about not being able to pay school fees or fees for education: not worried at all, secondary education or more (% ages 15+) |
| fin44d3.d.10 | Worried about not being able to pay school fees or fees for education: not worried at all, urban (% age 15+) |
| fin44d3.d.3 | Worried about not being able to pay school fees or fees for education: not worried at all, young (% ages 15-24) |
| fin44d2.d | Worried about not being able to pay school fees or fees for education: somewhat worried (% age 15+) |
| fin44d2.d.1 | Worried about not being able to pay school fees or fees for education: somewhat worried, female (% age 15+) |
| fin44d2.d.12 | Worried about not being able to pay school fees or fees for education: somewhat worried, in labor force (% age 15+) |
| fin44d2.d.7 | Worried about not being able to pay school fees or fees for education: somewhat worried, income, poorest 40% (% ages 15+) |
| fin44d2.d.8 | Worried about not being able to pay school fees or fees for education: somewhat worried, income, richest 60% (% ages 15+) |
| fin44d2.d.2 | Worried about not being able to pay school fees or fees for education: somewhat worried, male (% age 15+) |
| fin44d2.d.4 | Worried about not being able to pay school fees or fees for education: somewhat worried, older (% age 25+) |
| fin44d2.d.11 | Worried about not being able to pay school fees or fees for education: somewhat worried, out of labor force (% age 15+) |
| fin44d2.d.5 | Worried about not being able to pay school fees or fees for education: somewhat worried, primary education or less (% ages 15+) |
| fin44d2.d.9 | Worried about not being able to pay school fees or fees for education: somewhat worried, rural (% age 15+) |
| fin44d2.d.6 | Worried about not being able to pay school fees or fees for education: somewhat worried, secondary education or more (% ages 15+) |
| fin44d2.d.10 | Worried about not being able to pay school fees or fees for education: somewhat worried, urban (% age 15+) |
| fin44d2.d.3 | Worried about not being able to pay school fees or fees for education: somewhat worried, young (% ages 15-24) |
| fin44d1.d | Worried about not being able to pay school fees or fees for education: very worried (% age 15+) |
| fin44d1.d.1 | Worried about not being able to pay school fees or fees for education: very worried, female (% age 15+) |
| fin44d1.d.12 | Worried about not being able to pay school fees or fees for education: very worried, in labor force (% age 15+) |
| fin44d1.d.7 | Worried about not being able to pay school fees or fees for education: very worried, income, poorest 40% (% ages 15+) |
| fin44d1.d.8 | Worried about not being able to pay school fees or fees for education: very worried, income, richest 60% (% ages 15+) |
| fin44d1.d.2 | Worried about not being able to pay school fees or fees for education: very worried, male (% age 15+) |
| fin44d1.d.4 | Worried about not being able to pay school fees or fees for education: very worried, older (% age 25+) |
| fin44d1.d.11 | Worried about not being able to pay school fees or fees for education: very worried, out of labor force (% age 15+) |
| fin44d1.d.5 | Worried about not being able to pay school fees or fees for education: very worried, primary education or less (% ages 15+) |
| fin44d1.d.9 | Worried about not being able to pay school fees or fees for education: very worried, rural (% age 15+) |
| fin44d1.d.6 | Worried about not being able to pay school fees or fees for education: very worried, secondary education or more (% ages 15+) |
| fin44d1.d.10 | Worried about not being able to pay school fees or fees for education: very worried, urban (% age 15+) |
| fin44d1.d.3 | Worried about not being able to pay school fees or fees for education: very worried, young (% ages 15-24) |
| fin44c3.d | Worried about not having enough money for monthly expenses or bills: not worried at all (% age 15+) |
| fin44c3.d.1 | Worried about not having enough money for monthly expenses or bills: not worried at all, female (% age 15+) |
| fin44c3.d.12 | Worried about not having enough money for monthly expenses or bills: not worried at all, in labor force (% age 15+) |
| fin44c3.d.7 | Worried about not having enough money for monthly expenses or bills: not worried at all, income, poorest 40% (% ages 15+) |
| fin44c3.d.8 | Worried about not having enough money for monthly expenses or bills: not worried at all, income, richest 60% (% ages 15+) |
| fin44c3.d.2 | Worried about not having enough money for monthly expenses or bills: not worried at all, male (% age 15+) |
| fin44c3.d.4 | Worried about not having enough money for monthly expenses or bills: not worried at all, older (% age 25+) |
| fin44c3.d.11 | Worried about not having enough money for monthly expenses or bills: not worried at all, out of labor force (% age 15+) |
| fin44c3.d.5 | Worried about not having enough money for monthly expenses or bills: not worried at all, primary education or less (% ages 15+) |
| fin44c3.d.9 | Worried about not having enough money for monthly expenses or bills: not worried at all, rural (% age 15+) |
| fin44c3.d.10 | Worried about not having enough money for monthly expenses or bills: not worried at all, urban (% age 15+) |
| fin44c3.d.3 | Worried about not having enough money for monthly expenses or bills: not worried at all, young (% ages 15-24) |
| fin44c2.d | Worried about not having enough money for monthly expenses or bills: somewhat worried (% age 15+) |
| fin44c2.d.1 | Worried about not having enough money for monthly expenses or bills: somewhat worried, female (% age 15+) |
| fin44c2.d.12 | Worried about not having enough money for monthly expenses or bills: somewhat worried, in labor force (% age 15+) |
| fin44c2.d.7 | Worried about not having enough money for monthly expenses or bills: somewhat worried, income, poorest 40% (% ages 15+) |
| fin44c2.d.8 | Worried about not having enough money for monthly expenses or bills: somewhat worried, income, richest 60% (% ages 15+) |
| fin44c2.d.2 | Worried about not having enough money for monthly expenses or bills: somewhat worried, male (% age 15+) |
| fin44c2.d.4 | Worried about not having enough money for monthly expenses or bills: somewhat worried, older (% age 25+) |
| fin44c2.d.11 | Worried about not having enough money for monthly expenses or bills: somewhat worried, out of labor force (% age 15+) |
| fin44c2.d.5 | Worried about not having enough money for monthly expenses or bills: somewhat worried, primary education or less (% ages 15+) |
| fin44c2.d.9 | Worried about not having enough money for monthly expenses or bills: somewhat worried, rural (% age 15+) |
| fin44c2.d.6 | Worried about not having enough money for monthly expenses or bills: somewhat worried, secondary education or more (% ages 15+) |
| fin44c2.d.10 | Worried about not having enough money for monthly expenses or bills: somewhat worried, urban (% age 15+) |
| fin44c2.d.3 | Worried about not having enough money for monthly expenses or bills: somewhat worried, young (% ages 15-24) |
| fin44c1.d | Worried about not having enough money for monthly expenses or bills: very worried (% age 15+) |
| fin44c1.d.1 | Worried about not having enough money for monthly expenses or bills: very worried, female (% age 15+) |
| fin44c1.d.12 | Worried about not having enough money for monthly expenses or bills: very worried, in labor force (% age 15+) |
| fin44c1.d.7 | Worried about not having enough money for monthly expenses or bills: very worried, income, poorest 40% (% ages 15+) |
| fin44c1.d.8 | Worried about not having enough money for monthly expenses or bills: very worried, income, richest 60% (% ages 15+) |
| fin44c1.d.2 | Worried about not having enough money for monthly expenses or bills: very worried, male (% age 15+) |
| fin44c1.d.4 | Worried about not having enough money for monthly expenses or bills: very worried, older (% age 25+) |
| fin44c1.d.11 | Worried about not having enough money for monthly expenses or bills: very worried, out of labor force (% age 15+) |
| fin44c1.d.5 | Worried about not having enough money for monthly expenses or bills: very worried, primary education or less (% ages 15+) |
| fin44c1.d.9 | Worried about not having enough money for monthly expenses or bills: very worried, rural (% age 15+) |
| fin44c1.d.6 | Worried about not having enough money for monthly expenses or bills: very worried, secondary education or more (% ages 15+) |
| fin44c1.d.10 | Worried about not having enough money for monthly expenses or bills: very worried, urban (% age 15+) |
| fin44c1.d.3 | Worried about not having enough money for monthly expenses or bills: very worried, young (% ages 15-24) |
| fin44a3.d | Worried about not having enough money for old age: not worried at all (% age 15+) |
| fin44a3.d.1 | Worried about not having enough money for old age: not worried at all, female (% age 15+) |
| fin44a3.d.12 | Worried about not having enough money for old age: not worried at all, in labor force (% age 15+) |
| fin44a3.d.7 | Worried about not having enough money for old age: not worried at all, income, poorest 40% (% ages 15+) |
| fin44a3.d.8 | Worried about not having enough money for old age: not worried at all, income, richest 60% (% ages 15+) |
| fin44a3.d.2 | Worried about not having enough money for old age: not worried at all, male (% age 15+) |
| fin44a3.d.4 | Worried about not having enough money for old age: not worried at all, older (% age 25+) |
| fin44a3.d.11 | Worried about not having enough money for old age: not worried at all, out of labor force (% age 15+) |
| fin44a3.d.5 | Worried about not having enough money for old age: not worried at all, primary education or less (% ages 15+) |
| fin44a3.d.9 | Worried about not having enough money for old age: not worried at all, rural (% age 15+) |
| fin44a3.d.6 | Worried about not having enough money for old age: not worried at all, secondary education or more (% ages 15+) |
| fin44a3.d.10 | Worried about not having enough money for old age: not worried at all, urban (% age 15+) |
| fin44a3.d.3 | Worried about not having enough money for old age: not worried at all, young (% ages 15-24) |
| fin44a2.d | Worried about not having enough money for old age: somewhat worried (% age 15+) |
| fin44a2.d.1 | Worried about not having enough money for old age: somewhat worried, female (% age 15+) |
| fin44a2.d.12 | Worried about not having enough money for old age: somewhat worried, in labor force (% age 15+) |
| fin44a2.d.7 | Worried about not having enough money for old age: somewhat worried, income, poorest 40% (% ages 15+) |
| fin44a2.d.8 | Worried about not having enough money for old age: somewhat worried, income, richest 60% (% ages 15+) |
| fin44a2.d.2 | Worried about not having enough money for old age: somewhat worried, male (% age 15+) |
| fin44a2.d.4 | Worried about not having enough money for old age: somewhat worried, older (% age 25+) |
| fin44a2.d.11 | Worried about not having enough money for old age: somewhat worried, out of labor force (% age 15+) |
| fin44a2.d.5 | Worried about not having enough money for old age: somewhat worried, primary education or less (% ages 15+) |
| fin44a2.d.9 | Worried about not having enough money for old age: somewhat worried, rural (% age 15+) |
| fin44a2.d.6 | Worried about not having enough money for old age: somewhat worried, secondary education or more (% ages 15+) |
| fin44a2.d.10 | Worried about not having enough money for old age: somewhat worried, urban (% age 15+) |
| fin44a2.d.3 | Worried about not having enough money for old age: somewhat worried, young (% ages 15-24) |
| fin44a1.d | Worried about not having enough money for old age: very worried (% age 15+) |
| fin44a1.d.1 | Worried about not having enough money for old age: very worried, female (% age 15+) |
| fin44a1.d.12 | Worried about not having enough money for old age: very worried, in labor force (% age 15+) |
| fin44a1.d.7 | Worried about not having enough money for old age: very worried, income, poorest 40% (% ages 15+) |
| fin44a1.d.8 | Worried about not having enough money for old age: very worried, income, richest 60% (% ages 15+) |
| fin44a1.d.2 | Worried about not having enough money for old age: very worried, male (% age 15+) |
| fin44a1.d.4 | Worried about not having enough money for old age: very worried, older (% age 25+) |
| fin44a1.d.11 | Worried about not having enough money for old age: very worried, out of labor force (% age 15+) |
| fin44a1.d.5 | Worried about not having enough money for old age: very worried, primary education or less (% ages 15+) |
| fin44a1.d.9 | Worried about not having enough money for old age: very worried, rural (% age 15+) |
| fin44a1.d.6 | Worried about not having enough money for old age: very worried, secondary education or more (% ages 15+) |
| fin44a1.d.10 | Worried about not having enough money for old age: very worried, urban (% age 15+) |
| fin44a1.d.3 | Worried about not having enough money for old age: very worried, young (% ages 15-24) |

