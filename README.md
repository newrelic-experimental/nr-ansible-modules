[![New Relic Experimental header](https://github.com/newrelic/opensource-website/raw/master/src/images/categories/Experimental.png)](https://opensource.newrelic.com/oss-category/#new-relic-experimental)

# New Relic Ansible modules (nr-ansible-modules)

Ansible modules to ineract with newrelic apis

## Requirements/Versions
- ansible v[core 2.12.9]
- python3 v[3.8]

## Modules: 
- newrelic_custom_event
- newrelic_ct (change tracking)
## Adding a Module
 Copy the relevant module into your ansible modules folder and reference it in your ansible.cfg 
## Module Configurations
newrelic_custom_event:
- Configure a playbook with the below task
```yaml
- name: Send Custom Event
    newrelic_custom_event:
      insert_key: <insert_key>
      account_id: <account_id>
      event_type: <event_name>
      attributes:
        att1: <value>
        att2: <value>
        att3: <value>
```
newrelic_ct:
- Configure a plabook with the below task
```yaml
- name: Send Change Tracking Event
    newrelic_ct:
      user_key: <user_key>
      deployment:
        entityGuid: MzY0NzUyM3xBUE18QVBQTElDQVRJT058MTY5NjI2ODY4Mw
        version: 2.2
        user: some@user
        description: magic fix
```
### Usage
- Send custom events from within your playbook to monitor key metrics/events generated from your ansible playbooks. i.e. task status, time taken between tasks, playbook fails
- Send Change Tracking Events from within your playbook
## Support

New Relic hosts and moderates an online forum where customers can interact with New Relic employees as well as other customers to get help and share best practices. Like all official New Relic open source projects, there's a related Community topic in the New Relic Explorers Hub. You can find this project's topic/threads here:

>Raise any issues/feature requests through GitHub issues

## Contributing
We encourage your contributions to improve nr-ansible-modules! Keep in mind when you submit your pull request, you'll need to sign the CLA via the click-through using CLA-Assistant. You only have to sign the CLA one time per project.
If you have any questions, or to execute our corporate CLA, required if your contribution is on behalf of a company,  please drop us an email at opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed to the privacy and security of our customers and their data. We believe that providing coordinated disclosure by security researchers and engaging with the security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of New Relic's products or websites, we welcome and greatly appreciate you reporting it to New Relic through [HackerOne](https://hackerone.com/newrelic).

## License
nr-ansible-modules is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.

