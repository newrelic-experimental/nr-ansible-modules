#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Matt Coddington <coddington@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
import json
import requests

# ===========================================
# Module execution.
#

EXAMPLES = """
- name:  Send Custom Event
  newrelic_ct:
    user_key: AAAAAA //REQUIRED
    attributes: 
      entityGuid: MzY0NzUyM3xBUE18QVBQTElDQVRJT058MTY5NjI2ODY4Mw //REQUIRED
      version: 1.0 //REQUIRED
      changelog: "Added: /v2/deployments.rb, Removed: None" or changelog: "https://github.com/nodejs/node/blob/v4.2.3/CHANGELOG.md"
      description: "deployed something"
      commit: 
      deeplink:
      deploymentType:
      groupId:
      user:
"""
# attributes are optional (EXCEPT FOR entityGuid/version which are required)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user_key=dict(required=True, no_log=True),
            deployment=dict(type="json", required=True),
            # validate_certs=dict(default=True, type='bool'),
        ),
        required_together=[["user_key", "deployment"]],
        supports_check_mode=True,
    )

    # build list of params
    params = {}
    if not module.params["user_key"]:
        module.fail_json(msg="missing user_key")

    def check_keys_exist(dictionary, keys):
        for key in keys:
            if key not in dictionary:
                return False
        return True

    keys_to_check = ["entityGuid", "version"]
    if check_keys_exist(module.params["deployment"], keys_to_check):
        print("All keys exist in the dictionary")
    else:
        module.fail_json(msg="missing version || entityGuid")

    att = json.loads(module.params["deployment"])
    for item in att:
        if att[item] is not None:
            params[item] = att[item]
            
    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=True)

    query = """mutation ($input: ChangeTrackingDeploymentInput!){
                changeTrackingCreateDeployment(deployment: $input) {
                    deploymentId
                    entityGuid
                    version
                    }
                }
            """

    def wrap_numerical_values_as_strings(data):
        if isinstance(data, dict):
            return {
                key: wrap_numerical_values_as_strings(value)
                for key, value in data.items()
            }
        elif isinstance(data, (int, float)):
            return str(data)
        else:
            return data

    wrapped_params = wrap_numerical_values_as_strings(params)

    payload = {"query": query, "variables": {"input": wrapped_params}}
    pay = json.dumps(payload)

    url = "https://api.newrelic.com/graphql"
    headers = {
        "API-Key": module.params["user_key"],
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, data=pay, headers=headers)
    if response.status_code == 200:
        module.exit_json(changed=True, meta=response.status_code)
    else:
        module.exit_json(changed=True, meta=response.status_code)


if __name__ == "__main__":
    main()
