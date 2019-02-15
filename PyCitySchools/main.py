#!/usr/bin/env python
# coding: utf-8

#TODO format money output to include $

# Dependencies and Setup
import pandas as pd
import numpy as np
from IPython.display import display

# File to Load (Remember to Change These)
schoolDataToLoad = "Resources/schools_complete.csv"
studentDataToLoad = "Resources/students_complete.csv"
pd.options.mode.chained_assignment = None  # default='warn'
# Read School and Student Data File and store into Pandas Data Frames
schoolData = pd.read_csv(schoolDataToLoad)
studentData = pd.read_csv(studentDataToLoad)
# Combine the data into a single dataset
schoolDataComplete = pd.merge(studentData, schoolData, how="left", on=["school_name", "school_name"])
schoolNames = schoolData["school_name"]

def summarizeDistrict(schoolDataComplete):
# TODO: improve this code like with schools summary
    totalSchools = len(schoolDataComplete['school_name'].unique())
    totalStudents = schoolDataComplete.shape[0]
    totalBudget = schoolData['budget'].sum()
    totalMathPass = dict((schoolDataComplete["math_score"]>=70).value_counts())[True]
    totalReadingPass = dict((schoolDataComplete["reading_score"]>=70).value_counts())[True]
    averageMathScore = schoolDataComplete['math_score'].mean()
    averageReadingScore = schoolDataComplete['reading_score'].mean()
    percentMathPass = totalMathPass/totalStudents*100
    percentReadingPass = totalReadingPass/totalStudents*100

    districtSummary = pd.DataFrame(
        {'Total Schools' : [totalSchools],
        'Total Students' : [totalStudents],
        'Total Budget' : ["${0:,.2f}".format(totalBudget)],
        'Per Student Budget' : ["${0:,.2f}".format(totalBudget/totalStudents)],
        'Average Math Score' : [averageMathScore],
        'Average Reading Score': [averageReadingScore],
        '% Students Pass Math' : [percentMathPass],
        '% Students Pass Reading' : [percentReadingPass],
        'Average Pass Rate' : [(percentMathPass+percentReadingPass)/2]})

    return districtSummary

def summarizeSchools(schoolDataComplete):
    schools = []
    for highSchool in schoolNames:
        thisSchoolTable = schoolDataComplete[schoolDataComplete['school_name'] == highSchool]
        _, _, _, _, schoolName, _, _, id, type, students, budget = thisSchoolTable.iloc[0]
        totalMathPass = dict((thisSchoolTable["math_score"]>=70).value_counts())[True]
        totalReadingPass = dict((thisSchoolTable["reading_score"]>=70).value_counts())[True]
        percentMathPass = totalMathPass/students*100
        percentReadingPass = totalReadingPass/students*100

        schools.append (
            {'School Name' : schoolName,
            'School Type' : type,
            'Total Students' : students,
            'Total School Budget' : "${0:,.2f}".format(budget),
            'Per Student Budget' : "${0:,.2f}".format(budget/students),
            'Average Math Score' : thisSchoolTable['math_score'].mean(),
            'Average Reading Score' : thisSchoolTable['reading_score'].mean(),
            '% Passing Math' : percentMathPass,
            '% Passing Reading' : percentReadingPass,
            'Overall Passing Rate': (percentMathPass + percentReadingPass)/2
            })
    schoolsSummary = pd.DataFrame (schools)
    schoolsSummary = schoolsSummary[['School Name', 'School Type', "Total Students", 'Total School Budget', 'Per Student Budget', 'Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]
    return schoolsSummary.round(6)

def summarizeScoresByGrade (schoolDataComplete, subject):
    # subject: "math" or "reading"
    subjectScore = subject+"_score"

    # a series per grade
    series9thGrade = schoolDataComplete.loc[schoolDataComplete["grade"]=="9th"]
    series10thGrade = schoolDataComplete.loc[schoolDataComplete["grade"]=="10th"]
    series11thGrade = schoolDataComplete.loc[schoolDataComplete["grade"]=="11th"]
    series12thGrade = schoolDataComplete.loc[schoolDataComplete["grade"]=="12th"]

    # group the series by school and calculate average
    series9thGradeBySchool = series9thGrade.groupby("school_name", as_index=False)[subjectScore].mean().round(6)
    series10thGradeBySchool = series10thGrade.groupby("school_name", as_index=False)[subjectScore].mean().round(6)
    series11thGradeBySchool = series11thGrade.groupby("school_name", as_index=False)[subjectScore].mean().round(6)
    series12thGradeBySchool = series12thGrade.groupby("school_name", as_index=False)[subjectScore].mean().round(6)

    # merge all series on school name
    allGradesBySchool = pd.merge(series9thGradeBySchool, series10thGradeBySchool, on="school_name").merge(series11thGradeBySchool, on="school_name").merge(series12thGradeBySchool, on="school_name")
    # rename columns
    allGradesBySchool.columns = ["School Name", "9th", "10th", "11th", "12th"]
    allGradesBySchool = allGradesBySchool.set_index('School Name')
    # remove index name row for cleaner output
    allGradesBySchool.index.name = None
    return (allGradesBySchool)

def sortNumSchools (by, howMany, order):
    # Top Performing schools
    if order == 'descending':
        sortedSchoolsSummary = schoolsSummary.sort_values([by], ascending=False)
    else:
        sortedSchoolsSummary = schoolsSummary.sort_values([by], ascending=True)
    sortedSchoolsSummary = sortedSchoolsSummary.set_index('School Name')
    sortedSchoolsSummary.index.name = None
    return sortedSchoolsSummary.head(howMany)

def summarizeScoresBySpendingBudget(schoolsSummary):

    bins=[0, 585, 615, 645, 675]
    binLabels = ["<$585", "\$585-\$615", "\$615-\$645", "\$645-\$675"]
    #convert per student budget back to float for binning
    spendingRanges = pd.cut(schoolsSummary["Per Student Budget"].replace("\$", "", regex=True).astype(float), bins, labels=binLabels)
    schoolPerfBySpendingRange = schoolsSummary[["School Name", "Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "Overall Passing Rate"]]
    schoolPerfBySpendingRange ["Spending Ranges (Per Student)"] = spendingRanges

    return (schoolPerfBySpendingRange.sort_values(by="Spending Ranges (Per Student)").groupby("Spending Ranges (Per Student)").mean().round(6))

def summarizeScoresBySchoolSize(schoolsSummary):
    bins = [0, 1000, 2000, 5000]
    binLabels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

    sizeRanges = pd.cut(schoolsSummary["Total Students"], bins, labels=binLabels)
    schoolPerfBySize = schoolsSummary[["School Name", "Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "Overall Passing Rate"]]
    schoolPerfBySize ["School Size"] = sizeRanges

    return (schoolPerfBySize.sort_values(by="School Size").groupby("School Size").mean().round(6))

def summarizeScoresBySchoolType(schoolsSummary):
    # schoolsSummary.head(1)
    return schoolsSummary[["School Type", "Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "Overall Passing Rate"]].sort_values(by="School Type").groupby("School Type").mean().round(6)

# Perform the analysis
districtSummary = summarizeDistrict(schoolDataComplete)
schoolsSummary = summarizeSchools(schoolDataComplete)

# Display only relevant columns
districtSummary [['Total Schools', 'Total Students', 'Total Budget', 'Average Math Score', 'Average Reading Score','% Students Pass Math', "% Students Pass Reading", 'Average Pass Rate']]
schoolsSummary [['School Name', 'Per Student Budget', 'Total Students', 'Overall Passing Rate']]
#


# Top Performing schools
sortNumSchools ("Overall Passing Rate", 5, "descending")
# Bottom Performing schools
sortNumSchools("Overall Passing Rate", 5, "ascending")

summarizeScoresByGrade (schoolDataComplete, "math")
summarizeScoresByGrade (schoolDataComplete, "reading")

summarizeScoresBySpendingBudget(schoolsSummary)
summarizeScoresBySchoolSize(schoolsSummary)
summarizeScoresBySchoolType(schoolsSummary)
# size_bins = [0, 1000, 2000, 5000]
# group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
