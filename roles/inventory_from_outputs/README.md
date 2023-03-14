inventory_from_outputs
==================

A role to create an in-memory inventory from Terraform outputs.

Requirements
------------

- NA

Role Variables
--------------

* **project_path**: The path to the root of the Terraform directory with the .tfstate file. If not set, the current working directory is used as a Terraform directory.
* **state_file**: The path to an existing Terraform state file. If not set, terraform.tfstate in selected directory is used.
* **mapping_variables**: Names that define the mapping between Terraform output variables and inventory host variables. Contains the following:
  - **host_list**: (Required) The Terraform variable that contains the list of hosts to be processed into the in-memory inventory. Other keys in the mapping_variables parameter refer to properties of the items of this list.
  - **name**: (Required) The Terraform variable that contains the name of the resulting inventory host.
  - **ip**: (Required) The Terraform variable that contains the IP or hostname of the resulting inventory host. Maps directly to ansible_host.
  - **user**: (Required) The Terraform variable that contains the username of the resulting inventory host. Maps directly to ansible_user.
  - **group**: (Required) The Terraform variable that contains the group the resulting host will be a member of.

Limitations
------------

- NA

Dependencies
------------

- NA

Example Playbook
----------------

    - hosts: localhost
      roles:
        - role: cloud.terraform.inventory_from_outputs
          project_path: 'my_project_directory'
          mapping_variables:
            host_lists: terraform_var_host_list
            name: terraform_var_name
            ip: terraform_var_ip
            user: terraform_var_user
            group: terraform_var_group

License
-------

GNU General Public License v3.0 or later

See [LICENSE](https://github.com/ansible-collections/cloud.terraform/blob/main/LICENSE) to see the full text.
