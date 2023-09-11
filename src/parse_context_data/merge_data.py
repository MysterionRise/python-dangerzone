import csv
import os


def process_log_files(directory_path):
    # List to store the events
    events = []

    # Loop over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".log"):
            with open(os.path.join(directory_path, filename), "r") as f:
                lines = f.readlines()

                # Extract user_id from filename
                user_id = os.path.splitext(filename)[0]

                # Process the file line by line
                for i in range(0, len(lines), 4):
                    try:
                        answer = lines[i].strip().split(",")[0]
                        answer_reaction_time = lines[i].strip().split(",")[1]
                        certainty = lines[i + 1].strip().split(",")[0]
                        certainty_reaction_time = lines[i + 1].strip().split(",")[1]

                        events.append(
                            [
                                user_id,
                                answer,
                                answer_reaction_time,
                                certainty,
                                certainty_reaction_time,
                            ]
                        )
                    except IndexError:
                        # Handle incomplete data
                        continue

    # Write events to a CSV file
    with open("merged_logs.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "user_id",
                "answer",
                "answer_reaction_time",
                "certainty",
                "certainty_reaction_time",
            ]
        )
        writer.writerows(events)


# Process log files in the current directory
process_log_files("./data")
