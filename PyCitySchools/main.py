#!/usr/bin/env python
# coding: utf-8


# Dependencies and Setup
import pandas as pd
import numpy as np
from IPython.display import display

# File to Load (Remember to Change These)
schoolDataToLoad = "Resources/schools_complete.csv"
studentDataToLoad = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
schoolData = pd.read_csv(schoolDataToLoad)
studentData = pd.read_csv(studentDataToLoad)
# Combine the data into a single dataset
schoolDataComplete = pd.merge(studentData, schoolData, how="left", on=["school_name", "school_name"])

def summarize_district(schoolDataComplete, schoolData, studentData):
# TODO: improve this code like with schools summary
    totalSchools = schoolData.shape[0]
    totalStudents = studentData.shape[0]
    totalBudget = schoolData['budget'].sum()
    totalMathPass = dict((studentData["math_score"]>70).value_counts())[True]
    totalReadingPass = dict((studentData["reading_score"]>70).value_counts())[True]
    averageMathScore = studentData['math_score'].mean()
    averageReadingScore = studentData['reading_score'].mean()
    percentMathPass = round(totalMathPass/totalStudents*100, 2)
    percentReadingPass = round(totalReadingPass/totalStudents*100, 2)

    districtSummary = pd.DataFrame(
        {'Total Schools' : [totalSchools],
        'Total Students' : [totalStudents],
        'Total Budget' : [totalBudget],
        'Per Student Budget' : [round(totalBudget/totalStudents, 2)],
        'Average Math Score' : [round(averageMathScore, 2)],
        'Average Reading Score': [round(averageReadingScore,2)],
        '% Students Pass Math' : [percentMathPass],
        '% Students Pass Reading' : [percentReadingPass],
        'Average Pass Rate' : [(percentMathPass+percentReadingPass)/2]})

    return districtSummary

def summarize_schools(schoolDataComplete, schoolData, studentData):
    schools = []
    for highSchool in schoolData['school_name']:
        thisSchoolTable = schoolDataComplete[schoolDataComplete['school_name'] == highSchool]
        _, _, _, _, schoolName, _, _, id, type, students, budget = thisSchoolTable.iloc[0]
        percentMathPass = round(thisSchoolTable[thisSchoolTable['math_score']>70].shape[0]/students*100, 2)
        percentReadingPass = round(thisSchoolTable[thisSchoolTable['math_score']>70].shape[0]/students*100, 2)

        schools.append (
            {'School Name' : schoolName,
            'School Type' : type,
            'Total Students' : students,
            'Total School Budget' : budget,
            'Per Student Budget' : budget/students,
            'Average Math Score' : round(thisSchoolTable['math_score'].mean(), 2),
            'Average Reading Score' : round(thisSchoolTable['reading_score'].mean(), 2),
            '% Passing Math' : percentMathPass,
            '% Passing Reading' : percentReadingPass,
            'Overall Passing Rate': (percentMathPass + percentReadingPass)/2
            })
    schoolsSummary = pd.DataFrame (schools)
    schoolsSummary = schoolsSummary[['School Name', 'School Type', "Total Students", 'Total School Budget', 'Per Student Budget', 'Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]
    return schoolsSummary


districtSummary = summarize_district(schoolDataComplete, schoolData, studentData)
schoolsSummary = summarize_schools(schoolDataComplete, schoolData, studentData)

# Display only relevant columns
display(schoolsSummary [['Per Student Budget', 'Total Students', 'Overall Passing Rate']])
display(districtSummary [['Total Schools', 'Total Students', 'Per Student Budget', '% Students Pass Math', '% Students Pass Reading', 'Average Pass Rate']])

print ("--------------- Top 5 best performing schools -----------------------------------")
display(schoolsSummary.nlargest(5, 'Overall Passing Rate'))
print ("--------------- Bottom 5 worst performing schools -----------------------------------")
display(schoolsSummary.nsmallest(5, 'Overall Passing Rate'))

# spending_bins = [0, 585, 615, 645, 675]
# group_names = ["<$585", "$585-615", "$615-645", "$645-675"]
#
#
# size_bins = [0, 1000, 2000, 5000]
# group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
