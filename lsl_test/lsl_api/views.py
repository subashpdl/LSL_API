from django.shortcuts import render
from rest_framework import generics
from .models import LSLScript,Result
from .serializers import LSLScriptSerializer
import requests
import time
import datetime
import json

class LSLScriptCreateView(generics.CreateAPIView):
    queryset = LSLScript.objects.all()
    serializer_class = LSLScriptSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')

    def perform_create(self, serializer):
        # Call the get_auth_token function to fetch and store the token
        lsl_script = serializer.save()
        self.get_auth_token(lsl_script)
        self.lsl_execution(serializer)
        self.get_and_store_lasso_data(lsl_script, Result)


    def get_auth_token(self, lsl_script):
        url = "http://lassohp1.informatik.uni-mannheim.de:10222/auth/signin"
        data = {"username": "lgutachter", "password": "27c682dd"}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            response_data = response.json()

            token = response_data.get("token")
            if token:
                lsl_script.token = token
                lsl_script.save()
            else:
                print("Token not found in the response data.")
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print("Error getting token:", e)
            print("Response content:", response.content)

    def lsl_execution(self, serializer):
        # Save the LSLScript instance
        lsl_script = serializer.instance  # Use serializer.instance instead of serializer.save()

        # Prepare the data for the Lasso API
        lasso_data = {
            "script": lsl_script.script,
            "email": lsl_script.email,
            "share": lsl_script.share,
            "type": lsl_script.type
        }

        # Make a POST request to the Lasso API to execute the script
        url = "http://lassohp1.informatik.uni-mannheim.de:10222/api/v1/lasso/execute"
        headers = {
            "Authorization": f"Bearer {lsl_script.token}"
        }

        try:
            response = requests.post(url, json=lasso_data, headers=headers)
            response.raise_for_status()  # Check for API errors

            response_data = response.json()

            # Update the LSLScript instance with the execution ID
            lsl_script.execution_id = response_data.get("executionId")
            lsl_script.save()

            # Call the function to fetch and store additional information
            self.get_and_store_execution_info(lsl_script)
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print("Error executing script:", e)
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            print("Error decoding JSON response:", e)

    def get_and_store_execution_info(self, lsl_script):
        url = f"http://lassohp1.informatik.uni-mannheim.de:10222/api/v1/lasso/scripts/{lsl_script.execution_id}/status"
        headers = {
            "Authorization": f"Bearer {lsl_script.token}"
        }
        try:
            while True:
                response = requests.get(url, headers=headers)
                response_data = response.json()

                # Check if the response contains the status field
                if "status" in response_data:
                    status = response_data["status"]
                    if status == "SUCCESSFUL" or status == "FAILED":
                        # Save status and start time in the model
                        lsl_script.status = status
                        lsl_script.start = datetime.datetime.strptime(response_data.get("start"),
                                                                      '%Y-%m-%dT%H:%M:%S.%f%z')
                        lsl_script.save()
                        break  # Exit the loop when status is successful or failed
                else:
                    print("Invalid response data format:", response_data)

                # Wait for 30 seconds before checking again
                time.sleep(30)
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print("Error:", e)

    def get_and_store_lasso_data(self, lsl_script, Result):
        # Get the execution ID from the lsl_script object
        executionId = lsl_script.execution_id

        # Create the SQL query as a string
        sql_query = ("SELECT * FROM srm.CellValue WHERE executionId = '{executionId}' AND arenaid = 'execute' AND type = 'value' AND x = 0 AND variantid = 'original'")

        # Make a POST request to the Lasso API
        url = f"http://lassohp1.informatik.uni-mannheim.de:10222/api/v1/lasso/report/{executionId}"
        headers = {
            "Authorization": f"Bearer {lsl_script.token}",
            "Content-Type": "application/json;charset=UTF-8"
        }
        data = json.dumps({
            "execution"
            "executionId ": executionId,  # Execution ID as a string
            "sql": sql_query  # SQL query as a string
        })
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()  # Check for API errors

            response_data = response.json()

            Result.execution_id = response_data.get("EXECUTIONID")
            Result.abstraction_id = response_data.get("ABSTRACTIONID")
            Result.action_id = response_data.get("ACTIONID")
            Result.arena_id = response_data.get("ARENAID")
            Result.sheetid = response_data.get("SHEETID")
            Result.systemid = response_data.get("SYSTEMID")
            Result.variantid = response_data.get("VARIANTID")
            Result.adapterid = response_data.get("ADAPTERID")
            Result.x = response_data.get("X")
            Result.y = response_data.get("Y")
            Result.type = response_data.get("TYPE")
            Result.value = response_data.get("VALUE")
            Result.rawvalue = response_data.get("RAWVALUE")
            Result.valuetype = response_data.get("VALUETYPE")
            Result.lastmodified = response_data.get("LASTMODIFIED")
            Result.executiontime = response_data.get("EXECUTIONTIME")

            Result.save()
            # Create a new LassoResult instance and save it with the response data

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print("Error requesting Lasso data:", e)
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            print("Error decoding JSON response:", e)