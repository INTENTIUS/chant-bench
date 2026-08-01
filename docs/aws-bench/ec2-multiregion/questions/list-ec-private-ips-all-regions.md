# List all of my EC2 and their private ip in a table.

`list-ec-private-ips-all-regions` · the answer aws-bench grades against: **6 instances with private IPs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show PrivateIpAddress,region --explain
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

11 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | keys[] as $k | select(.Resources[$k].Type == "AWS::EC2::Instance") | .Resources[$k]' 2>/dev/null || npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {id: .key, resource: .value}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/template-us-east-1.json && cat /tmp/template-us-east-1.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/template-us-west-1.json && cat /tmp/template-us-west-1.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/template-us-west-2.json && cat /tmp/template-us-west-2.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-99224a9cff337e5b0 i-5fdf2028dd5a7a28d i-f5d8c3aa998285b73 i-754790856a4ef8150 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, PrivateIp: .PrivateIpAddress, State: .State.Name, InstanceType: .InstanceType}'
aws ec2 describe-instances --instance-ids i-c52758030f5620e05 --region us-west-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, PrivateIp: .PrivateIpAddress, State: .State.Name, InstanceType: .InstanceType}'
aws ec2 describe-instances --instance-ids i-e1c4d75f234795b0a --region us-west-2 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, PrivateIp: .PrivateIpAddress, State: .State.Name, InstanceType: .InstanceType}'
```
