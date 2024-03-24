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

            # If unique format predicted add to dictionary
            if date_format not in identified_formats:
                identified_formats[date_format] = 1
            # Increase count on format to count times format is predicted
            else:
                identified_formats[date_format] += 1
                
        # Sort formats by most times predicted
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
    

    def get_dict_list_format(self, dict_list, date_key):
        """ Takes a list of dictionary objects that contain a date string, and gets format predictions for each date in dictionaries. Then finds the format that is predicted most often.

        Parameters:
        date_str_list (list[dict[]]): A list of dictionaries, that can contain date strings

        date_key (str): The key that contains string dates inside the dictionary

        Returns:
        str: A string format of the dates, that is predicted most often from the dictionaries.


        """
        # Create list of date strings from dicts
        date_strs = [dict.get(date_key) for dict in dict_list]

        # Remove None values from list incase dicts don't contain date key
        date_strs = [date_str for date_str in date_strs if date_str != None]

        date_format = self.get_list_format(date_strs)

        return date_format
    
    
    def get_dict_list_datetime(self, dict_list, date_key, retain_date_str=False):
        """ Takes a list of dictionary objects that contain a date string, and gets format predictions for each date in dictionaries. Then finds the format that is predicted most often.
        Each date under given key is then converted to a datetime object. If retain_date_str is true then the original date string will be retained in each dictionary under the date
        key with "_original" added to the end.

        Parameters:
        date_str_list (list[dict[]]): A list of dictionaries, that can contain date strings.

        date_key (str): The key that contains string dates inside the dictionary.

        retain_date_str (bool): If true retain original date string under date key with "_original" added to the end

        Returns:
        list[dict[]]: A list of dictionaries that is a copy of dict_list with date strings under given key converted to datetime objects.


        """
        date_format = self.get_dict_list_format(dict_list, date_key)

        # Loop all dictionaries
        for n in range(len(dict_list)):
            # If dictionary doesn't contain date
            if date_key not in dict_list[n]:
                continue
            
            # Retain original string under different key
            if retain_date_str:
                dict_list[n][f"{date_key}_original"] = dict_list[n][date_key]
            
            dict_list[n][date_key] = datetime.strptime(dict_list[n][date_key], date_format)
        
        return dict_list


            



if __name__ == "__main__":
    df = DateDetective()
    print(df.get_format("30/12/2023 12:52:23"))
    print(df.get_datetime("30/12/2023 12:52:23").day)
    print(df.__doc__)
