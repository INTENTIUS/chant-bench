# Which EC2 instances are in which VPCs across all regions?

`list-ec-instances-by-vpc-across` · the answer aws-bench grades against: **6 instances across 4 VPCs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
```

## Terraform — answered

20 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform show -json 2>&1 | head -100
cd /workspace/terraform && ./terraform show -json 2>&1 | jq '.values.root_module | .. | select(type=="object" and .type=="aws_instance") | {address, values: {id, instance_id, vpc_id, subnet_id, availability_zone, provider_name}}' | head -200
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.default_vpc_server'
cd /workspace/terraform && for instance in $(./terraform state list | grep aws_instance); do echo "=== $instance ===" ./terraform state show "$instance" | grep -E "region|subnet_id|vpc_id|availability_zone|id = " | head -10 done
cd /workspace/terraform && ./terraform state list | grep aws_subnet
cd /workspace/terraform && for subnet in $(./terraform state list | grep 'aws_subnet'); do echo "=== $subnet ===" ./terraform state show "$subnet" | grep -E "id = |vpc_id|cidr_block|availability_zone" | head -5 done
cd /workspace/terraform && ./terraform state show 'module.primary.aws_subnet.private' | grep -E "id = |vpc_id"
cd /workspace/terraform && ./terraform state show 'module.primary.aws_subnet.private' | head -20
cd /workspace/terraform && cat > /tmp/map_instances.sh << 'EOF' #!/bin/bash # Get all instances and their details echo "Mapping EC2 instances to VPCs..." echo "" # First, let's build a subnet->vpc mapping declare -A subnet_to_vpc # Primary region subnets subnet_to_vpc["subnet-babfd57d"]="vpc-4e1c19fc" # private in us-east-1 subnet_to_vpc["subnet-cd9b267a"]="vpc-4e1c19fc" # public in us-east-1 # Now get default VPC subnets from state ./terraform state show 'module.primary.data.aws_subnets.default' 2>/dev/null | grep "id =" | while read line; do subnet_id=$(echo "$line" | grep -oP 'subnet-[a-z0-9]+' | head -1) if [ ! -z "$subnet_id" ]; then echo "Found default subnet: $subnet_id" fi done # Get subnets for west regions ./terraform state show 'module.west1.aws_subnet.public' | grep "id =" | head -1 ./terraform state show 'module.west2.aws_subnet.public' | grep "id =" | head -1 EOF chmod +x /tmp/map_instances.sh /tmp/map_instances.sh
cd /workspace/terraform && ./terraform state list | grep aws_vpc
cd /workspace/terraform && for vpc in $(./terraform state list | grep 'aws_vpc'); do echo "=== $vpc ===" ./terraform state show "$vpc" | grep -E "^ id = |^ cidr_block = " | head -2 done
# … 8 more
```

## Pulumi — answered

20 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi_state.json && echo "State exported successfully"
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: {id: .outputs.id, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone, private_ip: .outputs.privateIp}, inputs: {vpc_id: .inputs.vpcId, subnet_id: .inputs.subnetId}}' | head -100
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn, subnet_id: .outputs.id, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone, inputs_id: .inputs.id}'
cat > /tmp/build_instance_vpc_map.jq << 'EOF' # Build a map of subnet_id -> vpc_id .deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {key: .outputs.id, value: .outputs.vpcId} EOF cd /workspace/pulumi && \ cat /tmp/pulumi_state.json | jq -f /tmp/build_instance_vpc_map.jq | jq -s 'map({(.key): .value}) | add' > /tmp/subnet_vpc_map.json cat /tmp/subnet_vpc_map.json
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn, vpc_id: .outputs.id, cidr_block: .outputs.cidrBlock}'
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | .outputs.id'
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type | contains("DefaultVpc") or contains("default")) | {type, urn, outputs}'
cat > /tmp/final_mapping.jq << 'EOF' # Extract instances with their details and join with VPC info .deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | { instance_name: (.urn | split("::") | .[-1]), instance_id: .outputs.id, availability_zone: .outputs.availabilityZone, private_ip: .outputs.privateIp, subnet_id: .inputs.subnetId, launch_template_id: .inputs.launchTemplate.id // null } EOF cd /workspace/pulumi && \ cat /tmp/pulumi_state.json | jq -f /tmp/final_mapping.jq > /tmp/instances.json cat /tmp/instances.json
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {instance_name: (.urn | split("::") | .[-1]), instance_id: .outputs.id, availability_zone: .outputs.availabilityZone, private_ip: .outputs.privateIp, subnet_id: .inputs.subnetId, launch_template_id: (.inputs.launchTemplate.id | select(. != null))}' > /tmp/instances.json cat /tmp/instances.json
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {instance_name: (.urn | split("::") | .[-1]), instance_id: .outputs.id, availability_zone: .outputs.availabilityZone, private_ip: .outputs.privateIp, subnet_id: .inputs.subnetId}' -c
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn, vpc_id: .outputs.id, is_default: .outputs.isDefault}' -c
cd /workspace/pulumi && cat /tmp/pulumi_state.json | jq '.deployment.resources[] | select(.type == "aws:ssm/parameter:Parameter") | select(.urn | contains("DefaultVpcId")) | {urn, value: .inputs.value}' -c
# … 8 more
```

## AWS CDK — answered

14 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance")) | to_entries[] | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet")) | to_entries[] | {LogicalId: .key, Type: .value.Type, Properties: .value.Properties}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.ResourcesVpcPublicSubnet1Subnet7103FD34, .Resources.ResourcesVpcPrivateSubnet1Subnet98586872'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance")) | to_entries[] | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet")) | to_entries[] | {LogicalId: .key, Type: .value.Type}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance")) | map({LogicalId: .key, SubnetRef: .value.Properties.SubnetId})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, SubnetId: .value.Properties.SubnetId}'
# … 2 more
```
