git_plan
==================

Clone a Git repository and apply a plan from it.

Requirements
------------

- NA

Role Variables
--------------

* **project_path**: The path to the root of the Terraform directory with the .tfstate file. *Mutually exclusive with state_file*.
* **state_file**: An absolute path to an existing Terraform state file. *Mutually exclusive with project_path*.
* **mapping_variables**: Names that define the mapping between Terraform output variables and inventory host variables. Contains the following:
  - **host_list**: (Required) The Terraform variable that contains the list of hosts to be processed into the in-memory inventory. Other keys in the mapping_variables parameter refer to properties of the items of this list.
  - **name**: (Required) The Terraform variable that contains the name of the resulting inventory host.
  - **ip**: (Required) The Terraform variable that contains the IP or hostname of the resulting inventory host. Maps directly to ansible_host.
  - **user**: (Required) The Terraform variable that contains the username of the resulting inventory host. Maps directly to ansible_user.
  - **group**: (Required) The Terraform variable that contains the group the resulting host will be a member of.

* **repo_url**: (Required) The URL of the repository to clone.
* **repo_dir**: (Required) The directory to clone the Git repository into.
* **version**: The ref of the repository to use. Defaults to the remote HEAD.
* **plan_file**: (Required) The plan file to use. This must exist.
* **git_options**: Options to configure ansible.builtin.git. Names correspond to module arguments. See ansible.builtin.git documentation for details.
* **terraform_options**: Parameters for module cloud.terraform.terraform. See cloud.terraform.terraform documentation for details.

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
        - role: cloud.terraform.git_plan
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

See [LICENSE](https://github.com/ansible-collections/cloud.terraform/blob/stable-3/LICENSE) to see the full text.
