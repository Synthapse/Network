# HTTPS Dedicated Redirector
resource "linode_instance" "edge-redirector-1" {
    label = "edge-redirector-1"
    image = "linode/ubuntu18.04"
    region = "us-east"
    type = "g6-nanode-1"
    authorized_keys = [linode_sshkey.ssh_key.ssh_key]
    root_pass = random_string.random.result

    swap_size = 256
    private_ip = false

    depends_on = []

    connection {
        host = self.ip_address
        user = "root"
        type = "ssh"
        private_key = tls_private_key.temp_key.private_key_pem
        timeout = "10m"
    }

    provisioner "remote-exec" {
    inline = [
      "export PATH=$PATH:/usr/local/bin",
      "export DEBIAN_FRONTEND=noninteractive",
      "apt-get update",
      "yes | apt-get upgrade",
      "touch /tmp/task.complete"
    ]
  }
}

# DNS Dedicated Redirector
resource "linode_instance" "edge-redirector-2" {
    label = "edge-redirector-2"
    image = "linode/ubuntu18.04"
    region = "us-east"
    type = "g6-nanode-1"
    authorized_keys = [linode_sshkey.ssh_key.ssh_key]
    root_pass = random_string.random.result

    swap_size = 256
    private_ip = false

    depends_on = []

    connection {
        host = self.ip_address
        user = "root"
        type = "ssh"
        private_key = tls_private_key.temp_key.private_key_pem
        timeout = "10m"
    }

    provisioner "remote-exec" {
    inline = [
      "export PATH=$PATH:/usr/local/bin",
      "export DEBIAN_FRONTEND=noninteractive",
      "apt-get update",
      "yes | apt-get upgrade",
      "touch /tmp/task.complete"
    ]
  }
}
