import pocketbase
from pocketbase.models.utils import BaseModel
from .settings import *
from .containers import Response, UserCreation


class ReportWriterInstance(pocketbase.PocketBase):
    def __init__(self):
        super().__init__(URL)
        self.user_data = None
        self.user_model = None
        self.user_token = None
        self.user_is_valid = False

    def login(self, email, password) -> Response:
        try:
            self.user_data = self.collection("users").auth_with_password(email, password)
            self.user_model = self.auth_store.model
            self.user_token = self.auth_store.token
            self.user_is_valid = True

            return {"response": True,
                    "message": "Success"}

        except pocketbase.client.ClientResponseError as e:
            print("Error with logging in:", repr(e))
            print(e.data)

            if e.data["message"] == "Failed to authenticate.":
                error_string = e.data["message"] + " Make sure your username and password are correct"
            else:
                error_string = e.data["message"] + ":"

            if "identity" in e.data["data"].keys():
                error_string += f" Email {e.data['data']['identity']['message']}"
            elif "password" in e.data["data"].keys():
                error_string += f" Password {e.data['data']['password']['message']}"

            return {"response": False,
                    "message": f"Error code: {e.data['code']} - {error_string}"}

    def register_account(self, data: UserCreation) -> Response:
        try:
            self.user_data = self.collection("users").create(data)
            self.user_model = self.auth_store.model
            self.user_token = self.auth_store.token
            self.user_is_valid = True

            return {"response": True,
                    "message": "Success"}

        except pocketbase.client.ClientResponseError as e:
            print("Error with registering account:", repr(e))
            print(e.data)

            error_string = f"Error code: {e.data['code']} -  {e.data['message']} "

            if "email" in e.data["data"].keys():
                error_string += f"(email) {e.data['data']['email']['message']}"
            elif "passwordConfirm" in e.data["data"].keys():
                error_string += f"(password) {e.data['data']['passwordConfirm']['message']}"

            return {"response": False,
                    "message": error_string}

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
            return ({"response": False,
                    "message": "Success"}, self.user_model.forename.capitalize())

        else:
            return ({"response": False,
                    "message": "No user"}, None)

    def get_users_id(self) -> tuple[Response, None | str]:
        if self.user_is_valid:
            return ({"response": False,
                    "message": "Success"}, self.user_model.id)

        else:
            return ({"response": False,
                    "message": "No user"}, None)

    def get_users_surname(self) -> tuple[Response, None | str]:
        if self.user_is_valid:
            return ({"response": False,
                     "message": "Success"}, self.user_model.surname.capitalize())

        else:
            return ({"response": False,
                     "message": "No user"}, None)

    def get_users_fullname(self) -> tuple[Response, None | str]:
        if self.user_is_valid:
            return ({"response": False,
                     "message": "Success"}, f"{self.user_model.forename.capitalize()} " +
                                            f"{self.user_model.surname.capitalize()}")

        else:
            return ({"response": False,
                     "message": "No user"}, None)

    def get_users_email(self) -> tuple[Response, None | str]:
        if self.user_is_valid:
            return {"response": False,
                    "message": "Success"}, self.user_model.email
        else:
            return {"response": False,
                    "message": "No user"}, None

    def check_if_user_exists(self, email_to_check) -> tuple[Response, bool | None]:
        self.refresh_auth()
        if self.user_is_valid:
            try:
                results = self.collection("users").get_full_list(query_params={
                    "filter": f'email="{email_to_check}"'
                })
                if results:
                    return ({"response": True,
                             "message": "Search successful"}, True)
                else:
                    return ({"response": True,
                             "message": "Search successful"}, False)

            except pocketbase.client.ClientResponseError as e:
                print("Error finding user email:", repr(e))
                print(e.data)

                return ({"response": False,
                         "message": "Search for user email failed"}, None)
        else:
            return ({"response": False,
                     "message": "Search for user email failed"}, None)

    def get_full_list_from_collection(self,
                                      collection: str,
                                      query_params: dict = None) -> tuple[Response, list[BaseModel] | None]:

        if query_params is None:
            query_params = {}

        self.refresh_auth()

        if self.user_is_valid:
            try:
                results = self.collection(collection).get_full_list(query_params=query_params)

                return ({"response": True,
                         "message": "success"}, results)

            except pocketbase.client.ClientResponseError as e:
                print(f"Error collecting data from {collection}:", repr(e))
                print(e.data)

                return ({"response": False,
                         "message": f"Error code {e.data['code']}: {e.data['message']}"}, None)

        return ({"response": False,
                 "message": f"Error collecting data from {collection}: User not authorised"}, None)

    def get_single_record(self,
                          collection: str,
                          record_id: str,
                          query_params: dict = None) -> tuple[Response, BaseModel | None]:

        if query_params is None:
            query_params = {}

        self.refresh_auth()

        if self.user_is_valid:
            try:
                result = self.collection(collection).get_one(record_id, query_params=query_params)

                return ({"response": True,
                         "message": "success"}, result)

            except pocketbase.client.ClientResponseError as e:
                print(f"Error collecting data from {collection}:", repr(e))
                print(e.data)

                return ({"response": False,
                         "message": f"Error code {e.data['code']}: {e.data['message']}"}, None)

        return ({"response": False,
                 "message": f"Error collecting data from {collection}: User not authorised"}, None)

    def create_new_record(self,
                          collection: str,
                          record_data: dict) -> tuple[Response, BaseModel | None]:

        self.refresh_auth()

        if self.user_is_valid:
            try:
                result = self.collection(collection).create(record_data)

                return ({"response": True,
                         "message": "success"}, result)

            except pocketbase.client.ClientResponseError as e:
                print(f"Error creating record in {collection}:", repr(e))
                print(e.data)

                return ({"response": False,
                         "message": f"Error code {e.data['code']}: {e.data['message']}"}, None)

        return ({"response": False,
                 "message": f"Error creating data in {collection}: User not authorised"}, None)

    def update_record(self,
                      collection: str,
                      record_id: str,
                      record_data: dict) -> tuple[Response, BaseModel | None]:

        self.refresh_auth()

        if self.user_is_valid:
            try:
                result = self.collection(collection).update(record_id, record_data)

                return ({"response": True,
                         "message": "success"}, result)

            except pocketbase.client.ClientResponseError as e:
                print(f"Error updating record {record_id} in {collection}:", repr(e))
                print(e.data)

                return ({"response": False,
                         "message": f"Error code {e.data['code']}: {e.data['message']}"}, None)

        return ({"response": False,
                 "message": f"Error updating data in {collection}: User not authorised"}, None)

    def delete_record(self,
                      collection: str,
                      record_id: str) -> Response:

        self.refresh_auth()

        if self.user_is_valid:
            try:
                self.collection(collection).delete(record_id)

                return {"response": True,
                        "message": "success"}

            except pocketbase.client.ClientResponseError as e:
                print(f"Error deleting record {record_id} in {collection}:", repr(e))
                print(e.data)

                return {"response": False,
                        "message": f"Error code {e.data['code']}: {e.data['message']}"}

        return {"response": False,
                "message": f"Error deleting data from {collection}: User not authorised"}
