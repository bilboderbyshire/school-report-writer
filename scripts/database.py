import pocketbase
from settings import *
from typing import TypedDict, Any


class Response(TypedDict):
    response: bool
    message: str
    value: Any


class Pb(pocketbase.PocketBase):
    def __init__(self):
        super().__init__(URL)
        self.user_data = None
        self.user_model = None
        self.user_token = None
        self.user_is_valid = False

    def get_users_forename(self) -> Response:
        if self.user_is_valid:
            return {"response": False,
                    "message": "Success",
                    "value": self.user_model.forename}

        else:
            return {"response": False,
                    "message": "No user",
                    "value": None}

    def get_users_email(self) -> Response:
        if self.user_is_valid:
            return {"response": False,
                    "message": "Success",
                    "value": self.user_model.email}
        else:
            return {"response": False,
                    "message": "No user",
                    "value": None}

    def login(self, email, password) -> Response:
        try:
            self.user_data = self.collection("users").auth_with_password(email, password)
            self.user_model = self.auth_store.model
            self.user_token = self.auth_store.token
            self.user_is_valid = True

            return {"response": True,
                    "message": "Success",
                    "value": None}

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
                    "message": error_string,
                    "value": e.data["code"]}

    def refresh_auth(self) -> Response:
        try:
            self.user_data = self.collection("users").authRefresh()
            self.user_model = self.auth_store.model
            self.user_token = self.auth_store.token
            self.user_is_valid = True

            return {"response": True,
                    "message": "Success",
                    "value": None}

        except pocketbase.client.ClientResponseError as e:
            print("Error with refreshing session:", repr(e))
            print(e.data)
            self.auth_store.clear()
            self.user_is_valid = False
            self.user_data = None
            self.user_model = None
            self.user_token = None
            return {"response": False,
                    "message": f"Error {e.data['code']}",
                    "value": None}

    def user_valid(self) -> bool:
        return self.user_is_valid

    def logout(self) -> None:
        self.auth_store.clear()
        self.user_is_valid = False
        self.user_data = None
        self.user_model = None
        self.user_token = None


RUNNING_DB = Pb()
