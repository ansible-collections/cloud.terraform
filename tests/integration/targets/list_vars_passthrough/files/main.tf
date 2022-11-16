variable "vms" {
  type = list(string)
}

resource "null_resource" "debug" {
  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command = "echo '${jsonencode(var.vms)}' > ${path.module}/out.txt"
  }
}
