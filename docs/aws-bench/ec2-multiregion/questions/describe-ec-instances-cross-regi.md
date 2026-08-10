# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-i3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,VpcId --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-i3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json | jq -r '.Reservations[] | .Instances[] | {InstanceId, InstanceType, State: .State.Name, VpcId, SubnetId}'
aws ec2 describe-instances --region us-west-1 --output json | jq -r '.Reservations[] | .Instances[] | {InstanceId, InstanceType, State: .State.Name, VpcId, SubnetId}'
aws ec2 describe-instances --region us-west-2 --output json | jq -r '.Reservations[] | .Instances[] | {InstanceId, InstanceType, State: .State.Name, VpcId, SubnetId}'
```

## Terraform — answered

13 commands, from `terraform-i3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_ec2_instance' | head -20
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.resources[] | select(.type == "aws_instance") | "\(.address): region=\(.values.availability_zone | .[:-1]), vpc_id=\(.values.vpc_id), subnet_id=\(.values.subnet_id)"' 2>/dev/null
cd /workspace/terraform && ./terraform show -json 2>&1 | head -100
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.resources[0].type == "aws_instance") | {module: .resources[0].address | split(".")[1], instances: [.resources[] | select(.type == "aws_instance") | {name: .name, id: .values.id, region: .values.region, availability_zone: .values.availability_zone, subnet_id: .values.subnet_id, vpc_id: (.values | if has("vpc_id") then .vpc_id else "N/A" end)}]}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_instance") | "\(.values.region): \(.values.id) | VPC: \(.values.vpc_id) | Subnet: \(.values.subnet_id) | AZ: \(.values.availability_zone) | Name: \(.values.tags.Name // "N/A")"'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.resources[0].values.region == "us-east-1") | .resources[] | select(.type | IN("aws_vpc", "aws_subnet")) | {type: .type, id: .values.id, vpc_id: (if .type == "aws_subnet" then .values.vpc_id else .values.id end)}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[0].resources[] | select(.type == "aws_vpc" or .type == "aws_subnet") | {type: .type, id: .values.id, vpc_id: .values.vpc_id}' 2>/dev/null | head -40
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] as $mod | { module: $mod.module_address, subnets: ($mod.resources[] | select(.type == "aws_subnet") | {subnet_id: .values.id, vpc_id: .values.vpc_id}), instances: ($mod.resources[] | select(.type == "aws_instance") | {name: .values.tags.Name, id: .values.id, region: .values.region, subnet_id: .values.subnet_id, availability_zone: .values.availability_zone}) }' | jq -s '.'
cd /workspace/terraform && ./terraform show -json > /tmp/tf_state.json && cat > /tmp/parse_instances.jq << 'EOF' # Extract all subnets and their VPCs def get_subnet_vpc_map: (.values.root_module.child_modules[]?.resources[] + .values.root_module.child_modules[]?.child_modules[]?.resources[]) | select(.type == "aws_subnet") | {subnet_id: .values.id, vpc_id: .values.vpc_id}; # Extract all instances with region info def get_instances: (.values.root_module.child_modules[]?.resources[] + .values.root_module.child_modules[]?.child_modules[]?.resources[]) | select(.type == "aws_instance") | { name: .values.tags.Name // "N/A", instance_id: .values.id, region: .values.region, subnet_id: .values.subnet_id, availability_zone: .values.availability_zone }; # Build maps and correlate [get_subnet_vpc_map] as $subnets | [get_instances] as $instances | { subnets: ($subnets | unique_by(.subnet_id)), instances: $instances, with_vpc: ($instances | map(. + {vpc_id: ($subnets[] | select(.subnet_id == .subnet_id) | .vpc_id)})) } EOF jq -f /tmp/parse_instances.jq /tmp/tf_state.json
cd /workspace/terraform && ./terraform show -json | jq ' # Build subnet->VPC map (.values.root_module.child_modules[]?.resources[] | select(.type == "aws_subnet") | {key: .values.id, value: .values.vpc_id}) as $subnet_map | # Get all instances with region/subnet info [(.values.root_module.child_modules[]?.resources[] | select(.type == "aws_instance") | { name: (if .values.tags.Name then .values.tags.Name else "N/A" end), instance_id: .values.id, region: .values.region, subnet_id: .values.subnet_id, az: .values.availability_zone })] as $instances | # Create subnet map object (reduce (.values.root_module.child_modules[]?.resources[] | select(.type == "aws_subnet")) as $s ({}; .[$s.values.id] = $s.values.vpc_id)) as $subnet_vpc | # Annotate instances with VPC { instances: $instances | map(. + {vpc_id: $subnet_vpc[.subnet_id]}), subnet_vpc_map: $subnet_vpc }'
cd /workspace/terraform && ./terraform show -json | jq ' # Get default VPC info (.values.root_module.child_modules[]?.resources[] | select(.type == "aws_vpc" and .values.default == true)) as $default_vpc | # Get all instances [(.values.root_module.child_modules[]?.resources[] | select(.type == "aws_instance"))] | unique_by(.values.id) | map({ name: (if .values.tags.Name then .values.tags.Name else "N/A" end), instance_id: .values.id, region: .values.region, az: .values.availability_zone, subnet_id: .values.subnet_id, public_ip: (if .values.public_ip != "" and .values.public_ip != null then .values.public_ip else "none" end), private_ip: .values.private_ip }) | sort_by(.region)'
cd /workspace/terraform && ./terraform show -json | jq ' # Build unique subnet->VPC mapping reduce (.values.root_module.child_modules[]?.resources[] | select(.type == "aws_subnet")) as $s ({}; .[$s.values.id] = {vpc_id: $s.values.vpc_id, region: ($s.values.availability_zone | .[:-1])}) as $subnet_map | # Get all unique instances [(.values.root_module.child_modules[]?.resources[] | select(.type == "aws_instance"))] | unique_by(.values.id) | map(. + {vpc_info: $subnet_map[.values.subnet_id]}) | map({ name: (if .values.tags.Name then .values.tags.Name else "N/A" end), instance_id: .values.id, region: .values.region, az: .values.availability_zone, subnet_id: .values.subnet_id, vpc_id: .vpc_info.vpc_id, private_ip: .values.private_ip }) | sort_by([.region, .instance_id])'
# … 1 more
```

## Pulumi — answered

6 commands, from `pulumi-i3`.

```sh
cd /workspace/pulumi && ./pulumi-export 2>&1 | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | .[:-1], vpcId: .outputs.vpcId, instanceId: .outputs.id}' | head -100
cd /workspace/pulumi && ./pulumi-export 2>&1 | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: .outputs | keys}' | head -50
cd /workspace/pulumi && ./pulumi-export 2>&1 | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[3], region: (.outputs.availabilityZone | .[:-1]), instanceId: .outputs.id, subnetId: (.outputs.networkInterfaces[0].subnetId // .inputs.subnetId // "default"), launchTemplate: .inputs.launchTemplate}'
cd /workspace/pulumi && ./pulumi-export 2>&1 | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId}'
cd /workspace/pulumi && ./pulumi-export 2>&1 | jq '.deployment.resources[] | select(.type | contains("vpc") or contains("subnet") or contains("default"))'
cd /workspace/pulumi && ./pulumi-export 2>&1 | jq '.deployment.resources[] | select(.urn | contains("defaultVpcServer")) | {name: .urn | split("::")[3], instanceId: .outputs.id, inputs}'
```

## AWS CDK — answered

13 commands, from `cdk-i1`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | .[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({logicalId: .key, zone: .value.Properties.AvailabilityZone, subnet: (.value.Properties.SubnetId.Ref // .value.Properties.SubnetId), type: .value.Properties.InstanceType})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({logicalId: .key, zone: .value.Properties.AvailabilityZone, subnet: (.value.Properties.SubnetId | if type == "object" then .Ref else . end), instanceType: .value.Properties.InstanceType})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Subnet")) | map({logicalId: .key, vpcRef: .value.Properties.VpcId.Ref})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({logicalId: .key, zone: .value.Properties.AvailabilityZone, subnet: (.value.Properties.SubnetId | if type == "object" then .Ref else . end), instanceType: .value.Properties.InstanceType})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({logicalId: .key, zone: .value.Properties.AvailabilityZone, subnet: (.value.Properties.SubnetId | if type == "object" then .Ref else . end), instanceType: .value.Properties.InstanceType})'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-8efe413fb2db04cc6 i-7d9001a08d554ad03 i-c4deff6351c208ad9 i-2406a03b9ade076f4 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, instanceType: .InstanceType, zone: .Placement.AvailabilityZone, vpcId: .VpcId, subnetId: .SubnetId, securityGroups: .SecurityGroups[].GroupName, tags: ((.Tags[] | select(.Key == "Name") | .Value) // "no-name-tag")}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-fde88288e4fcb0f27 --region us-west-1 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, instanceType: .InstanceType, zone: .Placement.AvailabilityZone, vpcId: .VpcId, subnetId: .SubnetId, securityGroups: .SecurityGroups[].GroupName, tags: ((.Tags[] | select(.Key == "Name") | .Value) // "no-name-tag")}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId}'
# … 1 more
```

## Alchemy — answered

9 commands, from `alchemy-i3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state tree 2>&1 | head -50
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId 2>&1
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance 2>&1
find /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench -name "*.json" -exec grep -l '"kind".*"aws::Instance"' {} \;
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && find . -name "*.json" -exec grep -l '"kind":"aws::Instance"' {} \;
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && cat exp-InstanceId.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for file in exp-InstanceId.json exp-LaunchTemplateInstanceId.json exp-PrivateInstanceId.json exp-DefaultVPCInstanceId.json usw1-exp-InstanceId.json usw2-exp-InstanceId.json; do echo "=== $file ==="; jq '.output | {region, value}' "$file"; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.output.value' exp-VpcId.json exp-DefaultVpcId.json
```

## Alchemy v2 (Effect) — missed

7 commands, from `alchemy-effect-i3`.

```sh
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq '.resources[] | select(.state.resourceType == "aws:ec2:instance") | {stack, stage, fqn, id: .state.attr.id, vpc_id: .state.attr.vpcId, private_ip: .state.attr.privateIpAddress, tags: .state.attr.tags}' | head -200
/workspace/alchemy/alchemy state export /workspace/alchemy/us-west-1.run.ts --local 2>/dev/null | jq '.resources[] | select(.state.resourceType == "aws:ec2:instance") | {stack, stage, fqn, id: .state.attr.id, vpc_id: .state.attr.vpcId, private_ip: .state.attr.privateIpAddress, tags: .state.attr.tags}'
which alchemy && alchemy --version
cd /workspace/alchemy && /workspace/alchemy/node_modules/.bin/alchemy state export us-west-1.run.ts --local 2>&1 | head -50
cd /workspace/alchemy && /workspace/alchemy/node_modules/.bin/alchemy state export us-west-1.run.ts --local 2>&1 | jq '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | {stack: .stack, region: (.stack | split("-") | .[-1]), fqn: .fqn, instance_id: .state.attr.instanceId, instance_type: .state.attr.instanceType, vpc_id: .state.attr.vpcId, subnet_id: .state.attr.subnetId, name: .state.attr.tags.Name}'
cd /workspace/alchemy && /workspace/alchemy/node_modules/.bin/alchemy state export us-west-1.run.ts --local 2>&1 | jq '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | {stack: .stack, fqn: .fqn, instance_id: .state.attr.instanceId, instance_type: .state.attr.instanceType, vpc_id: .state.attr.vpcId, subnet_id: .state.attr.subnetId, availability_zone: .state.attr.availabilityZone, name: .state.attr.tags.Name}' > /tmp/instances.json && cat /tmp/instances.json
cd /workspace/alchemy && /workspace/alchemy/node_modules/.bin/alchemy state export us-west-1.run.ts --local 2>&1 | jq -r ' [.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | { region: (.state.attr.availabilityZone | sub("[a-z]$"; "")), stack: .stack, fqn: .fqn, instance_id: .state.attr.instanceId, instance_type: .state.attr.instanceType, vpc_id: .state.attr.vpcId, subnet_id: .state.attr.subnetId, az: .state.attr.availabilityZone, name: .state.attr.tags.Name }] | group_by(.region) | map({ region: .[0].region, count: length, instances: . })'
```
