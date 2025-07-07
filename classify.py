from regex_processor import classify_with_regex  # handles logs using regex rules
from BERT_processor import classify_with_bert    # handles logs using sentence transformers + logistic regression
from LLM_processor import classify_with_llm      # handles logs using a large language model
import pandas as pd

# main function to classify a list of (source, log_message) pairs
def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append(label)
    return labels

# picks the right method based on source or fallback if one fails
def classify_log(source, log_message):
    if source == "LegacyCRM":
        # if source is legacycrm, use the llm method
        label = classify_with_llm(log_message)
    else:
        # first try regex
        label = classify_with_regex(log_message)
        # if regex doesn’t return anything, try bert model
        if label is None:
            label = classify_with_bert(log_message)
    return label

# handles classification from a csv file
def classify_csv(input_file):
    df = pd.read_csv(input_file)

    # create target_label column with predicted classes
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    # save the result to a new csv file
    output_file = "data/output.csv"
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    # run the classification on a test csv file
    classify_csv("data/test.csv")

    # for testing without csv, you can use the sample logs below
    # logs = [
    #     ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    #     ("BillingSystem", "User User12345 logged in."),
    #     ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
    #     ("AnalyticsEngine", "Backup completed successfully."),
    #     ("ModernHR", "GET /v2/54fa9db421ce4c0dcbaed9335e4c35ae/servers/detail HTTP/1.1 RCODE 200 len: 1583 time: 0.187840"),
    #     ("ModernHR", "Admin access escalation detected for user 9429"),
    #     ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    #     ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
    #     ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
    #     ("LegacyCRM", "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the new analytics module.")
    # ]

    # classified_logs = classify(logs)
    # print(classified_logs)
