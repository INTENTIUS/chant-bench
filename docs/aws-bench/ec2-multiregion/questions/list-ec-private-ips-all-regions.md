# List all of my EC2 and their private ip in a table.

`list-ec-private-ips-all-regions` · the answer aws-bench grades against: **6 instances with private IPs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1" --at latest --env floci --show PrivateIpAddress,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1" --at latest --env floci --show PrivateIpAddress,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2" --at latest --env floci --show PrivateIpAddress,region --explain
```

## Terraform — answered

2 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type=="aws_instance") | {address: .address, region: .values.availability_zone, private_ip: .values.private_ip, public_ip: .values.public_ip, instance_id: .values.id}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type=="aws_instance") | {region: .values.availability_zone | .[:-1], instance_id: .values.id, private_ip: .values.private_ip, resource: .address}' | jq -s 'sort_by(.region, .instance_id) | .[] | "\(.region | ascii_upcase)\t\(.instance_id)\t\(.private_ip)\t\(.resource)"' -r
```

## Pulumi — answered

1 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn, region: .outputs.availabilityZone | sub("[a-z]$"; ""), privateIp: .outputs.privateIp}' | jq -s 'sort_by(.region, .name)'
```

## AWS CDK — answered

3 commands, from `cdk-m2`.

```sh
aws ec2 describe-instances --region us-east-1 --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name,Tags[?Key==`Name`].Value|[0]]' --output json 2>/dev/null
aws ec2 describe-instances --region us-west-1 --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name,Tags[?Key==`Name`].Value|[0]]' --output json 2>/dev/null
aws ec2 describe-instances --region us-west-2 --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name,Tags[?Key==`Name`].Value|[0]]' --output json 2>/dev/null
```
