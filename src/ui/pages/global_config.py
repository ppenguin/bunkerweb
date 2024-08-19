from base64 import b64encode
from contextlib import suppress
from json import dumps
from threading import Thread
from time import time

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required

from builder.global_config import global_config_builder  # type: ignore

from pages.utils import handle_error, manage_bunkerweb, wait_applying


global_config = Blueprint("global_config", __name__)


@global_config.route("/global-config", methods=["GET", "POST"])
@login_required
def global_config_page():
    if request.method == "POST":
        if current_app.db.readonly:
            return handle_error("Database is in read-only mode", "global_config")

        # Check variables
        variables = request.form.to_dict().copy()
        del variables["csrf_token"]

        # Edit check fields and remove already existing ones
        config = current_app.db.get_config(methods=True, with_drafts=True)
        services = config["SERVER_NAME"]["value"].split(" ")
        for variable, value in variables.copy().items():
            setting = config.get(variable, {"value": None, "global": True})
            if setting["global"] and value == setting["value"]:
                del variables[variable]
                continue

        variables = current_app.bw_config.check_variables(variables, config)

        if not variables:
            return handle_error("The global configuration was not edited because no values were changed.", "global_config", True)

        for variable, value in variables.copy().items():
            for service in services:
                setting = config.get(f"{service}_{variable}", None)
                if setting and setting["global"] and (setting["value"] != value or setting["value"] == config.get(variable, {"value": None})["value"]):
                    variables[f"{service}_{variable}"] = value

        db_metadata = current_app.db.get_metadata()

        def update_global_config(threaded: bool = False):
            wait_applying()

            manage_bunkerweb("global_config", variables, threaded=threaded)

        if "PRO_LICENSE_KEY" in variables:
            current_app.data["PRO_LOADING"] = True

        if any(
            v
            for k, v in db_metadata.items()
            if k in ("custom_configs_changed", "external_plugins_changed", "pro_plugins_changed", "plugins_config_changed", "instances_changed")
        ):
            current_app.data["RELOADING"] = True
            current_app.data["LAST_RELOAD"] = time()
            Thread(target=update_global_config, args=(True,)).start()
        else:
            update_global_config()

        current_app.data["CONFIG_CHANGED"] = True

        with suppress(BaseException):
            if config["PRO_LICENSE_KEY"]["value"] != variables["PRO_LICENSE_KEY"]:
                flash("Checking license key to upgrade.", "success")

        return redirect(
            url_for(
                "loading",
                next=url_for("global_config.global_config_page"),
                message="Saving global configuration",
            )
        )

    global_config = current_app.bw_config.get_config(global_only=True, methods=True)
    plugins = current_app.bw_config.get_plugins()
    builder = global_config_builder({}, plugins, global_config)
    return render_template("global-config.html", data_server_builder=b64encode(dumps(builder).encode("utf-8")).decode("ascii"))