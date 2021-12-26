from .change_user_params import ChangeUserParams
from .logout import Logout
from .refresh_token import RefreshToken
from .role import Role
from .role_manipulation import RoleManipulation
from .sign_in import SignIn
from .sign_up import SignUp
from .user_history import UserHistory

urls = [
    (SignIn, "/api/v1/user/sign_in"),
    (SignUp, "/api/v1/user/sign_up"),
    (RefreshToken, "/api/v1/user/refresh"),
    (Logout, "/api/v1/user/sign_out"),
    (ChangeUserParams, "/api/v1/user/change"),
    (UserHistory, "/api/v1/user/history"),
    (RoleManipulation, "/api/v1/user/role"),
    (Role, "/api/v1/access/role"),
]
