from exporter import export_results

sample_results = [

    {
        "Rank": 1,
        "Candidate": "Resume1.pdf",
        "Score": 91.5,
        "Recommendation": "Strongly Recommended"
    },

    {
        "Rank": 2,
        "Candidate": "Resume2.pdf",
        "Score": 84.3,
        "Recommendation": "Recommended"
    }

]

export_results(sample_results)