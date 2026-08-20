output "instance_public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.web_server.public_ip
}

output "ssh_connection_string" {
  description = "Command to connect to the instance"
  value       = "ssh -i ~/.ssh/tf_key ec2-user@${aws_instance.web_server.public_ip}"
}
output "vpc_id" {
  value = aws_vpc.main_vpc.id
}
output "subnet_id" {
  value = aws_subnet.public_subnet.id
}

output "ami_id" {
  value = data.aws_ami.amazon_linux_2023.id
}