# List all of my EC2 and their private ip in a table.

`list-ec-private-ips-all-regions` · the answer aws-bench grades against: **6 instances with private IPs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-i3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show PrivateIpAddress,region --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-i3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json | jq -r '.Reservations[] | .Instances[] | [.InstanceId, .PrivateIpAddress, .State.Name] | @tsv' 2>/dev/null | sort
aws ec2 describe-instances --region us-west-1 --output json | jq -r '.Reservations[] | .Instances[] | [.InstanceId, .PrivateIpAddress, .State.Name] | @tsv' 2>/dev/null | sort
aws ec2 describe-instances --region us-west-2 --output json | jq -r '.Reservations[] | .Instances[] | [.InstanceId, .PrivateIpAddress, .State.Name] | @tsv' 2>/dev/null | sort
```

## Terraform — answered

16 commands, from `terraform-i3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.resources[] | select(.type=="aws_instance") | "\(.address)|\(.values.private_ip)|\(.values.availability_zone)"' 2>/dev/null | head -20
cd /workspace/terraform && ./terraform show -json 2>&1 | jq '.values.root_module.resources[] | select(.type=="aws_instance") | {name: .address, private_ip: .values.private_ip, availability_zone: .values.availability_zone}'
cd /workspace/terraform && ./terraform show -json > /tmp/tf_state.json 2>&1 && echo "State file saved"
jq '.values.root_module.resources[] | select(.type=="aws_instance") | {name: .address, private_ip: .values.private_ip, availability_zone: .values.availability_zone}' /tmp/tf_state.json 2>&1
jq '.values.root_module.resources[0:5]' /tmp/tf_state.json 2>&1 | head -50
jq '.values.root_module.resources[] | select(.type=="aws_instance")' /tmp/tf_state.json 2>&1
jq '.values.root_module | keys' /tmp/tf_state.json 2>&1
jq '.values.root_module.child_modules | map({address: .address, resource_types: [.resources[].type] | unique})' /tmp/tf_state.json 2>&1
jq ' def extract_instances: .address as $module | .resources[] | select(.type=="aws_instance") | { module: $module, name: .address, private_ip: .values.private_ip, availability_zone: .values.availability_zone, instance_id: .values.id }; .values.root_module.child_modules[] | extract_instances ' /tmp/tf_state.json 2>&1
jq -r ' def extract_instances: .address as $module | ($module | if . == "module.primary" then "us-east-1" elif . == "module.west1" then "us-west-1" elif . == "module.west2" then "us-west-2" else . end) as $region | .resources[] | select(.type=="aws_instance") | [ $region, .values.id, .address | split(".") | .[-1], .values.private_ip, .values.availability_zone ] | @csv; "Region,Instance ID,Instance Name,Private IP,Availability Zone", (.values.root_module.child_modules[] | extract_instances) ' /tmp/tf_state.json 2>&1
jq 'type' /tmp/tf_state.json 2>&1
cat > /tmp/extract_instances.jq << 'EOF' def extract_instances: .address as $module | ($module | if . == "module.primary" then "us-east-1" elif . == "module.west1" then "us-west-1" elif . == "module.west2" then "us-west-2" else . end) as $region | .resources[] | select(.type=="aws_instance") | [ $region, .values.id, (.address | split(".") | .[-1]), .values.private_ip, .values.availability_zone ]; "Region,Instance ID,Instance Name,Private IP,Availability Zone", (.values.root_module.child_modules[] | extract_instances | @csv) EOF jq -rRf /tmp/extract_instances.jq /tmp/tf_state.json 2>&1
# … 4 more
```

## Pulumi — answered

3 commands, from `pulumi-i3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, privateIp: .outputs.privateIp, availabilityZone: .outputs.availabilityZone}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[-1]), region: (.outputs.availabilityZone | .[:-1]), privateIp: .outputs.privateIp} | [.name, .region, .privateIp] | @csv' | sort
cat > /tmp/ec2_table.txt << 'EOF' EC2 Instances and Private IPs by Region ======================================== EOF # Add the table header cat >> /tmp/ec2_table.txt << 'EOF' Instance Name Region Private IP ===================================================== EOF # Add the data rows sorted by region then instance name cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[-1]), region: (.outputs.availabilityZone | .[:-1]), privateIp: .outputs.privateIp} | "\(.name | @json) \(.region | @json) \(.privateIp | @json)"' | sort | while read line; do name=$(echo "$line" | cut -d' ' -f1 | tr -d '"') region=$(echo "$line" | cut -d' ' -f2 | tr -d '"') ip=$(echo "$line" | cut -d' ' -f3 | tr -d '"') printf "%-21s %-13s %s\n" "$name" "$region" "$ip" done >> /tmp/ec2_table.txt cat /tmp/ec2_table.txt
```

## AWS CDK — answered

11 commands, from `cdk-i1`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}' > /tmp/instances-us-east-1.json && cat /tmp/instances-us-east-1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}' > /tmp/instances-us-west-1.json && cat /tmp/instances-us-west-1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}' > /tmp/instances-us-west-2.json && cat /tmp/instances-us-west-2.json
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Status: .ResourceStatus}'
aws ec2 describe-instances --instance-ids i-8efe413fb2db04cc6 i-7d9001a08d554ad03 i-c4deff6351c208ad9 i-2406a03b9ade076f4 --region us-east-1 2>/dev/null | jq '.Reservations[] | .Instances[] | {InstanceId: .InstanceId, InstanceType: .InstanceType, PrivateIpAddress: .PrivateIpAddress, State: .State.Name, AZ: .Placement.AvailabilityZone}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-fde88288e4fcb0f27 --region us-west-1 2>/dev/null | jq '.Reservations[] | .Instances[] | {InstanceId: .InstanceId, InstanceType: .InstanceType, PrivateIpAddress: .PrivateIpAddress, State: .State.Name, AZ: .Placement.AvailabilityZone}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-c18071845f3e04292 --region us-west-2 2>/dev/null | jq '.Reservations[] | .Instances[] | {InstanceId: .InstanceId, InstanceType: .InstanceType, PrivateIpAddress: .PrivateIpAddress, State: .State.Name, AZ: .Placement.AvailabilityZone}'
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances Across All Regions ## Summary Total EC2 Instances: 6 | Instance ID | Region | Availability Zone | Instance Type | Private IP Address | State | |---|---|---|---|---|---| | i-8efe413fb2db04cc6 | us-east-1 | us-east-1a | t3.micro | 10.0.0.10 | running | | i-7d9001a08d554ad03 | us-east-1 | us-east-1a | t3.micro | 172.31.0.10 | running | | i-c4deff6351c208ad9 | us-east-1 | us-east-1a | t3.micro | 10.0.1.10 | running | | i-2406a03b9ade076f4 | us-east-1 | us-east-1a | t3.micro | 10.0.0.11 | running | | i-fde88288e4fcb0f27 | us-west-1 | us-west-1a | t3.micro | 10.0.0.10 | running | | i-c18071845f3e04292 | us-west-2 | us-west-2a | t3.micro | 10.0.0.10 | running | ## Breakdown by Region ### us-east-1 (4 instances) | Instance ID | Private IP Address | |---|---| | i-8efe413fb2db04cc6 | 10.0.0.10 | | i-7d9001a08d554ad03 | 172.31.0.10 | | i-c4deff6351c208ad9 | 10.0.1.10 | | i-2406a03b9ade076f4 | 10.0.0.11 | ### us-west-1 (1 instance) | Instance ID | Private IP Address | |---|---| | i-fde88288e4fcb0f27 | 10.0.0.10 | ### us-west-2 (1 instance) | Instance ID | Private IP Address | |---|---| | i-c18071845f3e04292 | 10.0.0.10 | EOF cat /logs/agent/agent-output.txt
```

## Alchemy — answered

8 commands, from `alchemy-i3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i "aws::instance"
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && for name in defaultVpcServer webServer ltServer privateServer usw1-server usw2-server; do echo "=== $name ==="; alchemy state get "alchemy-ec2-multiregion/bench/$name" 2>/dev/null | jq -r '.kind, .output.id, .output.privateIpAddress, .output.region // "unknown"' | head -10; done
cd /workspace/alchemy && for name in defaultVpcServer webServer ltServer privateServer usw1-server usw2-server; do echo "=== $name ==="; alchemy state get "alchemy-ec2-multiregion/bench/$name" 2>/dev/null | jq '.output | {id, privateIpAddress, region}'; done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/defaultVpcServer" 2>/dev/null | jq '.output | keys'
cd /workspace/alchemy && for name in defaultVpcServer webServer ltServer privateServer usw1-server usw2-server; do alchemy state get "alchemy-ec2-multiregion/bench/$name" 2>/dev/null | jq -r '.output | [.InstanceId, .PrivateIp, .region] | @csv'; done
cat > /logs/agent/agent-output.txt << 'EOF' EC2 Instances and Private IPs by Region ======================================== | Instance ID | Private IP | Region | |------------------------|---------------|------------| | i-f790634a64f31b54d | 172.31.32.10 | us-east-1 | | i-22d6ee20dfcf1a449 | 10.0.0.10 | us-east-1 | | i-75367a863c9a41c2a | 10.0.0.11 | us-east-1 | | i-b0486cc893ddd7bfa | 10.0.1.10 | us-east-1 | | i-6bec89de8180a8f42 | 10.0.0.10 | us-west-1 | | i-df124de17e5a70593 | 10.0.0.10 | us-west-2 | Summary ------- Total EC2 Instances: 6 By Region: - us-east-1: 4 instances - us-west-1: 1 instance - us-west-2: 1 instance EOF cat /logs/agent/agent-output.txt
```

## Alchemy v2 (Effect) — missed

5 commands, from `alchemy-effect-i3`.

```sh
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq -r '.resources[] | select(.resourceType == "aws:ec2:instance") | {stack: .stack, instanceId: .state.id, privateIp: .state.privateIpAddress} | @json' | head -20
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>&1 | head -50
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>&1 | jq -r '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | [.stack | sub("alchemy-effect-ec2-multiregion-"; ""), .state.attr.instanceId, .state.attr.privateIpAddress] | @csv'
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>&1 | jq -r '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | [(.stack | sub("alchemy-effect-ec2-multiregion-"; "")), .state.attr.instanceId, .state.attr.privateIpAddress] | @csv'
cd /workspace/alchemy && { echo "Region,Instance ID,Private IP" alchemy state export us-west-1.run.ts --local 2>&1 | jq -r '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | [(.stack | sub("alchemy-effect-ec2-multiregion-"; "")), .state.attr.instanceId, .state.attr.privateIpAddress] | @csv' | sed 's/"//g' } > /logs/agent/agent-output.txt && cat /logs/agent/agent-output.txt
```
