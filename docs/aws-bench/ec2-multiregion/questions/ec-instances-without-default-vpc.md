# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

2 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show VpcId,providerDefault,region
```

## No tool (AWS CLI) — answered

6 commands, from `bare-m3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json | jq -r '.Reservations[].Instances[] | {InstanceId, VpcId, Region: "us-east-1"}' > /tmp/instances_east.json && cat /tmp/instances_east.json
aws ec2 describe-instances --region us-west-1 --output json | jq -r '.Reservations[].Instances[] | {InstanceId, VpcId, Region: "us-west-1"}' > /tmp/instances_west1.json && cat /tmp/instances_west1.json
aws ec2 describe-instances --region us-west-2 --output json | jq -r '.Reservations[].Instances[] | {InstanceId, VpcId, Region: "us-west-2"}' > /tmp/instances_west2.json && cat /tmp/instances_west2.json
aws ec2 describe-vpcs --region us-east-1 --output json | jq '.Vpcs[] | {VpcId, IsDefault}'
aws ec2 describe-vpcs --region us-west-1 --output json | jq '.Vpcs[] | {VpcId, IsDefault}'
aws ec2 describe-vpcs --region us-west-2 --output json | jq '.Vpcs[] | {VpcId, IsDefault}'
```

## Terraform — answered

14 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type == "aws_instance") | {address, values: .values | {id, vpc_id, subnet_id, primary_network_interface_id}}' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type == "aws_subnet" or .type == "aws_vpc") | {address, type, values: .values | {id, vpc_id, is_default, default_network_acl_id}}' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type == "aws_subnet" and .values.id == "subnet-default-c") | .values' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type | contains("default")) | {address, type, values: .values | {id, vpc_id}}' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | {address, type}' /tmp/state.json | head -100
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_vpc" or .type == "aws_subnets") | {address, values: .values | {id}}' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_subnets") | .values' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address == "module.west1") | .resources[] | {address, type} | select(.type | contains("vpc") or contains("subnets"))' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address == "module.west2") | .resources[] | {address, type} | select(.type | contains("vpc") or contains("subnets"))' /tmp/state.json
cd /workspace/terraform && cat /workspace/terraform/*.tf | grep -E "provider\s+\"aws\"|region\s*=" | head -20
cat > /tmp/analysis.py << 'EOF' import json # Read the state with open('/tmp/state.json', 'r') as f: state = json.load(f) # Helper function to recursively get all resources def get_all_resources(module): resources = module.get('resources', []) for child in module.get('child_modules', []): resources.extend(get_all_resources(child)) return resources all_resources = get_all_resources(state['values']['root_module']) # Build VPC to default mapping vpc_to_module = {} default_vpcs = {} for resource in all_resources: if resource['type'] == 'aws_subnets': # data source for default subnets address = resource['address'] module_name = address.split('.')[0] if '.' in address else 'root' if 'default' in address: vpc_ids = resource['values'].get('filter', [{}])[0].get('values', []) if vpc_ids: default_vpcs[module_name] = vpc_ids[0] # Build subnet to VPC mapping subnet_to_vpc = {} for resource in all_resources: if resource['type'] == 'aws_subnet': subnet_id = resource['values']['id'] vpc_id = resource['values']['vpc_id'] subnet_to_vpc[subnet_id] = vpc_id # Find instances not in default VPC instances = [] for resource in all_resources: if resource['type'] == 'aws_instance': instance_id = resource['values']['id'] subnet_id = resource['values']['subnet_id'] address = resource['address'] # Extract module name parts = address.split('.') module_name = parts[1] if len(parts) > 2 else 'primary' # Check if in default VPC vpc_id = subnet_to_vpc.get(subnet_id) if vpc_id is None and subnet_id.startswith('subnet-default'): vpc_id = default_vpcs.get(module_name) is_default = (module_name in default_vpcs and vpc_id == default_vpcs[module_name]) instances.append({ 'instance_id': instance_id, 'address': address, 'region': module_name, 'subnet': subnet_id, 'vpc': vpc_id, 'is_default': is_default }) # Sort by region instances.sort(key=lambda x: (x['region'], x['instance_id'])) # Print results print("=" * 80) print("EC2 INSTANCES NOT IN DEFAULT VPC (ALL REGIONS)") print("=" * 80) print() non_default = [i for i in instances if not i['is_default']] if non_default: for inst in non_default: print(f"Instance ID: {inst['instance_id']}") print(f" Region: {inst['region']}") print(f" Terraform Address: {inst['address']}") print(f" VPC: {inst['vpc']}") print(f" Subnet: {inst['subnet']}") print() else: print("All instances are in default VPCs.") print() print("=" * 80) print("SUMMARY") print("=" * 80) print(f"Total instances: {len(instances)}") print(f"In default VPC: {len([i for i in instances if i['is_default']])}") print(f"NOT in default VPC: {len(non_default)}") print() if non_default: print("Instance IDs NOT in default VPC:") for inst in non_default: print(f" - {inst['instance_id']} ({inst['region']})") EOF python3 /tmp/analysis.py
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_vpc") | .values' /tmp/state.json
# … 2 more
```

## Pulumi — answered

7 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, inputs: .inputs | {vpc_security_group_ids, subnet_id, associate_public_ip_address}, outputs: .outputs | {id, vpc_id, subnet_id, primary_network_interface_id}, dependencies}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[3], id: .outputs.id, all_outputs: .outputs}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {name: .urn | split("::")[3], id: .outputs.id, cidr_block: .outputs.cidrBlock, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone, default_for_az: .outputs.defaultForAz}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {name: .urn | split("::")[3], id: .outputs.id, cidr_block: .outputs.cidrBlock, is_default: .outputs.isDefault}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | { instance_name: (.urn | split("::")[3]), instance_id: .outputs.id, region: (.arn | split(":")[3]), subnet_id: .outputs.subnetId, private_ip: .outputs.privateIp, dependencies: [.dependencies[]? | split("::")[3]] }' | jq -s ' . as $instances | { instances: $instances, analysis: ($instances | map( select(.instance_name != null) | { instance_name, instance_id, region, is_default_vpc: ( if .instance_name == "defaultVpcServer" then true elif (.subnet_id | startswith("subnet-default")) then true elif (.private_ip | startswith("172.31")) then true # Default VPC CIDR range else false end ) } )) }'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[3], id: .outputs.id, region: .outputs.arn | split(":")[3], subnet_id: .outputs.subnetId, private_ip: .outputs.privateIp}' -c | while read line; do echo "$line" | jq '.name + " | " + .id + " | Region: " + .region + " | Subnet: " + .subnet_id + " | Private IP: " + .private_ip'; done
```

## AWS CDK — answered

10 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, VpcId: .value.Properties.VpcId, SubnetId: .value.Properties.Tags[0]}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.ResourcesVpc' 2>/dev/null | head -20
```

## Alchemy — answered

13 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance | jq '.'
cd /workspace/alchemy && alchemy state list | xargs -I {} alchemy state get {} 2>/dev/null | jq -s 'map(select(.kind == "aws::Instance"))' | jq '.'
cd /workspace/alchemy && find .alchemy -name "*.json" | head -20
cd /workspace/alchemy && for f in .alchemy/alchemy-ec2-multiregion/bench/*.json; do if jq -e '.kind | startswith("aws::")' "$f" > /dev/null 2>&1; then echo "=== $(basename $f) ===" jq '.kind' "$f" fi done | head -50
cd /workspace/alchemy && find .alchemy -name "*Instance*" -o -name "*Server*" -o -name "*instance*" -o -name "*server*" | sort
cd /workspace/alchemy && for f in .alchemy/alchemy-ec2-multiregion/bench/*Server.json .alchemy/alchemy-ec2-multiregion/bench/*-server.json; do if [ -f "$f" ]; then echo "=== $(basename $f) ===" jq '.kind, (.output | {vpcId, subnetId})' "$f" 2>/dev/null fi done
cd /workspace/alchemy && jq '.output | keys' .alchemy/alchemy-ec2-multiregion/bench/webServer.json
cd /workspace/alchemy && for f in .alchemy/alchemy-ec2-multiregion/bench/*Server.json .alchemy/alchemy-ec2-multiregion/bench/*-server.json; do if [ -f "$f" ]; then echo "=== $(basename $f) ===" jq '.output | {InstanceId, region, VpcId, SubnetId}' "$f" 2>/dev/null fi done
cd /workspace/alchemy && for f in .alchemy/alchemy-ec2-multiregion/bench/*.json; do if jq -e '.kind == "aws::Vpc" or .kind == "AWS::EC2::VPC"' "$f" > /dev/null 2>&1; then echo "=== $(basename $f) ===" jq '.output | {id, VpcId, isDefault}' "$f" 2>/dev/null fi done
cd /workspace/alchemy && jq '.output | keys' .alchemy/alchemy-ec2-multiregion/bench/vpc.json
cd /workspace/alchemy && for f in .alchemy/alchemy-ec2-multiregion/bench/*.json; do if jq -e '.kind == "aws::Vpc" or .kind == "AWS::EC2::VPC"' "$f" > /dev/null 2>&1; then echo "=== $(basename $f) ===" jq '.output | {region, vpcId, isDefault}' "$f" 2>/dev/null fi done
# … 1 more
```

## Alchemy v2 (Effect) — answered

5 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state resources --stack main --stage prod us-east-1.run.ts --local
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | head -20
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | xargs grep -l '"resourceType".*Instance' | sort
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | xargs grep -l "subnet-6202ea08"
cat > /logs/agent/agent-output.txt << 'EOF' EC2 Instances Without Default VPC (All Regions) ================================================ Summary: 5 EC2 instances do NOT have a default VPC deployment across all regions. INSTANCES WITHOUT DEFAULT VPC: 1. PrivateServer (us-east-1) - Instance ID: i-bbb510fe354a70a32 - VPC ID: vpc-67a8bb5d (custom VPC) - Subnet ID: subnet-83b34d83 - Private IP: 10.0.1.10 - Instance Type: t3.micro - State: running 2. LaunchTemplateServer (us-east-1) - Instance ID: i-e46792d6b2b8486e4 - VPC ID: vpc-67a8bb5d (custom VPC) - Subnet ID: subnet-6202ea08 - Private IP: 10.0.0.11 - Public IP: 54.144.28.102 - Instance Type: t3.micro (launched from template) - State: running 3. WebServer (us-east-1) - Instance ID: i-6d75471c4910be414 - VPC ID: vpc-67a8bb5d (custom VPC) - Subnet ID: subnet-6202ea08 - Private IP: 10.0.0.10 - Public IP: 54.144.171.90 - Instance Type: t3.micro - State: running 4. WebServer (us-west-1) - Instance ID: i-39804f00db6e59d8d - VPC ID: vpc-1b8e235b (custom VPC) - Subnet ID: subnet-31898648 - Private IP: 10.0.0.10 - Public IP: 54.144.43.207 - Instance Type: t3.micro - State: running 5. WebServer (us-west-2) - Instance ID: i-0010e58b85266301e - VPC ID: vpc-4329a58d (custom VPC) - Subnet ID: subnet-494e35e9 - Private IP: 10.0.0.10 - Public IP: 54.144.201.183 - Instance Type: t3.micro - State: running NOTE: DefaultVpcServer in us-east-1 (i-f1a817952c915d0b4) HAS a default VPC (vpc-default) and is therefore not included in this list. EOF cat /logs/agent/agent-output.txt
```
