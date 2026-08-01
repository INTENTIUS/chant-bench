# List all of my EC2 and their private ip in a table.

`list-ec-private-ips-all-regions` · the answer aws-bench grades against: **6 instances with private IPs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PrivateIpAddress --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-m2`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[*].Instances[*].[InstanceId, PrivateIpAddress, State.Name]' 2>/dev/null | jq -r '.[] | .[] | @csv' | sort
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[*].Instances[*].[InstanceId, PrivateIpAddress, State.Name]' 2>/dev/null | jq -r '.[] | .[] | @csv' | sort
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[*].Instances[*].[InstanceId, PrivateIpAddress, State.Name]' 2>/dev/null | jq -r '.[] | .[] | @csv' | sort
```

## Terraform — answered

5 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.resources[] | select(.type=="aws_instance") | {address: .address, region: .values.availability_zone | .[:-1], private_ip: .values.private_ip}' | jq -s 'sort_by(.region)'
cd /workspace/terraform && ./terraform state list | head -20
cd /workspace/terraform && ./terraform show -json | jq '.values | [.root_module.resources[], (.root_module.child_modules[] | .resources[])] | map(select(.type=="aws_instance")) | sort_by(.values.availability_zone)'
cd /workspace/terraform && ./terraform show -json | jq '.values | [.root_module.resources[], (.root_module.child_modules[] | .resources[])] | map(select(.type=="aws_instance")) | map({name: .address, region: .values.availability_zone | .[:-1], private_ip: .values.private_ip}) | sort_by(.region)'
cat > /logs/agent/agent-output.txt << 'EOF' EC2 Instances Across Regions ============================= | Instance Name | Region | Private IP | |---------------------------------------------|-----------|-------------| | module.primary.aws_instance.default_vpc_server | us-east-1 | 172.31.32.10 | | module.primary.aws_instance.launch_template_server | us-east-1 | 10.0.0.11 | | module.primary.aws_instance.private_server | us-east-1 | 10.0.1.10 | | module.primary.aws_instance.web_server | us-east-1 | 10.0.0.10 | | module.west1.aws_instance.server | us-west-1 | 10.0.0.10 | | module.west2.aws_instance.server | us-west-2 | 10.0.0.10 | Summary by Region: ================== - us-east-1: 4 instances - us-west-1: 1 instance - us-west-2: 1 instance Total: 6 EC2 instances across 3 regions EOF cat /logs/agent/agent-output.txt
```

## Pulumi — answered

3 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, private_ip: .outputs.privateIp, instance_id: .outputs.id}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::") | .[3], instance_id: .outputs.id, private_ip: .outputs.privateIp, availability_zone: .outputs.availabilityZone}' | jq -s '.'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | "\(.urn | split("::") | .[3])\t\(.outputs.id)\t\(.outputs.privateIp)\t\(.outputs.availabilityZone | .[:-1])"' | sort
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

## Alchemy — answered

7 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state list | grep -E 'Instance|instance' | grep -v 'InstanceProfile|InstanceId|InstanceAttribute|InstanceMetadata'
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && for resource in instance defaultVpcServer ltServer privateServer webServer usw1-server usw2-server; do echo "=== $resource ==="; alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>/dev/null | jq '{kind, output: .output | {id, PrivateIpAddress, region, PublicIpAddress}}' 2>/dev/null | head -20; done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/webServer" | jq '.output'
cd /workspace/alchemy && for resource in instance defaultVpcServer ltServer privateServer webServer usw1-server usw2-server; do alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>/dev/null | jq -r 'select(.output.kind == null or .kind == "AWS::EC2::Instance") | [.output.region // "N/A", .output.InstanceId // .output.id // "N/A", .output.PrivateIp // "N/A"] | @tsv' 2>/dev/null; done
cat > /logs/agent/agent-output.txt << 'EOF' EC2 Instances and Private IPs by Region ======================================== Region | Instance ID | Private IP -------------|--------------------------|------------- us-east-1 | i-921e46837aeb1bc8f | 172.31.32.10 us-east-1 | i-90e9ce2cb766dcb16 | 10.0.0.11 us-east-1 | i-6c989581751564893 | 10.0.1.10 us-east-1 | i-995f3ae70ec3f33e5 | 10.0.0.10 us-west-1 | i-f1d7273a68dfda9c7 | 10.0.0.10 us-west-2 | i-50e1953f84e69d261 | 10.0.0.10 Summary ======= Total Instances: 6 - us-east-1: 4 instances - us-west-1: 1 instance - us-west-2: 1 instance EOF cat /logs/agent/agent-output.txt
```
