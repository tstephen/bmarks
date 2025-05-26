import csv
from datetime import datetime, timezone
import logging
import os
from bmarks.models import Outline
import argparse
from jinja2 import Template
from importlib.resources import files

logger = logging.getLogger(__name__)


def read_outlines_from_csv(csv_path):
    outlines = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            outline = Outline(
                title=row.get('title', ''),
                url=row.get('url', ''),
                category=row.get('tags'),
                created_at=datetime.fromtimestamp(int(row['time_added']), tz=timezone.utc) if 'time_added' in row and row['time_added'] else datetime.now(datetime.timezone.utc),
                status=row.get('status', 'archive')
            )
            outlines.append(outline)
    return outlines


def main():
    parser = argparse.ArgumentParser(description="Read outlines from a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output OPML file", default=None, nargs='?')
    args = parser.parse_args()

    outlines = read_outlines_from_csv(args.input_file)
    logger.info("Loaded %s outlines.", len(outlines))
    template_path = files("bmarks.templates").joinpath("pocket2opml.j2")
    with open(template_path, "r", encoding="utf-8") as f:
        opml_template = f.read()

    template = Template(opml_template)
    opml_output = template.render(
        now=datetime.now(timezone.utc).isoformat(),
        outlines=outlines
    )
    if args.output_file:
        dirname = os.path.dirname(args.output_file)
        if dirname != '' and not os.path.exists(dirname):
            os.makedirs(os.path.dirname(args.output_file))
        with open(args.output_file, "w", encoding="utf-8") as f:
            logger.info("OPML output written to %s", args.output_file)
            f.write(opml_output)
    else:
        print(opml_output)


if __name__ == "__main__":
    main()
