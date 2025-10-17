import csv

from src.models import AnswerResult


def save_to_csv(
        csv_filename: str,
        transcript: str,
        transcript_column: int,
        results: list[AnswerResult]
) -> None:
    """
    Saves results to a csv file according to save_to_column field

    :param csv_filename: str
    :param transcript: str
    :param transcript_column: int
    :param results: list[AnswerResult]
    :return:
    """
    # Add to the columns transcript text
    results.append(AnswerResult(answer=transcript, save_to_column=transcript_column))
    results.sort(key=lambda r: r.save_to_column)

    # Get columns count
    with open(csv_filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)  # Read all rows into a list
        if data:  # Check if the list is not empty
            last_row = data[-1]
            columns_count = len(last_row)
        else:
            # If no one rows in file, use maximum value of save_to_column as columns_count
            columns_count = max(results, key=lambda r: r.save_to_column).save_to_column

    cur_pointer = 0
    row = []

    # Add only values to row when it equals result save_to_column otherwise put empty string
    for i in range(columns_count):
        if i == results[cur_pointer].save_to_column-1:
            row.append(results[cur_pointer].answer)
            cur_pointer += 1
            continue

        row.append("")

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
