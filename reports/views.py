from datetime import date, datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .reporting import EOD_Reports

#Gathers the data from the .reporting module and returns it.
class DayReport(APIView):
    def get(self, request, *args, **kwargs):

        rep_date = request.query_params.get("date")
        if rep_date:
            rep_date = datetime.strptime(rep_date, "%Y-%m-%d")
        else:
            rep_date = date.today()

        data = {
            "report date": rep_date,
            "todays transactions": EOD_Reports.transactions(rep_date),
            "stock": EOD_Reports.all_stock(),
            "stock running low": EOD_Reports.low_stock(),
        }

        return Response(data)
