import csv

from src.models import AnswerResult


def save_to_csv(
        csv_filename: str,
        transcript: str,
        transcript_column: int,
        results: list[AnswerResult]
) -> None:
    with open(csv_filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)
        columns_count = len(first_row)

    cur_pointer = 0
    row = []

    results.append(AnswerResult(answer=transcript, save_to_column=transcript_column))
    results.sort(key=lambda r: r.save_to_column)

    for i in range(columns_count):
        if i == results[cur_pointer].save_to_column-1:
            row.append(results[cur_pointer].answer)
            cur_pointer += 1
            continue

        row.append("")

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
