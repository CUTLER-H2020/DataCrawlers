"""

This script removes all comments from the raw comment area to have distinct sets of comment
and non-comment data

It is only used to gather training and test data for the classifier and not needed for the crawler itself

"""
import pandas as pd

comments = pd.read_csv('native_comments.csv', header=None, usecols=[1])
comment_area = pd.read_csv('raw_comment_area.csv', header=None, usecols=[1])

mask = comment_area.isin(comments.to_dict(orient='list')).all(axis=1)
data = comment_area[~mask]

data.to_csv('area_without_comments.csv')