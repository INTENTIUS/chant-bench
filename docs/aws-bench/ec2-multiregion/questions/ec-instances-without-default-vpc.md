# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-i3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance !->kind:EC2::VPC attr:providerDefault=true" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show InstanceId,VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show VpcId,providerDefault,region --explain
```

## No tool (AWS CLI) — answered

6 commands, from `bare-i3`.

```sh
# Get default VPC ID for each region echo "=== Default VPCs by Region ===" for region in us-east-1 us-west-1 us-west-2; do default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) echo "$region: $default_vpc" done
# Get all instances not in default VPC for each region echo "=== Instances NOT in Default VPC ===" for region in us-east-1 us-west-1 us-west-2; do echo "" echo "Region: $region" # Get default VPC for this region default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) if [ -z "$default_vpc" ] || [ "$default_vpc" = "None" ]; then echo " No default VPC found in this region" continue fi echo " Default VPC ID: $default_vpc" # Get instances not in default VPC instances=$(aws ec2 describe-instances --region "$region" --query "Reservations[].Instances[?VpcId!='$default_vpc'].[InstanceId,VpcId,State.Name,InstanceType,Tags[?Key=='Name'].Value|[0]]" --output json 2>/dev/null) # Check if we got any instances count=$(echo "$instances" | jq 'length') if [ "$count" -eq 0 ]; then echo " No instances outside default VPC" else echo "$instances" | jq -r '.[] | "\(.InstanceId) | VPC: \(.VpcId) | State: \(.State.Name) | Type: \(.InstanceType) | Name: \(.Tags // "N/A")"' fi done
# Get all instances not in default VPC for each region - fixed query echo "=== Instances NOT in Default VPC ===" for region in us-east-1 us-west-1 us-west-2; do echo "" echo "Region: $region" # Get default VPC for this region default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) if [ -z "$default_vpc" ] || [ "$default_vpc" = "None" ]; then echo " No default VPC found in this region" continue fi echo " Default VPC ID: $default_vpc" # Get instances not in default VPC aws ec2 describe-instances --region "$region" \ --query "Reservations[].Instances[?VpcId!='$default_vpc'].{InstanceId:InstanceId,VpcId:VpcId,State:State.Name,InstanceType:InstanceType,Name:Tags[?Key=='Name']|[0].Value}" \ --output json 2>/dev/null | jq -r '.[] | select(.InstanceId != null) | "\(.InstanceId) | VPC: \(.VpcId) | State: \(.State) | Type: \(.InstanceType) | Name: \(.Name // "N/A")"' done
# Debug: check the actual JSON structure region="us-east-1" default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) echo "Default VPC: $default_vpc" echo "" echo "Raw instance data:" aws ec2 describe-instances --region "$region" --output json 2>/dev/null | jq '.Reservations[0].Instances[0] | {InstanceId, VpcId, State: .State.Name}' | head -20
# Get all instances not in default VPC for each region echo "=== Instances NOT in Default VPC ===" for region in us-east-1 us-west-1 us-west-2; do echo "" echo "Region: $region" echo "---" # Get default VPC for this region default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) if [ -z "$default_vpc" ] || [ "$default_vpc" = "None" ]; then echo "No default VPC found in this region" continue fi echo "Default VPC: $default_vpc" echo "" # Get all instances and filter for those not in default VPC aws ec2 describe-instances --region "$region" --output json 2>/dev/null | jq -r --arg default_vpc "$default_vpc" ' .Reservations[].Instances[] | select(.VpcId != $default_vpc) | [.InstanceId, .VpcId, .State.Name, .InstanceType, (.Tags[] | select(.Key=="Name") | .Value // "N/A")] | @tsv' | awk -F'\t' '{print $1 " | VPC: " $2 " | State: " $3 " | Type: " $4 " | Name: " $5}' # Count instances count=$(aws ec2 describe-instances --region "$region" --output json 2>/dev/null | jq --arg default_vpc "$default_vpc" '[.Reservations[].Instances[] | select(.VpcId != $default_vpc)] | length') if [ "$count" -eq 0 ]; then echo "(No instances outside default VPC)" fi done
# Create comprehensive output and write to file cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES NOT IN DEFAULT VPC ================================= Summary: - Total instances outside default VPC: 5 - us-east-1: 3 instances - us-west-1: 1 instance - us-west-2: 1 instance Details by Region: ================== REGION: us-east-1 Default VPC: vpc-default Instances outside default VPC: 1. i-5c8da84c9f36669a2 (LaunchTemplateInstance) - VPC: vpc-9db1ce60 - State: running - Type: t3.micro 2. i-428719f07db4ec1d6 (WebServerInstance) - VPC: vpc-9db1ce60 - State: running - Type: t3.micro 3. i-b8310d81b99b27c48 (PrivateInstance) - VPC: vpc-9db1ce60 - State: running - Type: t3.micro REGION: us-west-1 Default VPC: vpc-default Instances outside default VPC: 1. i-794ef32b4de64a6f7 (WebServerInstance) - VPC: vpc-f8f29d71 - State: running - Type: t3.micro REGION: us-west-2 Default VPC: vpc-default Instances outside default VPC: 1. i-ca26e23ef677e8e1a (WebServerInstance) - VPC: vpc-081a956d - State: running - Type: t3.micro Key Observations: ================= - All 5 instances outside default VPCs are in a running state - All instances are t3.micro type - In us-east-1, all 3 instances are in the same custom VPC (vpc-9db1ce60) - Each region has a distinct custom VPC for its non-default instances EOF cat /logs/agent/agent-output.txt
```

## Terraform — answered

21 commands, from `terraform-i3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.resources[] | select(.type == "aws_instance") | .address' | head -20
cd /workspace/terraform && ./terraform show -json > /tmp/terraform_state.json && echo "State exported successfully"
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address: .address, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id}' 2>/dev/null
cd /workspace/terraform && ./terraform state list 2>&1 | head -20
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_vpc.default' 2>&1
cd /workspace/terraform && for instance in 'module.primary.aws_instance.default_vpc_server' 'module.primary.aws_instance.launch_template_server' 'module.primary.aws_instance.private_server' 'module.primary.aws_instance.web_server'; do echo "=== $instance ===" ./terraform state show "$instance" 2>&1 | grep -E 'id|vpc_id|subnet_id|ami|availability_zone|region' done
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_subnets.default' 2>&1
cd /workspace/terraform && ./terraform state list 2>&1 | grep -E 'aws_instance|module' | head -50
cd /workspace/terraform && ./terraform state list 2>&1 | grep 'module.west1' | grep 'aws_instance\|data.aws_vpc\|data.aws_subnets'
cd /workspace/terraform && ./terraform state list 2>&1 | grep -o 'module\.[^.]*' | sort -u
cd /workspace/terraform && ./terraform state list 2>&1 | grep 'aws_instance'
cd /workspace/terraform && ./terraform state show 'module.west1.aws_instance.server' 2>&1 | grep -E 'id|vpc_id|subnet_id|ami|availability_zone|region'
# … 9 more
```

## Pulumi — answered

5 commands, from `pulumi-i3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, vpc_id: .outputs.vpc_id, subnet_id: .outputs.subnet_id, private_ip: .outputs.private_ip}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, inputs: .inputs | {vpc_id, subnet_id}}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, outputs: .outputs}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn: .urn, isDefault: .outputs.isDefault, cidrBlock: .outputs.cidrBlock}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | "\(.outputs.tags.Name // "unnamed")\t\(.outputs.id)\t\(.outputs.privateIp)\t\(.outputs.availabilityZone)"' | sort
```

## AWS CDK — answered

15 commands, from `cdk-i1`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq -r '.Resources | keys[] as $key | select(.Resources[$key].Type == "AWS::EC2::Instance") | $key' 2>/dev/null || echo "No EC2 instances in this stack"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/stack1.json && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | .key' /tmp/stack1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/stack2.json && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | .key' /tmp/stack2.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/stack3.json && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | .key' /tmp/stack3.json
cd /workspace/cdk_app && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key): SubnetId=\(.value.Properties.SubnetId // "NOT SET") | NetworkInterfaces=\(.value.Properties.NetworkInterfaces // "NOT SET")"' /tmp/stack1.json
cd /workspace/cdk_app && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key): SubnetId=\(.value.Properties.SubnetId // "NOT SET") | NetworkInterfaces=\(.value.Properties.NetworkInterfaces // "NOT SET")"' /tmp/stack2.json
cd /workspace/cdk_app && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key): SubnetId=\(.value.Properties.SubnetId // "NOT SET") | NetworkInterfaces=\(.value.Properties.NetworkInterfaces // "NOT SET")"' /tmp/stack3.json
cd /workspace/cdk_app && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC") | "\(.key): \(.value.Properties | {CidrBlock, Tags})"' /tmp/stack1.json
cd /workspace/cdk_app && jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | "\(.key): VpcId=\(.value.Properties.VpcId) | SubnetId will ref to this"' /tmp/stack1.json | head -20
cat > /tmp/analyze_vpcs.sh << 'EOF' #!/bin/bash echo "=== US-EAST-1 Stack ===" echo "EC2 Instances:" jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\n--- \(.key) ---\nSubnetId: \(.value.Properties.SubnetId | tostring)\nVPC details:"' /tmp/stack1.json echo "" echo "VPC/Subnet Mappings:" jq -r '.Resources | to_entries[] | select(.value.Type | . == "AWS::EC2::VPC" or . == "AWS::EC2::Subnet") | "\(.key): Type=\(.value.Type) | VpcId/SubnetId=\(.value.Properties.VpcId // .value.Properties.SubnetId // "N/A")"' /tmp/stack1.json echo "" echo "=== US-WEST-1 Stack ===" jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key): SubnetId=\(.value.Properties.SubnetId | tostring)"' /tmp/stack2.json echo "" echo "=== US-WEST-2 Stack ===" jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key): SubnetId=\(.value.Properties.SubnetId | tostring)"' /tmp/stack3.json EOF chmod +x /tmp/analyze_vpcs.sh /tmp/analyze_vpcs.sh
aws cloudformation describe-stack-resources \ --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 \ --region us-east-1 \ --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' \ --output table 2>/dev/null
# … 3 more
```

## Alchemy — answered

14 commands, from `alchemy-i3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId
cd /workspace/alchemy && alchemy state list | grep -E "aws::Instance|aws::EC2"
cd /workspace/alchemy && alchemy state list | head -20
cd /workspace/alchemy && alchemy state list | tail -30
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/defaultVpcServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/web
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-server
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw2-server
cd /workspace/alchemy && alchemy state list | xargs -I {} sh -c 'alchemy state get {} | grep -q '"'"'AWS::EC2::Instance'"'"' && echo {}'
# … 2 more
```

## Alchemy v2 (Effect) — missed

7 commands, from `alchemy-effect-i3`.

```sh
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources | map(select(.resourceType == "aws:ec2/instance:Instance")) | map({fqn: .fqn, stack: .stack, vpcId: .state.attr.vpcId, subnetId: .state.attr.subnetId})'
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources | map(.resourceType) | unique' | grep -i ec2
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources | map(.resourceType) | unique'
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources[0]' | head -50
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources | map(select(.state.resourceType == "AWS.EC2.Instance")) | map({fqn: .fqn, stack: .stack, vpcId: .state.attr.vpcId})'
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources | map(select(.state.resourceType == "AWS.EC2.Instance")) | map(select(.state.attr.vpcId != "vpc-default")) | map({fqn: .fqn, stack: .stack, region: .stack | split("-") | .[-1], vpcId: .state.attr.vpcId, instanceId: .state.attr.instanceId})'
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources | map(select(.state.resourceType == "AWS.EC2.Instance")) | map(select(.state.attr.vpcId != "vpc-default")) | sort_by(.stack) | map({name: .fqn, region: (.stack | match("(us-[a-z]+-[0-9])") | .captures[0].string), vpcId: .state.attr.vpcId, instanceId: .state.attr.instanceId})'
```
