.. _ansible_collections.cloud.terraform.docsite.guide_aap:

*************************************************************
Using cloud.terraform in Ansible Automation Platform
*************************************************************

The ``cloud.terraform`` collection requires some extra configuration to run in `Ansible Automation Platform (AAP) <https://www.redhat.com/en/technologies/management/ansible>`_; in particular the default execution environment in AAP does not include a Terraform binary due to `Terraform licensing restrictions <https://www.hashicorp.com/license-faq>`_. You must create an execution environment containing a Terraform binary in order to run any Terraform commands from within AAP.

In addition, a remote Terraform backend should be used to store Terraform state as any local state files created in AAP jobs are ephemeral. The Terraform backend credential type allows secure storage of remote backend configuration to enable this.

=====================
Execution Environment
=====================

Job templates and inventory source syncs using the ``cloud.terraform`` collection in AAP must be run in an execution environment containing a Terraform binary. You can create one using `ansible-builder <https://ansible.readthedocs.io/projects/builder/en/latest/#>`_ following the instructions below.

Instructions
------------

1. Install ansible-builder:

.. code-block:: console

    pip install ansible-builder

2. Create an execution-environment.yml configuration similar to this example. Note the inclusion of the ``cloud.terraform`` collection and the ``additional_build_steps`` section that downloads and installs Terraform.

.. code-block:: yaml

    ---
    version: 3

    images:
    base_image:
      name: quay.io/centos/centos:stream9

    dependencies:
    ansible_core:
      package_pip: ansible-core
    ansible_runner:
      package_pip: ansible-runner
    galaxy:
      collections:
        - name: cloud.terraform

    additional_build_steps:
    append_base: |
      RUN yum install -y git
      RUN curl https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo | tee /etc/yum.repos.d/terraform.repo
      RUN yum install -y terraform

3. Build the execution environment image:

.. code-block:: console

    ansible-builder build

The Containerfile/Dockerfile and build files should now be in ``/context`` and you can see your newly created image in podman or docker:

.. code-block:: console

    podman images

    REPOSITORY                       TAG         IMAGE ID      CREATED         SIZE
    localhost/ansible-execution-env  latest      2976756bc5f3  5 seconds ago   521 MB
    <none>                           <none>      74ac0ff084f1  14 seconds ago  523 MB
    <none>                           <none>      2498e29966ee  21 seconds ago  521 MB
    quay.io/centos/centos            stream9     94714b8dc9d7  2 days ago      168 MB


4. Publish the image:

.. code-block:: console

    podman login quay.io
    podman push localhost/ansible-execution-env quay.io/<username>/<repository>

5. You can now add the execution environment to your AAP instance and use it in job templates and inventory sources. Refer to the `Automation Controller User Guide <https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.4/html/automation_controller_user_guide/index>`_ for information on using execution environments in jobs.

===========
Credentials
===========

Using built-in cloud credentials in AAP
---------------------------------------

When running job templates that use ``cloud.terraform`` to deploy cloud resources, the built-in `credential types <https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.4/html/automation_controller_user_guide/controller-credentials#ref-controller-credential-types>`_ can be used to securely store and pass cloud credentials to those jobs as environment variables. However, the built-in Azure and GCE credential types store env variables that are slightly different from the ones Terraform expects (the AWS credential type stores env variables that Terraform can read as is). To use the Azure and GCE credentials, you can pass the Ansible ``environment`` option to provide new env variables to playbooks using the env variables from stored credentials. Here is an example converting the relevant Azure and GCE env variables in a playbook using ``cloud.terraform.terraform`` to deploy resources:

.. code-block:: yaml

    ---
    - name: Terraform apply
      hosts: localhost
      environment:
        ARM_SUBSCRIPTION_ID: "{{ lookup('ansible.builtin.env', 'AZURE_SUBSCRIPTION_ID') }}"
        ARM_TENANT_ID: "{{ lookup('ansible.builtin.env', 'AZURE_TENANT') }}"
        ARM_CLIENT_ID: "{{ lookup('ansible.builtin.env', 'AZURE_CLIENT_ID') }}"
        ARM_CLIENT_SECRET: "{{ lookup('ansible.builtin.env', 'AZURE_SECRET') }}"
        GOOGLE_CREDENTIALS: "{{ lookup('ansible.builtin.env', 'GCE_CREDENTIALS_FILE_PATH') }}"
      tasks:
        - name: Run Terraform apply
          cloud.terraform.terraform:
            project_path: '{{ project_dir }}'
            state: present
            force_init: true

----------------------------
Terraform backend credential
----------------------------

The Terraform backend credential type in AAP allows secure storage of a Terraform backend configuration, which can be provided to playbooks using the ``cloud.terraform`` modules to configure and use the remote backend. This credential is also required to use the Terraform state inventory source in AAP, which creates Ansible hosts from a Terraform state file and thus needs access to the remote backend configuration. Refer to the `Automation Controller User Guide <https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.4/html/automation_controller_user_guide/index>`_ for details on creating and using this credential type. An example job using the credential type with an S3 backend would look something like this:

Terraform configuration file:

.. code-block:: hcl

    terraform {

      backend "s3" {} # Note empty backend configuration, just specifying the type

      required_providers {
        aws = {
          source = "hashicorp/aws"
          version = "5.34.0"
        }
    }

    provider "aws" {
      region = "us-east-1"
    }

    resource "aws_instance" "test" {
      ami           = "ami-0a3c3a20c09d6f377"
      instance_type = "t2.micro"

      tags = {
        Name = "Test AWS Instance"
      }
    }

Contents of Terraform backend credential in AAP:

.. code-block:: hcl

    bucket = "my-terraform-state-bucket"
    key = "path/to/terraform-state-file"
    region = "us-east-1"
    access_key = "my-aws-access-key"
    secret_key = "my-aws-secret-access-key"

Playbook file:

.. code-block:: yaml

    ---
    - name: Terraform apply
      hosts: localhost
      tasks:
        - name: Run Terraform apply using Terraform backend credential to supply backend config
          cloud.terraform.terraform:
          project_path: '{{ project_dir }}'
          state: present
          force_init: true
          backend_config_files:
            - "{{ lookup('ansible.builtin.env', 'TF_BACKEND_CONFIG_FILE') }}" # Note use of the env variable set by the Terraform backend credential to store the backend configuration file path
