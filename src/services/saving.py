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
    # Get columns count
    with open(csv_filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)
        columns_count = len(first_row)

    cur_pointer = 0
    row = []

    # Add to the columns transcript text
    results.append(AnswerResult(answer=transcript, save_to_column=transcript_column))
    results.sort(key=lambda r: r.save_to_column)

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
