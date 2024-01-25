#!/usr/bin/env bash
set -eux

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mkdir -p "${SCRIPT_DIR}/.collection_root/ansible_collections/cloud"
ln -s -n "${SCRIPT_DIR}" "${SCRIPT_DIR}/.collection_root/ansible_collections/cloud/terraform"
cd "${SCRIPT_DIR}/.collection_root/ansible_collections/cloud/terraform/"
export MYPYPATH="${SCRIPT_DIR}/.collection_root"
mypy -p ansible_collections.cloud.terraform.plugins
rm -rf "${SCRIPT_DIR}/.collection_root"