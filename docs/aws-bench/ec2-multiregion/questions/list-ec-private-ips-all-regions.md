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

4 commands, from `bare-m3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,State.Name]' | jq -r '.[][] | @csv' > /tmp/ec2_us_east_1.csv 2>&1 && echo "us-east-1 done" || echo "us-east-1 error"
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,State.Name]' | jq -r '.[][] | @csv' > /tmp/ec2_us_west_1.csv 2>&1 && echo "us-west-1 done" || echo "us-west-1 error"
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,State.Name]' | jq -r '.[][] | @csv' > /tmp/ec2_us_west_2.csv 2>&1 && echo "us-west-2 done" || echo "us-west-2 error"
{ echo "Region | Instance ID | Private IP | State" echo "-------|-------------|------------|-------" # Process us-east-1 while IFS=',' read -r instance_id private_ip state; do instance_id=$(echo "$instance_id" | tr -d '"') private_ip=$(echo "$private_ip" | tr -d '"') state=$(echo "$state" | tr -d '"') echo "us-east-1 | $instance_id | $private_ip | $state" done < /tmp/ec2_us_east_1.csv # Process us-west-1 while IFS=',' read -r instance_id private_ip state; do instance_id=$(echo "$instance_id" | tr -d '"') private_ip=$(echo "$private_ip" | tr -d '"') state=$(echo "$state" | tr -d '"') echo "us-west-1 | $instance_id | $private_ip | $state" done < /tmp/ec2_us_west_1.csv # Process us-west-2 while IFS=',' read -r instance_id private_ip state; do instance_id=$(echo "$instance_id" | tr -d '"') private_ip=$(echo "$private_ip" | tr -d '"') state=$(echo "$state" | tr -d '"') echo "us-west-2 | $instance_id | $private_ip | $state" done < /tmp/ec2_us_west_2.csv } > /logs/agent/agent-output.txt cat /logs/agent/agent-output.txt
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

3 commands, from `cdk-m2`.

```sh
aws ec2 describe-instances --region us-east-1 --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name,Tags[?Key==`Name`].Value|[0]]' --output json 2>/dev/null
aws ec2 describe-instances --region us-west-1 --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name,Tags[?Key==`Name`].Value|[0]]' --output json 2>/dev/null
aws ec2 describe-instances --region us-west-2 --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name,Tags[?Key==`Name`].Value|[0]]' --output json 2>/dev/null
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

## Alchemy v2 (Effect) — answered

11 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && \ for stack in alchemy-effect-ec2-multiregion-us-east-1 alchemy-effect-ec2-multiregion-us-west-1 alchemy-effect-ec2-multiregion-us-west-2; do echo "=== Stack: $stack ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local | grep -i instance || true done
cd /workspace/alchemy && \ for stack in alchemy-effect-ec2-multiregion-us-east-1 alchemy-effect-ec2-multiregion-us-west-1 alchemy-effect-ec2-multiregion-us-west-2; do echo "=== Stack: $stack ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local | head -30 done
for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" stack_dir="/workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-${region}/bench" ls "$stack_dir" | grep -i instance || true done
for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" stack_dir="/workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-${region}/bench" for file in "$stack_dir"/*.json; do if jq -e '.resourceType == "AWS::EC2::Instance"' "$file" > /dev/null 2>&1; then echo "Found instance: $(basename $file)" fi done done
for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" stack_dir="/workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-${region}/bench" jq -r '.resourceType' "$stack_dir"/*.json 2>/dev/null | sort -u done
for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" stack_dir="/workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-${region}/bench" for file in "$stack_dir"/*.json; do resource_type=$(jq -r '.resourceType' "$file" 2>/dev/null) if [ "$resource_type" = "AWS.EC2.Instance" ] || [ "$resource_type" = "AWS.EC2.LaunchTemplateInstance" ]; then name=$(jq -r '.name' "$file" 2>/dev/null) instance_id=$(jq -r '.attr.InstanceId // .attr.id' "$file" 2>/dev/null) private_ip=$(jq -r '.attr.PrivateIp' "$file" 2>/dev/null) echo "Name: $name, Type: $resource_type, Instance ID: $instance_id, Private IP: $private_ip" fi done done
stack_dir="/workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench" for file in "$stack_dir"/*.json; do resource_type=$(jq -r '.resourceType' "$file" 2>/dev/null) if [ "$resource_type" = "AWS.EC2.Instance" ]; then echo "File: $(basename $file)" jq '.' "$file" 2>/dev/null | head -50 break fi done
cat > /tmp/get_instances.sh << 'EOF' #!/bin/bash # Create a combined list of all instances across regions declare -a instances for region in us-east-1 us-west-1 us-west-2; do stack_dir="/workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-${region}/bench" for file in "$stack_dir"/*.json; do resource_type=$(jq -r '.resourceType' "$file" 2>/dev/null) if [ "$resource_type" = "AWS.EC2.Instance" ] || [ "$resource_type" = "AWS.EC2.LaunchTemplateInstance" ]; then logical_id=$(jq -r '.logicalId' "$file" 2>/dev/null) instance_id=$(jq -r '.attr.instanceId' "$file" 2>/dev/null) private_ip=$(jq -r '.attr.privateIpAddress' "$file" 2>/dev/null) tag_name=$(jq -r '.attr.tags.Name // "N/A"' "$file" 2>/dev/null) if [ -n "$instance_id" ] && [ "$instance_id" != "null" ]; then echo "$region|$logical_id|$tag_name|$instance_id|$private_ip" fi fi done done EOF chmod +x /tmp/get_instances.sh /tmp/get_instances.sh
cat > /tmp/format_table.py << 'EOF' #!/usr/bin/env python3 import sys # Get the data instances = [ ("us-east-1", "DefaultVpcServer", "MyEC2Instance", "i-866ecbcb0c3539eb6", "172.31.32.10"), ("us-east-1", "LaunchTemplateServer", "N/A", "i-6e2bfa2e69398375f", "10.0.0.11"), ("us-east-1", "PrivateServer", "PrivateInstance", "i-82022bfe3dc0ef2c8", "10.0.1.10"), ("us-east-1", "WebServer", "WebServerInstance", "i-44aad298d11867aa6", "10.0.0.10"), ("us-west-1", "WebServer", "WebServerInstance", "i-583215fd3a2732541", "10.0.0.10"), ("us-west-2", "WebServer", "WebServerInstance", "i-c55cdc877c08961ad", "10.0.0.10"), ] # Sort by region and logical ID instances.sort(key=lambda x: (x[0], x[1])) # Create table headers = ["Region", "Logical ID", "Name Tag", "Instance ID", "Private IP"] col_widths = [max(len(h), max(len(str(row[i])) for row in instances)) for i, h in enumerate(headers)] # Print header header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) print(header_line) print("-" * len(header_line)) # Print rows for row in instances: print(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers)))) print("\nTotal EC2 Instances: {}".format(len(instances))) EOF python3 /tmp/format_table.py
```
