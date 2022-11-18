#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Matt Coddington <coddington@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.six.moves.urllib.parse import quote
import json

# ===========================================
# Module execution.
#

EXAMPLES = '''
- name:  Send Custom Event
  newrelic_custom_event:
    insert_key: AAAAAA
    event_type: AnsibleTestEvent
    account_id: 123456
    attributes:
      value: 1
      value2: 3
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            insert_key=dict(required=True, no_log=True),
            account_id=dict(required=True),
            event_type=dict(required=True),
            attributes=dict(type="json", required=False),
            validate_certs=dict(default=True, type='bool'),
        ),
        required_together=[['insert_key','event_type','account_id']],
        supports_check_mode=True
    )
    
 
    # build list of params
    params = {}
    if not module.params["insert_key"] and not module.params["event_type"] and not module.params["account_id"]:
        module.fail_json(msg="you need to add insert key and event type")

    params["eventType"] = module.params["event_type"]
    att = json.loads(module.params["attributes"])
    
    for item in att:
        if att[item] is not None:
            params[item] = att[item]
    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=True)
    # Post Custom Event to New relic
    url = "https://insights-collector.newrelic.com/v1/accounts/%s/events" % quote(str(module.params["account_id"]), safe='')
    data = [params]
    headers = {
        'X-Insert-Key': module.params["insert_key"],
        'Content-Type': 'application/json',
    }
    response, info = fetch_url(module, url, data=module.jsonify(data), headers=headers, method="POST")
    if info['status'] in (200, 201):
        module.exit_json(changed=True)
    else:
        module.fail_json(msg="Unable to post custom event: %s" % info['msg'])

if __name__ == '__main__':
    main()