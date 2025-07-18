import os
import re
import sys
from dockerspawner import DockerSpawner
from oauthenticator.generic import GenericOAuthenticator
from traitlets.config import Config

c: Config

# Authenticator Configuration
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.client_id = os.getenv('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.getenv('OAUTH_CLIENT_SECRET')
c.GenericOAuthenticator.oauth_callback_url = 'http://airavata.host:20000/hub/oauth_callback'
c.GenericOAuthenticator.authorize_url = 'http://airavata.host:18080/realms/default/protocol/openid-connect/auth'
c.GenericOAuthenticator.token_url = 'http://airavata.host:18080/realms/default/protocol/openid-connect/token'
c.GenericOAuthenticator.userdata_url = 'http://airavata.host:18080/realms/default/protocol/openid-connect/userinfo'
c.GenericOAuthenticator.scope = ['openid', 'profile', 'email']
c.GenericOAuthenticator.username_claim = 'email'

# User Permissions
c.Authenticator.enable_auth_state = True
c.GenericOAuthenticator.allow_all = True
c.Authenticator.admin_users = {'airvata@apache.org'}


# Custom Spawner
class CustomDockerSpawner(DockerSpawner):

    def _options_form_default(self):
        return ""

    def options_from_form(self, formdata):
        options = {}

        if hasattr(self, 'handler') and self.handler:
            qs_args = self.handler.request.arguments  # eg. {'git': [b'https://github...'], 'dataPath': [b'bmtk']}
            if 'git' in qs_args:
                options['git'] = qs_args['git'][0].decode('utf-8')
            if 'dataPath' in qs_args:
                # decode ALL dataPath values into a list of strings
                options['dataPath'] = [v.decode('utf-8') for v in qs_args['dataPath']]

        return options

    def sanitize_name(self, name):
        """Docker safe volume/container names."""
        return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)

    async def start(self):
        # Create a unique volume name keyed by (username + servername).
        # If the user spawns again with the same (servername), it will reuse the same volume.
        safe_user = self.sanitize_name(self.user.name)
        safe_srv = self.sanitize_name(self.name or "default")
        reference_git_url = "https://github.com/cyber-shuttle/cybershuttle-reference.git"
        git_url = self.user_options.get("git") or reference_git_url
        data_subfolders = self.user_options.get("dataPath", [])
        print("THE DATA PATH IS: ", data_subfolders)

        self.image = "cybershuttle/jupyterlab-base"
        if not hasattr(self, "environment"):
            self.environment = {}
        self.environment["GIT_URL"] = git_url
        self.post_start_cmd = "/usr/local/bin/init.sh"
        self.volumes = {}

        # register the home directory as volume (rw)
        vol_name = f"jupyterhub-vol-{safe_user}-{safe_srv}"
        self.volumes[vol_name] = "/home/jovyan/work"

        # register given datasets as volumes (ro)
        for subfolder in data_subfolders:
            host_data_path = f"/mnt/{subfolder}"
            container_path = f"/cybershuttle_data/{subfolder}"
            self.volumes[host_data_path] = {
                'bind': container_path,
                'mode': 'ro'
            }

        return await super().start()


# Spawner Configuration
c.JupyterHub.allow_named_servers = True
c.JupyterHub.named_server_limit_per_user = 10
c.JupyterHub.spawner_class = CustomDockerSpawner
c.DockerSpawner.notebook_dir = '/home/jovyan/work'
c.DockerSpawner.default_url = "/lab"
c.DockerSpawner.start_timeout = 600

c.DockerSpawner.environment = {
    'CHOWN_HOME': 'no',
    'CHOWN_HOME_OPTS': '',
}
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.getenv('DOCKER_NETWORK_NAME', 'jupyterhub_network')

# Hub Configuration
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.shutdown_on_logout = True

# External URL
c.JupyterHub.external_url = 'http://airavata.host:20000'

# Logging
c.JupyterHub.log_level = 'DEBUG'

# Terminate idle notebook containers
c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "admin": True,
        "command": [sys.executable, "-m", "jupyterhub_idle_culler", "--timeout=3600"],
    }
]

c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        "services": ["jupyterhub-idle-culler-service"],
    }
]

# SSL Termination
c.JupyterHub.bind_url = 'http://0.0.0.0:20000'
c.JupyterHub.external_ssl = True

# Custom templates - Login
c.JupyterHub.template_paths = ['/srv/jupyterhub/custom_templates']
c.OAuthenticator.login_service = "Sign in with Existing Institution Credentials"
