import datetime
import pandas as pd

def get_and_write_metadata(df_comments):
    """
    Writes the meta.txt file as is required for the Hierarchical Multi-Dirichlet Process (HMDP) implementation
    provided by Promoss.
    See https://github.com/ckling/promoss for further information.


    :param df_comments:  pandas.DataFrame containing the df_comments
    :return:
    """
    #df_comments = get_doc_identifier(df_comments)
    df_comments["date_of_experience"].to_csv('meta.txt', sep=';', index=None, header=None)
    #df_comments["sentiment"].to_csv('meta.txt', sep=';', index=None, header=None)

    return df_comments


if __name__ == '__main__':
    get_metadata()
