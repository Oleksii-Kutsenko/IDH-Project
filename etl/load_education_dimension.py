from enum import Enum

from openpyxl import load_workbook

from models.education_dimension import EducationDimension

DATA_RANGE = "B13:D796"


class ReportType(Enum):
    MATH = 1
    SCIENCE = 2
    READING = 3


REPORT_TYPE_MAP = {
    ReportType.MATH: "math_score",
    ReportType.SCIENCE: "science_score",
    ReportType.READING: "reading_score",
}


def load_education_dimension():
    excel = load_workbook("etl/data/pisa_scores.xlsx")

    # Data has been divided into three worksheets: Math, Science, and Reading
    # So we need to link data by year and country
    education_dimension_dict = {}
    for worksheet_name, report_type in zip(excel.sheetnames, list(ReportType)):
        worksheet = excel[worksheet_name]

        year = None
        for row in worksheet[DATA_RANGE]:
            if row[0].value is not None and row[0].value.isdecimal():
                year = int(row[0].value)

            dict_key = (year, row[1].value)
            if dict_key not in education_dimension_dict:
                education_dimension_dict[dict_key] = {REPORT_TYPE_MAP[report_type]: row[2].value}
            else:
                education_dimension_dict[dict_key][REPORT_TYPE_MAP[report_type]] = row[2].value
    import pdb

    pdb.set_trace()
    education_dim_objects = []
