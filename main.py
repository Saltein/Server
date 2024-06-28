# import modules
from flask import Flask
from flask import request
from flask import jsonify
import traceback, json
from sqliteMode import *
from func import *
from _datetime import datetime

# create flask object
app = Flask(__name__)


# Base commands
@app.route('/checkuser', methods=['POST'])
def checkUser():
    """"route for verify the user by telegram id"""
    try:
        check = CheckUserIdTg(request.json["id_tg"])
        ##print(check)
        if len(check) > 0:
            return jsonify({"action": "success", "name": check["name"], "id": check["id"]})
        else:
            return jsonify({"action": "success", "name": "None"})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/getusers', methods=['POST'])
def getUsers():
    """route for reading user data"""
    try:
        data = SelectData("users", "id", request.json["id"])
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/registrations', methods=['POST'])
def registrations():
    """route for  register users"""
    try:
        idUser = GenerateAlfNumStr(10)
        INNSI = f'"{idUser}", "{request.json["name"]}", "{request.json["numb"]}", "{request.json["id_tg"]}", "{request.json["surname"]}"'
        check = InsertData(T="users", V=INNSI)
        con.commit()
        if len(check) > 1:
            return jsonify({"action": "success", "id": idUser})
        else:
            return jsonify({"action": "errorData"})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/balance/getusers', methods=['POST'])
def getUsersBalance():
    """route for getting users balance"""
    try:
        user_id = request.json['user_id']
        user_balance = SelectData("balance", "user_id", user_id, "summ" )["summ"]

        return jsonify({"action": "success", "balance": user_balance})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/balance/spending', methods=['POST'])
def SpendTheBalance():
    """route for spending users balance"""
    try:
        user_id = request.json['user_id']
        deduction = request.json['deduction']

        user_balance = SelectData("balance", "user_id", user_id, "summ" )["summ"]

        user_balance -= deduction

        UpdateData("balance", "summ", user_balance, "user_id", user_id)
        #create a transaction
        current_datetime = str(datetime.now())
        transaction_id = GenerateAlfNumStr(10)
        transaction_data = f'"{transaction_id}", "{user_id}", "{deduction}", "{current_datetime}", "purchase" '
        InsertData("transactions", transaction_data)

        return jsonify({"action": "success", "balance": user_balance})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/balance/recharging', methods=['POST'])
def RechargeTheBalance():
    """route for recharging users balance"""
    try:
        credit = request.json['credit']
        user_id = request.json['user_id']
        user_balance = SelectData("balance", "user_id", user_id, "summ" )["summ"]

        user_balance += credit

        UpdateData("balance", "summ", user_balance, "user_id", user_id)

        #create a transaction
        current_datetime = str(datetime.now())
        transaction_id = GenerateAlfNumStr(10)
        transaction_data = f'"{transaction_id}", "{user_id}", "{credit}", "{current_datetime}", "deposit" '
        InsertData("transactions", transaction_data)

        return jsonify({"action": "success", "balance": user_balance})
    except Exception as e:
        return jsonify({"action": "errorData"})

        
# Working with consent
@app.route('/consent/save_response', methods=['POST'])
def saveUserConsent():
    """
    Route for saving user's consent response.

    Expects JSON data with the following fields:
    - id_tg: Telegram ID of the user (int)
    - response: User's response ('accept' or 'decline')
    - timestamp: Timestamp of the response (string)

    Returns:
    - {"action": "success"} if data is successfully saved.
    - {"action": "errorData"} if there is an error during the process.
    """
    try:

        id_agreement = GenerateAlfNumStr(7)
        user_tg_id = request.json["user_tg_id"]
        response = request.json["response"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Example of inserting data into your database (modify as per your database structure):
        status = InsertData("agreement", f'"{id_agreement}","{user_tg_id}", "{response}", "{timestamp}"')

        if len(status) > 0:

            return jsonify({"action": "success"})
        else:
            return jsonify({"action": "errorData"})
    except Exception as e:
        return jsonify({"action": "errorData"})




@app.route('/consent/get_response', methods=['POST'])
def getUserConsent():
        """
        Route for retrieving user's consent response.

        Expects JSON data with the following fields:
        - id_tg: Telegram ID of the user (int)

        Returns:
        - {"action": "success", "data": {"response": <response>, "timestamp": <timestamp>}}
          if data is successfully retrieved.
        - {"action": "errorData"} if there is an error during the process.
        """
        try:
            user_tg_id = request.json["user_tg_id"]
            # Example of retrieving data from your database (modify as per your database structure):
            response_data = SelectData(T="agreement", C= "user_tg_id", V= user_tg_id)
            if response_data:
                response = response_data["response"]
                timestamp = response_data["datetime"]
                id_agreement = response_data["id_agreement"]

                return jsonify({"action": "success", "data": {"response": response, "datetime": timestamp, "id_agreement":id_agreement}})
            else:
                return jsonify({"action": "errorData", "data": {"response": None, "datetime": None}})
        except Exception as e:
            return jsonify({"action": "errorData"})


@app.route('/check_drivers/save_drivers', methods=['POST'])
def saveDriversCheck():
    """
    Route for saving user's consent response.

    Expects JSON data with the following fields:
    - id_tg: Telegram ID of the user (int)
    - response: User's response ('accept' or 'decline')
    - timestamp: Timestamp of the response (string)

    Returns:
    - {"action": "success"} if data is successfully saved.
    - {"action": "errorData"} if there is an error during the process.
    """
    try:

        id_become = GenerateAlfNumStr(7)
        id_user = request.json["id_user"]
        status = request.json["status"]
        timedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Example of inserting data into your database (modify as per your database structure):
        insertstatus = InsertData("is_become_driver", f'"{id_become}","{id_user}", "{status}", "{timedate}"')

        if len(insertstatus) > 0:
            return jsonify({"action": "success"})
        else:
            return jsonify({"action": "errorData"})
    except Exception as e:
        return jsonify({"action": "errorData"})




@app.route('/check_drivers/get_drivers', methods=['POST'])
def getDriversCheck():
        """
        Route for retrieving user's consent response.

        Expects JSON data with the following fields:
        - id_tg: Telegram ID of the user (int)

        Returns:
        - {"action": "success", "data": {"response": <response>, "timestamp": <timestamp>}}
          if data is successfully retrieved.
        - {"action": "errorData"} if there is an error during the process.
        """
        try:
            id_user = request.json["id_user"]

            # Example of retrieving data from your database (modify as per your database structure):
            status_data = SelectData(T="is_become_driver", C= "id_user", V= id_user)
            if status_data:
                status = status_data["status"]
                timedate = status_data["datetime"]
                id_become = status_data["id_become"]

                return jsonify({"action": "success", "data": {"status": status, "datetime": timedate, "id_become":id_become}})
            else:
                return jsonify({"action": "errorData", "data": {"status": None, "datetime": None}})
        except Exception as e:
            return jsonify({"action": "errorData"})


# Working with trips ---------------------------------------------------------
@app.route('/сreatingtrips', methods=['POST'])
def сreatingTrips():
    """
    Route for creating trips
    If the user is a driver, then there is a recording in the agreed trips
    """
    try:
        id_trips = GenerateAlfNumStr(7)
        id_trip = GenerateAlfNumStr(7)
        ITTTPPI = f'"{request.json["user_id"]}", "{request.json["typeofmembers"]}", "{request.json["tripsdates"]}", "{request.json["tripstimes"]}", "{request.json["direction_name"]}", "{request.json["route_number"]}", "{request.json["pointa"]}","{request.json["pointb"]}", "{id_trips}", "{request.json["number_of_passengers"]}", "{request.json["status"]}"'
        check = InsertData("trips", ITTTPPI)
        con.commit()
        if request.json["typeofmembers"] == "driver":
            request_bd = f'"{id_trip}", "{request.json["user_id"]}", {request.json["maximum_number_of_passengers"]}, {request.json["number_of_passengers"]}, "{id_trips}", "{request.json["status"]}"'
            check_2 = InsertData("agreedTrips", request_bd,
                               "(agreeding_trips_id, driver_trip_id, maximum_number_of_passengers, number_of_passengers, ids_trips, status)")
            con.commit()
            return jsonify({"action": "success", "id_trip": id_trips, "id_agreedTrips": id_trip})
        if len(check) > 0:
            return jsonify({"action": "success", "id_trip": id_trips})
        else:
            return jsonify({"action": "errorData"})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/gettrips/trips', methods=['POST'])
def getTrips():
    """route for checking for suitable trips"""
    try:
        data = SelectAllData("trips", "user_id", request.json["id"])
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/gettrips/trips/Trips', methods=['POST'])
def TripsDrivers():
    """route for get  suitable trips"""
    try:
        data = SelectAllData("trips", ' "status" = "agreed" OR "status" ', "waiting")
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/gettrips/trips/suitableTrips', methods=['POST'])
def suitableTripsDrivers():
    """route for get  suitable trips"""
    try:
        data = SelectAllData("trips", "status", "waiting")
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/gettrips/trips/agreedTrips', methods=['POST'])
def agreedTripsDrivers():
    """route for get  suitable trips"""
    try:
        data = SelectAllData("trips", "status", "agreed")
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/gettrips/agreedTrips', methods=['POST'])
def agreedTrips():
    """route for checking for agreed trips"""
    try:
        data = SelectAllData("agreedTrips", "id_trip", request.json["id_trip"])
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/gettrips/agreedTrips/suitableTrips', methods=['POST'])
def suitableTripsPassengers():
    """route for get  suitable trips"""
    try:
        data = SelectAllData("agreedTrips", "status", "waiting")
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/settrips/agreedTrips', methods=['POST'])
def setAgreedTrips():
    """route for set  agreed trips"""
    try:
        data = SelectAllData("agreedTrips", "id_trip", request.json["id_agreed_trip"])
        if int(data[0]["number_of_passengers"]) == int(data[0]["maximum_number_of_passengers"]):
            UpdateData("agreedTrips", "(status)", '"agreed"', "id_trip", request.json["id_agreed_trip"])
            return jsonify({"action": "success", "status": "no seats "})
        elif int(data[0]["number_of_passengers"]) > int(data[0]["maximum_number_of_passengers"]):
            return jsonify({"action": "success", "status": "technical error"})
        else:
            request_bd = f'"{int(data[0]["number_of_passengers"]) + 1}", "{data[0]["id_passenger"]}/{request.json["id_passenger"]}", "{data[0]["ids_trips"]}/{request.json["id_trip"]}"'
            check = UpdateData("agreedTrips", "(number_of_passengers, id_passenger, ids_trips)", request_bd, "id_trip",
                               request.json["id_agreed_trip"])
            check_1 = UpdateData("trips", "(status)", '"agreed"', "id_trip", request.json["id_trip"])
            con.commit()
            if len(check) > 1:
                return jsonify({"action": "success", "status": "success"})
            return jsonify({"action": "errorData1"})
    except Exception as e:
        ##print(traceback.format_exc())
        return jsonify({"action": "errorData"})


@app.route('/gettrips/drivers', methods=['POST'])
def drivers():
    """route for reading drivers trips"""
    try:
        data = SelectAllData("drivers", "user_id", request.json["user_id"])
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/registrations/drivers', methods=['POST'])
def registrationsDrivers():
    """route for driver registration"""
    try:
        car_id = GenerateAlfNumStr(7)
        IBCN = f'"{request.json["user_id"]}", "{request.json["brand"]}", "{request.json["colour"]}", "{request.json["numbcar"]}", "{car_id}"'
        InsertData("drivers", IBCN)
        con.commit()
        return jsonify({"action": "success"})
    except Exception as e:
        return jsonify({"action": "errorData1"})


@app.route('/gettrips/drivers/delete', methods=['POST'])
def driversDelete():
    """route for delete drivers trips"""
    try:
        data = DeleteData("drivers", "user_id", request.json["user_id"])
        return jsonify({"action": "success", "data": data})
    except Exception as e:
        return jsonify({"action": "errorData"})


@app.route('/updatetrips/trips/status', methods=['POST'])
def updateTripStatus():
    """
    Route for updating the status of a trip.

    Parameters:
        - status: The new status of the trip (string)
        - id_trip: The ID of the trip (int)

    Returns:
        - If the data has been successfully updated, returns:
            {"action": "success"}
        - If the data update failed, returns:
            {"action": "error"}
        - If an error occurred during the update process, returns:
            {"action": "errorData <error_message>"}
    """
    try:
        data = UpdateData("trips", "(status)", f'"{request.json["status"]}"', "id_trip", request.json["id_trip"])
        if len(data) > 1:
            return jsonify({"action": "success"})
        return jsonify({"action": "error"})
    except Exception as e:
        return jsonify({"action": f"errorData {e}"})


# ----------------- admin -----------------
@app.route('/admin/get_by_number', methods=['POST'])
def AdminGetByNumber():
        """
        Admin route for retrieving all users by number.
        """

        request_number = request.json["numb"]

        try:
            # Example of retrieving data from your database (modify as per your database structure):
            user_data = SelectAllData("users", "numb", request_number)
            if user_data:
                return jsonify({"action": "success", "data": user_data})
            else:
                return jsonify({"action": "errorData", "data": "error"})
        except Exception as e:
            return jsonify({"action": "errorData"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

try:
    con.commit()
    con.close()
except:
    pass
