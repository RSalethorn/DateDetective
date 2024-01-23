import torch

from datefinder.BiLSTMTagger import BiLSTMTagger
from datefinder.Encoding import char_to_index, index_to_tag

MODEL = {
            "location": "./datefinder/model_Ms_Zoey_Fadel_MD_state_dict.pth",
            "num_characters": len(char_to_index),
            "num_tags": len(index_to_tag),
            "embedding_dim": 32,
            "hidden_dim": 256
        }

class ModelHandler:
    """
    A class used to complete operations with the model file.

    ...

    Attributes
    ----------
    device : torch.device
        The object that represents what device tensor operations should be done (CPU/GPU)

    model : torch.nn.Module
        The model to be used to create format predictions.
    
    Methods
    -------
    preprocess_input(input_date)
        Takes a date string, and converts it to a tensor that represents a date.

    postprocess_output(output_tensor)
        Takes output tensor from model and converts it to the predicted tags for a date.

    predict_date_tags(input_date)
        Takes a date and produces format predictions tags for each character of a date.
   
     """
    def __init__(self, useCuda):
        """Loads the model file and selects if processing will be on CUDA cores or CPU

        Parameters:
        model_location (str): File path for the model file.

        """
        self.model = BiLSTMTagger(MODEL["num_characters"], MODEL["num_tags"], MODEL["embedding_dim"], MODEL["hidden_dim"])
        
        # Determine the device
        self.device = torch.device("cuda" if torch.cuda.is_available() and useCuda is True else "cpu")
        self.model = self.model.to(self.device)

        self.model.load_state_dict(torch.load(MODEL['location'], map_location=self.device))

        print(f"Loaded model - {MODEL['location']}, to {self.device}")
    
    def preprocess_input(self, input_date):
        """Takes an input date and turns into a tensor where each element is the encoded
        form of a character in date.

        Parameters:
        input_date (str): A string representation of a date.

        Returns:
        torch.tensor: A tensor that represents the inputted date for the model.

        """
        input_date = input_date.lower()
        # Tokenize and convert to indices
        character_indices = [char_to_index[char] for char in input_date]
        # Convert to tensor and add batch dimension
        return torch.tensor(character_indices, dtype=torch.long).unsqueeze(0).to(self.device)

    def postprocess_output(self, output_tensor):
        """Takes output tensor from model and converts it to the predicted tags for each
        character of a date.

        Parameters:
        output_tensor (torch.tensor): An output tensor produced by the model.

        Returns:
        list of str: A list of strings where each string is a date format prediction for
                     an individual character in a date.

        """
        # Convert probabilities to tag indices
        _, predicted_tags = torch.max(output_tensor, dim=2)

        if predicted_tags.is_cuda:
            predicted_tags = predicted_tags.cpu()

        # Convert indices to tags
        predicted_tags = [index_to_tag[index.item()] for index in predicted_tags[0]]
        return predicted_tags

    def predict_date_tags(self, input_date):
        # Preprocess the input
        input_tensor = self.preprocess_input(input_date)

        # Set the model to evaluation mode
        self.model.eval()

        # Predict
        with torch.no_grad():
            output_tensor = self.model(input_tensor)

        # Postprocess the output
        predicted_tags = self.postprocess_output(output_tensor)

        return predicted_tags