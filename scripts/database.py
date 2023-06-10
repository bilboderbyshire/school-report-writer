import pocketbase
from settings import *
from containers import *

class Pb(pocketbase.PocketBase):
    def __init__(self):
        super().__init__(URL)
        self.user_data = None
        self.user_model = None
        self.user_token = None
        self.user_is_valid = False

    def login(self, email, password) -> tuple[Response, None | str]:
        try:
            self.user_data = self.collection("users").auth_with_password(email, password)
            self.user_model = self.auth_store.model
            self.user_token = self.auth_store.token
            self.user_is_valid = True

            return {"response": True,
                    "message": "Success"}, None

        except pocketbase.client.ClientResponseError as e:
            print("Error with getting username:", repr(e))
            print(e.data)

            if e.data["message"] == "Failed to authenticate.":
                error_string = e.data["message"] + " Make sure your username and password are correct"
            else:
                error_string = e.data["message"] + ":"

            if "identity" in e.data["data"].keys():
                error_string += f" Username {e.data['data']['identity']['message']}"
            elif "password" in e.data["data"].keys():
                error_string += f" Password {e.data['data']['password']['message']}"

            return {"response": False,
                    "message": error_string}, e.data["code"]

    def logout(self) -> None:
        self.auth_store.clear()
        self.user_is_valid = False
        self.user_data = None
        self.user_model = None
        self.user_token = None

    def refresh_auth(self) -> Response:
        try:
            self.user_data = self.collection("users").authRefresh()
            self.user_model = self.auth_store.model
            self.user_token = self.auth_store.token
            self.user_is_valid = True

            return {"response": True,
                    "message": "Success"}

        except pocketbase.client.ClientResponseError as e:
            print("Error with refreshing session:", repr(e))
            print(e.data)
            self.auth_store.clear()
            self.user_is_valid = False
            self.user_data = None
            self.user_model = None
            self.user_token = None
            return {"response": False,
                    "message": f"Error {e.data['code']}"}

    def user_valid(self) -> bool:
        return self.user_is_valid

    def get_users_forename(self) -> tuple[Response, None | str]:
        if self.user_is_valid:
            return {"response": False,
                    "message": "Success",
                    "value": self.user_model.forename}

        else:
            return {"response": False,
                    "message": "No user",
                    "value": None}

    def get_users_email(self) -> tuple[Response, None | str]:
        if self.user_is_valid:
            return {"response": False,
                    "message": "Success",
                    "value": self.user_model.email}
        else:
            return {"response": False,
                    "message": "No user",
                    "value": None}

    def get_set_reports(self) -> tuple[Response, list[SingleReportSet]]:
        self.refresh_auth()
        if self.user_is_valid:
            try:
                results = self.collection("report_set").get_full_list(query_params={
                    "expand": "template, template.owner, user"
                })
                return_list = [SingleReportSet(i) for i in results]
                return {
                    "response": True,
                    "message": "success"
                }, return_list

            except pocketbase.client.ClientResponseError as e:
                print("Error collecting set reports:", repr(e))
                print(e.data)

                return ({"response": False,
                         "message": "Getting set reports failed"}, [])




RUNNING_DB = Pb()
RUNNING_DB.login("iris@higgins.com", "password123")

# results = RUNNING_DB.collection("report_pieces").get_full_list(query_params={
#     "expand": "template",
#     "filter": 'template = "22xo1dtgrjmcw9s"',
#     "sort": "-piece_position"
# })
#
# for i in results:
#     print(i.piece_text, i.piece_position, i.expand)
