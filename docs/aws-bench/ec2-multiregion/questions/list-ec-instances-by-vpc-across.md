# Which EC2 instances are in which VPCs across all regions?

`list-ec-instances-by-vpc-across` · the answer aws-bench grades against: **6 instances across 4 VPCs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,PrivateIpAddress,PublicIpAddress,region --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-m3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json
aws ec2 describe-instances --region us-west-1 --output json
aws ec2 describe-instances --region us-west-2 --output json
```

## Terraform — answered

10 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_ec2_instance|aws_vpc' | head -30
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && echo "State exported to JSON"
cd /workspace/terraform && jq -r '.values.root_module | .. | select(type == "object" and .type == "aws_instance") | "\(.address): vpc_id=\(.values.vpc_id), subnet_id=\(.values.subnet_id), private_ip=\(.values.private_ip)"' /tmp/state.json
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.web_server
cd /workspace/terraform && jq -r ' .values.root_module | ( [.. | select(type == "object" and .type == "aws_subnet") | {address: .address, values: .values}] as $subnets | [.. | select(type == "object" and .type == "aws_vpc") | {address: .address, values: .values}] as $vpcs | [.. | select(type == "object" and .type == "aws_instance") | {address: .address, values: .values}] as $instances | $instances[] | .values.subnet_id as $subnet_id | ($subnets[] | select(.values.id == $subnet_id)) as $subnet | ($vpcs[] | select(.values.id == $subnet.values.vpc_id)) as $vpc | "\(.address) | Region: \($instances[] | select(.values | has("region")) | select(.values.id == .values.id) .values.region // "unknown") | VPC: \($vpc.address) (id: \($vpc.values.id)) | Subnet: \($subnet.address) (id: \($subnet_id))" ) ' /tmp/state.json 2>/dev/null | sort
cd /workspace/terraform && ./terraform state list | grep 'aws_instance\.' | while read instance; do echo "=== $instance ===" ./terraform state show "$instance" | grep -E '^\s+(id|region|subnet_id|arn)\s*=' | head -10 done
cd /workspace/terraform && ./terraform state list | grep 'aws_subnet\.' | while read subnet; do echo "=== $subnet ===" ./terraform state show "$subnet" | grep -E '^\s+(id|vpc_id)\s*=' done
cd /workspace/terraform && ./terraform state list | grep 'aws_vpc\.' | while read vpc; do echo "=== $vpc ===" ./terraform state show "$vpc" | grep -E '^\s+(id|cidr_block)' | head -2 done
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_vpc.default' | grep -E '^\s+id\s*=' | head -1
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES BY REGION AND VPC ================================ REGION: us-east-1 ================= VPC: vpc-default (Default VPC, 172.31.0.0/16) - Instance: default_vpc_server ID: i-300b21df4a83914d9 Subnet: subnet-default-c Private IP: 172.31.32.10 VPC: vpc-2bab67cb (Custom VPC, 10.0.0.0/16) - Instance: web_server ID: i-0ba6a42ade430f176 Subnet: subnet-7a6b81fa (public) Private IP: 10.0.0.10 Public IP: 54.144.13.131 - Instance: launch_template_server ID: i-b41235d7d93348f6e Subnet: subnet-7a6b81fa (public) Private IP: 10.0.0.11 - Instance: private_server ID: i-58d75f672379b0574 Subnet: subnet-4fb8565b (private) Private IP: 10.0.1.10 REGION: us-west-1 ================= VPC: vpc-6d5e4dff (Custom VPC, 10.0.0.0/16) - Instance: server ID: i-6b85edfbf78860085 Subnet: subnet-84ebef7c (public) Private IP: 10.0.0.10 REGION: us-west-2 ================= VPC: vpc-7f5be42b (Custom VPC, 10.0.0.0/16) - Instance: server ID: i-0a3101c51d65b7d3c Subnet: subnet-7f98cb00 (public) Private IP: 10.0.0.10 SUMMARY ======= Total Instances: 6 - us-east-1: 4 instances (2 VPCs: 1 default + 1 custom) - us-west-1: 1 instance (1 custom VPC) - us-west-2: 1 instance (1 custom VPC) VPC Summary: - vpc-default (AWS default VPC in us-east-1): 1 instance - vpc-2bab67cb (module.primary, us-east-1): 3 instances - vpc-6d5e4dff (module.west1, us-west-1): 1 instance - vpc-7f5be42b (module.west2, us-west-2): 1 instance EOF cat /logs/agent/agent-output.txt
```

## Pulumi — answered

13 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | rtrimstr((.outputs.availabilityZone[-1:])), vpc: .outputs.vpcId, subnetId: .outputs.subnetId, instanceId: .outputs.id, tags: .outputs.tags}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: {vpcId, id, availabilityZone, tags}}' | head -100
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' | jq . | head -200
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], instanceId: .outputs.id, region: .outputs.arn | match("arn:aws:ec2:([^:]+):").captures[0].string, availabilityZone: .outputs.availabilityZone, subnetId: .outputs.subnetId, tags: .outputs.tags}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, subnetArn: .outputs.arn, vpcId: .outputs.vpcId}' | grep -E '(subnetId|vpcId)'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {vpcId: .outputs.id, arn: .outputs.arn, tags: .outputs.tags}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" or .type == "aws:ec2/defaultSubnet:DefaultSubnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId, arn: .outputs.arn}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("default")) | {type, id: .outputs.id, vpcId: .outputs.vpcId, arn: .outputs.arn}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ssm/parameter:Parameter" and .inputs.name | contains("DefaultVpcId")) | {name: .inputs.name, value: .outputs.value}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ssm/parameter:Parameter" and (.inputs.name | type == "string" and contains("DefaultVpcId"))) | {name: .inputs.name, value: .outputs.value}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("Vpc") or contains("Subnet")) | {type, id: .outputs.id, vpcId: .outputs.vpcId}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("get") or contains("data")) | {type, id: .outputs.id, urn}'
# … 1 more
```

## AWS CDK — answered

13 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC") | {LogicalId, PhysicalId, ResourceType, StackRegion: .StackId | split(":")[3]}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC") | {LogicalId, PhysicalId, ResourceType, StackRegion: .StackId | split(":")[3]}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC") | {LogicalId, PhysicalId, ResourceType, StackRegion: .StackId | split(":")[3]}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC") | {LogicalId, PhysicalId, ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC") | {LogicalId, PhysicalId, ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC") | {LogicalId, PhysicalId, ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance")'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::VPC")'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance")'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::VPC")'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance")'
# … 1 more
```

## Alchemy — answered

9 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -E "aws::Instance|aws::Vpc" | head -30
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && for name in webServer defaultVpcServer ltServer privateServer usw1-server usw2-server; do echo "=== $name ==="; alchemy state get alchemy-ec2-multiregion/bench/$name | jq '.output | {id, region, vpcId, subnetId}' 2>/dev/null || echo "Not found"; done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer | jq '.output' 2>/dev/null
cd /workspace/alchemy && for name in webServer defaultVpcServer ltServer privateServer usw1-server usw2-server; do echo "=== $name ==="; alchemy state get alchemy-ec2-multiregion/bench/$name 2>/dev/null | jq '.output | {region, InstanceId, VpcId}'; done
cd /workspace/alchemy && for vpc in vpc usw1-vpc usw2-vpc; do echo "=== $vpc ==="; alchemy state get alchemy-ec2-multiregion/bench/$vpc 2>/dev/null | jq '.output | {VpcId, region, CidrBlock}'; done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/vpc | jq '.output'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-vpc | jq '.output' && echo "---" && alchemy state get alchemy-ec2-multiregion/bench/usw2-vpc | jq '.output'
```

## Alchemy v2 (Effect) — answered

10 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state tree us-east-1.run.ts --local | head -50
cd /workspace/alchemy && alchemy state tree us-west-1.run.ts --local | head -50
cd /workspace/alchemy && alchemy state tree us-west-2.run.ts --local | head -50
find /workspace/alchemy/.alchemy/state -name "*.json" | head -20
for region_dir in /workspace/alchemy/.alchemy/state/*/bench/; do echo "=== $(basename $(dirname $region_dir)) ===" && ls $region_dir | grep -E '(Server|Instance|Vpc)' | sort; done
jq -r '.resourceType' /workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/{WebServer,DefaultVpcServer,LaunchTemplateServer,PrivateServer,Vpc}.json
cat > /tmp/parse_instances.sh << 'EOF' #!/bin/bash regions=( "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2" ) for region_stack in "${regions[@]}"; do region=$(echo "$region_stack" | grep -o "us-[a-z]*-[0-9]") echo "=== $region ===" # Find VPC resources and get their IDs vpc_file="/workspace/alchemy/.alchemy/state/$region_stack/bench/Vpc.json" if [ -f "$vpc_file" ]; then vpc_id=$(jq -r '.attr.physicalResourceId // .attr.id' "$vpc_file") echo "VPC: $vpc_id" fi # Find all instance resources find "/workspace/alchemy/.alchemy/state/$region_stack/bench/" -name "*.json" | while read file; do resource_type=$(jq -r '.resourceType // "N/A"' "$file" 2>/dev/null) case "$resource_type" in AWS.EC2.Instance|AWS.EC2.LaunchTemplateInstance) resource_name=$(basename "$file" .json) instance_id=$(jq -r '.attr.physicalResourceId // .attr.instanceId // "N/A"' "$file") subnet_id=$(jq -r '.attr.subnetId // .attr.SubnetId // "N/A"' "$file") vpc_id=$(jq -r '.attr.vpcId // .attr.VpcId // "N/A"' "$file") echo " Instance: $resource_name" echo " ID: $instance_id" echo " Subnet: $subnet_id" echo " VPC: $vpc_id" ;; esac done echo "" done EOF chmod +x /tmp/parse_instances.sh /tmp/parse_instances.sh
cat > /tmp/detailed_parse.sh << 'EOF' #!/bin/bash regions=( "alchemy-effect-ec2-multiregion-us-east-1:us-east-1" "alchemy-effect-ec2-multiregion-us-west-1:us-west-1" "alchemy-effect-ec2-multiregion-us-west-2:us-west-2" ) for region_info in "${regions[@]}"; do IFS=':' read -r region_stack region <<< "$region_info" echo "=== $region ===" # Get main VPC ID vpc_file="/workspace/alchemy/.alchemy/state/$region_stack/bench/Vpc.json" if [ -f "$vpc_file" ]; then main_vpc_id=$(jq -r '.attr.id // .attr.physicalResourceId // "N/A"' "$vpc_file") fi # Find all instance resources and show mapping instances_found=0 find "/workspace/alchemy/.alchemy/state/$region_stack/bench/" -name "*Server.json" -o -name "*Instance*.json" | sort | while read file; do resource_type=$(jq -r '.resourceType // "N/A"' "$file" 2>/dev/null) case "$resource_type" in AWS.EC2.Instance|AWS.EC2.LaunchTemplateInstance) resource_name=$(basename "$file" .json) instance_id=$(jq -r '.attr.id // .attr.physicalResourceId // "N/A"' "$file") subnet_id=$(jq -r '.attr.subnetId // .attr.SubnetId // "N/A"' "$file") vpc_id=$(jq -r '.attr.vpcId // .attr.VpcId // "N/A"' "$file") # If VPC is not directly available, it might be in references if [ "$vpc_id" = "N/A" ] || [ "$vpc_id" = "null" ]; then vpc_id=$(jq -r '.attr.vpc // "N/A"' "$file") fi echo " $instance_id in $vpc_id (subnet: $subnet_id)" instances_found=$((instances_found + 1)) ;; esac done if [ $instances_found -eq 0 ]; then echo " No instances found" fi echo "" done EOF chmod +x /tmp/detailed_parse.sh /tmp/detailed_parse.sh
cat > /tmp/final_parse.sh << 'EOF' #!/bin/bash regions=( "alchemy-effect-ec2-multiregion-us-east-1:us-east-1" "alchemy-effect-ec2-multiregion-us-west-1:us-west-1" "alchemy-effect-ec2-multiregion-us-west-2:us-west-2" ) for region_info in "${regions[@]}"; do IFS=':' read -r region_stack region <<< "$region_info" echo "=== $region ===" # Find all instance resources and show mapping instances_found=0 declare -A vpc_map # First pass: collect all instances with their VPCs find "/workspace/alchemy/.alchemy/state/$region_stack/bench/" -name "*.json" | sort | while read file; do resource_type=$(jq -r '.resourceType // "N/A"' "$file" 2>/dev/null) case "$resource_type" in AWS.EC2.Instance|AWS.EC2.LaunchTemplateInstance) resource_name=$(basename "$file" .json) instance_id=$(jq -r '.attr.instanceId // "N/A"' "$file") vpc_id=$(jq -r '.attr.vpcId // "N/A"' "$file") subnet_id=$(jq -r '.attr.subnetId // "N/A"' "$file") state=$(jq -r '.attr.state // "N/A"' "$file") if [ "$instance_id" != "N/A" ] && [ "$instance_id" != "null" ]; then echo " $instance_id -> VPC: $vpc_id" echo " Subnet: $subnet_id, State: $state" fi ;; esac done echo "" done EOF chmod +x /tmp/final_parse.sh /tmp/final_parse.sh
cat > /tmp/complete_parse.sh << 'EOF' #!/bin/bash regions=( "alchemy-effect-ec2-multiregion-us-east-1:us-east-1" "alchemy-effect-ec2-multiregion-us-west-1:us-west-1" "alchemy-effect-ec2-multiregion-us-west-2:us-west-2" ) # Build subnet->VPC mappings declare -A subnet_to_vpc for region_info in "${regions[@]}"; do IFS=':' read -r region_stack region <<< "$region_info" find "/workspace/alchemy/.alchemy/state/$region_stack/bench/" -name "*.json" | while read file; do resource_type=$(jq -r '.resourceType // "N/A"' "$file" 2>/dev/null) if [[ "$resource_type" == "AWS.EC2.Instance" || "$resource_type" == "AWS.EC2.LaunchTemplateInstance" ]]; then subnet=$(jq -r '.attr.subnetId // "N/A"' "$file") vpc=$(jq -r '.attr.vpcId // "N/A"' "$file") if [ "$vpc" != "N/A" ] && [ "$vpc" != "null" ]; then echo "$subnet $vpc" fi fi done | sort -u > /tmp/subnet_vpc_map_$region.txt done # Now print results for region_info in "${regions[@]}"; do IFS=':' read -r region_stack region <<< "$region_info" echo "=== $region ===" find "/workspace/alchemy/.alchemy/state/$region_stack/bench/" -name "*.json" | sort | while read file; do resource_type=$(jq -r '.resourceType // "N/A"' "$file" 2>/dev/null) case "$resource_type" in AWS.EC2.Instance|AWS.EC2.LaunchTemplateInstance) resource_name=$(basename "$file" .json) instance_id=$(jq -r '.attr.instanceId // "N/A"' "$file") vpc_id=$(jq -r '.attr.vpcId // "N/A"' "$file") subnet_id=$(jq -r '.attr.subnetId // "N/A"' "$file") # If VPC is not available, try to infer from subnet if [ "$vpc_id" = "N/A" ] || [ "$vpc_id" = "null" ]; then inferred_vpc=$(grep "^$subnet_id " /tmp/subnet_vpc_map_$region.txt 2>/dev/null | awk '{print $2}') if [ -n "$inferred_vpc" ]; then vpc_id="$inferred_vpc (inferred from subnet)" fi fi if [ "$instance_id" != "N/A" ] && [ "$instance_id" != "null" ]; then echo " $instance_id -> VPC: $vpc_id" fi ;; esac done echo "" done EOF chmod +x /tmp/complete_parse.sh /tmp/complete_parse.sh
```
