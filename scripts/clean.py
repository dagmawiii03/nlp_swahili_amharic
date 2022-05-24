import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from functools import reduce

class Clean:
    """
    - this class is responsible for performing 
    Cleaning Tasks
    """

    def __init__(self, df):
        """initialize the cleaning class"""
        self.df = df

    def has_missing_values(self):
        """
        expects:
            -   nothing
        returns:
            -   boolean
        """
        has_missing_values = False
        if True in self.df.isnull().any().to_list():
            has_missing_values = True
        counts = None
        counts = self.df.isnull().sum()
        return counts,has_missing_values

    def store_features(self,type_,value):
        """
        purpose:
            - stores features for the data set
        input:
            - string,int,dataframe
        returns:
            - dataframe
        """
        features = [None]
        if type_ == "numeric":
            features = self.df.select_dtypes(include=value).columns.tolist()
        elif type_ == "categorical":
            features = self.df.select_dtypes(exclude=value).columns.tolist()
        return features

    def merge_df(self,df_,column):
        """
        expects:
            - string(column)
        returns:
            - merged df
        """
        self.df = pd.merge(self.df, df_, how = 'left', on = column)
        return self.df

    
    def handle_missing_values_numeric(self, features, df=None):
        """
        this algorithm does the following
        - remove columns with x percentage of missing values
        - fill the missing values with the mean
        returns:
            - df
            - percentage of missing values
        """
        if df:
            self.df=df
        missing_percentage = round((self.df.isnull().sum().sum()/\
                reduce(lambda x, y: x*y, self.df.shape))*100,2)
        for key in features:
            self.df[key] = self.df[key].fillna(self.df[key].mean())
        return missing_percentage, self.df

    def handle_missing_values_categorical(self,features):
        """
        this algorithm does the following
        - remove columns with x percentage of missing values
        - fill the missing values with the mode
        returns:
            - df
            - percentage of missing values
        """
        missing_percentage = round((self.df.isnull().sum().sum()/\
                reduce(lambda x, y: x*y, self.df.shape))*100,2)
        for key in features:
            self.df[key] = self.df[key].fillna(self.df[key].mode()[0])
        return missing_percentage, self.df


    def drop_missing_values(self)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        self.df.dropna(inplace=True)
        
    
    def drop_duplicate(self, df:pd.DataFrame,column)->pd.DataFrame:
        """
        - this function drop duplicate rows
        """
        self.df = self.df.drop_duplicates(subset=[column])
        return self.df
        
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        return self.df



    def fix_outliers(self,column,threshold):
        """
        - this algorithm fixes outliers
        """
        numerical_columns=self.store_features("numeric","number")
        for i in numerical_columns:
            if i == column:
                self.df = self.df[self.df[column] < threshold]  #Drops samples which have sales more than 25000
                self.df.reset_index(drop=True)
                
        return

    def remove_unnamed_cols(self):
        """
        - this algorithm removes columns with unnamed
        """
        self.df.drop(self.df.columns[self.df.columns.str.contains('unnamed',
        case = False)],axis = 1, inplace = True)

    def transfrom_time_series(self,column,date_column):
        """
        - transform the data into a 
        time series dataset
        """
        self.df.sort_values([column,date_column], ignore_index=True, inplace=True)    
        self.df[date_column] = pd.to_datetime(self.df[date_column],errors='coerce')
        self.df['Day'] = self.df[date_column].dt.day
        self.df['Month'] = self.df[date_column].dt.month
        self.df['Year'] = self.df[date_column].dt.year
        self.df['DayOfYear'] = self.df[date_column].dt.dayofyear
        self.df['WeekOfYear'] = self.df[date_column].dt.weekofyear
        self.df.set_index(date_column, inplace=True)

    def save(self,name):
        """
        - returns the dataframes
        """
        self.df.to_csv(name,index=False)


    def get_df(self):
        """
        - returns the dataframe
        """
        return self.df

if __name__ == '__main__':
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    store_path = sys.argv[3]
    store = pd.read_csv(store_path)
    df = pd.read_csv(train_path)
    clean_df = Clean(df)
    clean_df.merge_df(store,'Store')
    clean_df.drop_missing_values()
    clean_df.fix_outliers('Sales',25000)
    clean_df.remove_unnamed_cols()
    clean_df.transfrom_time_series("Store","Date")
    clean_df.save(name="data/training.csv")
    df = pd.read_csv(test_path)
    clean_df = Clean(df)
    clean_df.merge_df(store,'Store')
    clean_df.drop_missing_values()
    clean_df.fix_outliers('Sales',25000)
    clean_df.remove_unnamed_cols()
    clean_df.transfrom_time_series("Store","Date")
    clean_df.get_df().drop('Id',axis=1,inplace=True)
    clean_df.save(name="data/testing.csv")