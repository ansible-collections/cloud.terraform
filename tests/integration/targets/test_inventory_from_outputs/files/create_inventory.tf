output "myvar_hostlist" {
  value = [
    { "myvar_ip" : "my_ip1", "myvar_group" : "my_group1", "myvar_name" : "my_name1", "myvar_user" : "my_user" },
    { "myvar_ip" : "my_ip2", "myvar_group" : "my_group2", "myvar_name" : "my_name2", "myvar_user" : "my_user" },
    { "myvar_ip" : "my_ip3", "myvar_group" : "my_group1", "myvar_name" : "my_name3", "myvar_user" : "my_user" },
  ]
}
