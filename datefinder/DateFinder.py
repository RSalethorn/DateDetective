from datetime import datetime

from datefinder.ModelHandler import ModelHandler
from datefinder.BiLSTMTagger import BiLSTMTagger

class DateFinder:
    """
    A class used as an access point for all DateFinder functionality

    ...

    Attributes
    ----------
    mh : ModelHandler
        The object that handles any interaction with torch model

    Methods
    -------
    get_format(date)
        Takes a date string, uses model for predictions then creates a datetime format string

    get_datetime(date)
        Takes a date string, uses model for predictions, creates format string and uses it to
        create a datetime object
    """
    def __init__(self, useCuda = True):
        self.mh = ModelHandler(useCuda)

    def get_format(self, date)-> str:
        """Takes a date string, uses model for predictions then creates a datetime format string

        Parameters:
        date (str): A string representation of a date.

        Returns:
        str: A string format of the given date that can be used with datetime module.

        """
        tags = self.mh.predict_date_tags(date)

        date_format = ""

        # Split given date into list of chars
        date_chars = list(date)

        # Go through each predicted tag
        for i in range(len(tags)):
            # Remove the Before and Inside (B & I) and "-" from tags
            tags[i] = tags[i].split("-")[-1]
            # For non classified char add char to dateformat
            if "None" in tags[i]:
                date_format += date_chars[i]
            # If tag is first tag of its type add to dateformat
            elif tags[i] != tags[i-1]:
                date_format += f"%{tags[i]}"

        return date_format
    
    def get_datetime(self, date)-> datetime:
        """Takes a date string, uses model for predictions then creates a datetime format string

        Parameters:
        date (str): A string representation of a date.

        Returns:
        datetime: A datetime object that represents the given date

        """
        date_format = self.get_format(date)

        date = datetime.strptime(date, date_format)

        return date


if __name__ == "__main__":
    df = DateFinder()
    print(df.get_format("30/12/2023 12:52:23"))
    print(df.get_datetime("30/12/2023 12:52:23").day)
    print(df.__doc__)
