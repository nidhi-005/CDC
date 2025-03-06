import pandas as pd
import os
from django.http import JsonResponse
from django.views import View
from django.conf import settings

class PlacementStatisticsView(View):
    def get(self, request):
        # Load CSV files
        students_path = os.path.join(settings.BASE_DIR, 'data', 'students.csv')
        placements_path = os.path.join(settings.BASE_DIR, 'data', 'placements.csv')
        applications_path = os.path.join(settings.BASE_DIR, 'data', 'placement_applications.csv')

        try:
            students_df = pd.read_csv(students_path)
            placements_df = pd.read_csv(placements_path)
            applications_df = pd.read_csv(applications_path)
        except FileNotFoundError:
            return JsonResponse({"error": "CSV files not found"}, status=500)

        # Merge datasets
        merged_df = applications_df.merge(placements_df, left_on="placementid", right_on="id") \
                                   .merge(students_df, left_on="studentid", right_on="id")

        merged_df = merged_df[merged_df["selected"] == True]  # Filter only selected students

        # Compute statistics per branch
        statistics = {"highest_ctc": {}, "median_ctc": {}, "lowest_ctc": {}, "average_ctc": {}, "percentage_placed": {}}

        for branch in students_df["branch"].unique():
            branch_students = students_df[students_df["branch"] == branch]
            branch_placements = merged_df[merged_df["branch"] == branch]

            if branch_placements.empty:
                statistics["highest_ctc"][branch] = None
                statistics["median_ctc"][branch] = None
                statistics["lowest_ctc"][branch] = None
                statistics["average_ctc"][branch] = None
                statistics["percentage_placed"][branch] = 0
                continue

            ctc_values = branch_placements["ctc"].astype(float)
            statistics["highest_ctc"][branch] = ctc_values.max()
            statistics["median_ctc"][branch] = ctc_values.median()
            statistics["lowest_ctc"][branch] = ctc_values.min()
            statistics["average_ctc"][branch] = ctc_values.mean()
            statistics["percentage_placed"][branch] = (len(branch_placements["studentid"].unique()) / len(branch_students)) * 100

        # Student-wise placement details
        students_list = []
        for _, student in students_df.iterrows():
            student_placements = merged_df[merged_df["studentid"] == student["id"]]
            if student_placements.empty:
                continue

            companies_selected = student_placements["name"].tolist()
            highest_ctc = student_placements["ctc"].astype(float).max()

            students_list.append({
                "rollno": student["rollno"],
                "branch": student["branch"],
                "batch": student["batch"],
                "companies_selected": companies_selected,
                "ctc": highest_ctc
            })

        return JsonResponse({
            "highest_ctc": statistics["highest_ctc"],
            "median_ctc": statistics["median_ctc"],
            "lowest_ctc": statistics["lowest_ctc"],
            "average_ctc": statistics["average_ctc"],
            "percentage_placed": statistics["percentage_placed"],
            "students": students_list if students_list else None
        })

