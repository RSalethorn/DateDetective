from datetime import datetime

try:
    import torch
    print("PyTorch installation has been found.")
except ImportError:
    raise ImportError("PyTorch installation can't be found in current Python environment. PyTorch is required for DateDetective to work. \nTo install PyTorch go to 'https://pytorch.org/get-started/locally/' to find the install command relevant to you.")


from datedetective.ModelHandler import ModelHandler
from datedetective.BiLSTMTagger import BiLSTMTagger

class DateDetective:
    """
    A class used as an access point for all DateDetective functionality

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
    
    def get_list_format(self, date_str_list) -> str:
        """Takes a list of date strings, and gets format predictions for each date in list. Then finds the format that is predicted most often.

        Parameters:
        date_str_list (str): A list of string representations of dates.

        Returns:
        str: A string format of the dates, that is predicted most often from the list.

        """
        identified_formats = {}
        for date_str in date_str_list:
            date_format = self.get_format(date_str)

            if date_format in identified_formats:
                identified_formats[date_format] += 1
            else:
                identified_formats[date_format] = 1

        sorted_identified_formats = sorted(identified_formats.items(), key=lambda x:x[1], reverse=True)

        most_matched_format = sorted_identified_formats[0][0]

        return most_matched_format
    
    
    def get_list_datetime(self, date_str_list) -> list[datetime]:
        """Takes a list of date strings, and gets format predictions for each date in list. Each date string in the list is then converted to a datetime object, using the format that is predicted the most in the date list.

        Parameters:
        date_str_list (str): A list of string representations of dates.

        Returns:
        list[datetime]: A list of datetime objects that represent the original list of string dates.

        """
        date_format = self.get_list_format(date_str_list)

        date_obj_list = []

        for date_str in date_str_list:
            date_obj = datetime.strptime(date_str, date_format)
            date_obj_list.append(date_obj)
        
        return date_obj_list

            



if __name__ == "__main__":
    df = DateDetective()
    print(df.get_format("30/12/2023 12:52:23"))
    print(df.get_datetime("30/12/2023 12:52:23").day)
    print(df.__doc__)
