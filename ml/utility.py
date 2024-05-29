from sklearn.model_selection import train_test_split

def split_data(features, target, split=0.2):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=split)
    return X_train, X_test, y_train, y_test