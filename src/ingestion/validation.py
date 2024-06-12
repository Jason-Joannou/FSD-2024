from .exceptions import InvalidDatasetName

def validate_dataset_name(dataset_name: str) -> None:
    validation_array = dataset_name.split("/")
    
    # Check correct format
    if len(validation_array) == 1:
        message = f"The dataset name '{dataset_name}' is not in the right format. The format should be '[owner]/[dataset]'."
        raise InvalidDatasetName(message)
    
    # Check owner format
    if " " in validation_array[0]:
        message = f"The owner name '{validation_array[0]}' contains spaces. Owner name should not contain spaces."
        raise InvalidDatasetName(message)
    
    # Check dataset format
    if " " in validation_array[1]:
        message = f"The dataset name '{validation_array[1]}' contains spaces. Dataset name should not contain spaces."
        raise InvalidDatasetName(message)
    
    if len(validation_array)>2:
        message = f"The dataset name '{dataset_name}' is not in the right format. The format should be '[owner]/[dataset]'."
        raise InvalidDatasetName(message)


    

    
    
