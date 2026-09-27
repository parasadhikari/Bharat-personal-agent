class PermissionManager:

    def __init__(self):
        self.permissions = {}

    def request(self, permission_id):
        return {
            "required": True,
            "permission_id": permission_id
        }

    def grant(self, permission_id):
        self.permissions[permission_id] = True

    def deny(self, permission_id):
        self.permissions[permission_id] = False

    def allowed(self, permission_id):
        return self.permissions.get(permission_id, False)