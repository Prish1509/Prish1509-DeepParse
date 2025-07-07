from sentence_transformers import SentenceTransformer
import joblib

# load the sentence transformer model to create embeddings from log messages
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

# load the trained classification model
classifier_model = joblib.load('models/log_classifier.joblib')

def classify_with_bert(log_message):
    # turn the log message into an embedding
    message_embedding = transformer_model.encode(log_message)

    # get prediction probabilities for each class
    probabilities = classifier_model.predict_proba([message_embedding])[0]

    # if the confidence is too low, return 'unclassified'
    if max(probabilities) < 0.5:
        return "Unclassified"

    # otherwise, return the predicted label
    predicted_label = classifier_model.predict([message_embedding])[0]
    return predicted_label


if __name__ == "__main__":
    # some sample logs to test the model
    logs = [
        "alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
        "GET /v2/3454/servers/detail HTTP/1.1 RCODE 404 len: 1583 time: 0.1878400",
        "System crashed due to drivers errors when restarting the server",
        "Hey bro, chill ya!",
        "Multiple login failures occurred on user 6454 account",
        "Server A790 was restarted unexpectedly during the process of data transfer"
    ]

    # loop through each log and print its predicted label
    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)
