# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-p3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show providerDefault,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region | grep -v "vpc-default"
```

## No tool (AWS CLI) — answered

3 commands, from `bare-g3`.

```sh
# Get the default VPC ID for each region for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text) echo "Default VPC: $default_vpc" done
# Query instances in all regions and check which are not in default VPC declare -a regions=("us-east-1" "us-west-1" "us-west-2") declare -a non_default_instances for region in "${regions[@]}"; do echo "Querying region: $region" # Get default VPC for this region default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) if [ "$default_vpc" != "None" ] && [ -n "$default_vpc" ]; then echo " Default VPC ID: $default_vpc" # Get all instances and their VPC IDs aws ec2 describe-instances --region "$region" --query 'Reservations[*].Instances[*].[InstanceId,VpcId,State.Name,InstanceType,Tags[?Key==`Name`].Value|[0]]' --output json | jq -r '.[][] | @csv' | while IFS=',' read -r instance_id vpc_id state instance_type name; do # Remove quotes from values instance_id=$(echo $instance_id | tr -d '"') vpc_id=$(echo $vpc_id | tr -d '"') state=$(echo $state | tr -d '"') instance_type=$(echo $instance_type | tr -d '"') name=$(echo $name | tr -d '"') # Check if instance is not in default VPC if [ "$vpc_id" != "$default_vpc" ] && [ -n "$instance_id" ] && [ "$state" = "running" ]; then echo " Found non-default: $instance_id (VPC: $vpc_id, Type: $instance_type, Name: $name)" fi done else echo " No default VPC found or error querying VPC" fi done
# Generate comprehensive report of instances not in default VPC { echo "EC2 Instances Not in Default VPC (All Regions)" echo "==============================================" echo "" declare -a regions=("us-east-1" "us-west-1" "us-west-2") for region in "${regions[@]}"; do echo "Region: $region" echo "---" # Get default VPC for this region default_vpc=$(aws ec2 describe-vpcs --region "$region" --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text 2>/dev/null) if [ "$default_vpc" != "None" ] && [ -n "$default_vpc" ]; then # Get all instances with full details aws ec2 describe-instances --region "$region" --query 'Reservations[*].Instances[*].[InstanceId,VpcId,State.Name,InstanceType,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' --output json | jq -r '.[][] | select(.[1] != null) | @json' | while read -r line; do instance_data=$(echo "$line" | jq -r '.') instance_id=$(echo "$instance_data" | jq -r '.[0]') vpc_id=$(echo "$instance_data" | jq -r '.[1]') state=$(echo "$instance_data" | jq -r '.[2]') instance_type=$(echo "$instance_data" | jq -r '.[3]') private_ip=$(echo "$instance_data" | jq -r '.[4]') name=$(echo "$instance_data" | jq -r '.[5]') # Check if instance is not in default VPC if [ "$vpc_id" != "$default_vpc" ] && [ -n "$instance_id" ]; then name_display="${name:-<no name>}" echo " • Instance: $instance_id" echo " Name: $name_display" echo " VPC: $vpc_id" echo " Type: $instance_type" echo " State: $state" echo " Private IP: $private_ip" echo "" fi done # Check if there were any non-default instances non_default_count=$(aws ec2 describe-instances --region "$region" --query "Reservations[*].Instances[?VpcId!='$default_vpc']" --output json | jq '[.[] | .[] | .[]] | length') if [ "$non_default_count" -eq 0 ]; then echo " (No instances outside default VPC)" echo "" fi else echo " Unable to determine default VPC" echo "" fi done } | tee /logs/agent/agent-output.txt
```

## Terraform — answered

15 commands, from `terraform-g3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module' > /tmp/state.json && head -100 /tmp/state.json
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address, region: .values.availability_zone[:-1], vpc_id: .values.vpc_id}' | head -100
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance")' 2>&1 | head -50
cd /workspace/terraform && ./terraform state list | grep -i instance
cd /workspace/terraform && for instance in "module.primary.aws_instance.default_vpc_server" "module.primary.aws_instance.launch_template_server" "module.primary.aws_instance.private_server" "module.primary.aws_instance.web_server" "module.west1.aws_instance.server" "module.west2.aws_instance.server"; do echo "=== $instance ===" ./terraform state show "$instance" | grep -E "vpc_id|availability_zone|subnet_id" done
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type == "aws_instance") | {name: .address, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, az: .values.availability_zone}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type == "aws_subnet") | {name: .address, subnet_id: .values.id, vpc_id: .values.vpc_id}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.values.id == "subnet-default-c" or (.values.subnet_id == "subnet-default-c")) | {type, address, id: .values.id, subnet_id: .values.subnet_id}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type | contains("default_vpc") or contains("default_subnet") or contains("default_network")) | {type, address, values}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type == "aws_vpc") | {name: .address, vpc_id: .values.id, is_default: .values.enable_dns_hostnames, cidr: .values.cidr_block}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]?) | .resources[] | select(.type | startswith("data.")) | select(.type | contains("subnet") or contains("vpc")) | {type, address, id: .values.id, vpc_id: .values.vpc_id}'
cd /workspace/terraform && ./terraform state list | grep -i "data.*default"
# … 3 more
```

## Pulumi — answered

8 commands, from `pulumi-g3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, vpc_id: .outputs.vpcId, subnet_id: .outputs.subnetId, private_ip: .outputs.privateIp}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn: .urn, subnet_id: .outputs.id, vpc_id: .outputs.vpcId}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn: .urn, vpc_id: .outputs.id, is_default: .outputs.isDefault}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], vpc_id: .outputs.vpcId, subnet_id: .outputs.subnetId, availability_zone: .outputs.availabilityZone, tags: .inputs.tags}' | jq -s 'sort_by(.name)'
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | ($resources[] | select(.type == "aws:ec2/vpc:Vpc") | {vpc_id: .outputs.id, urn: .urn}) as $vpcs | ($resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, vpc_id: .outputs.vpcId, urn: .urn}) as $subnets | ($resources[] | select(.type == "aws:ec2/instance:Instance") | { instance_name: .urn | split("::")[-1], instance_id: .outputs.id, subnet_id: .outputs.subnetId, az: .outputs.availabilityZone, vpc_id: ($subnets | select(.subnet_id == (.outputs.subnetId // empty)) | .vpc_id) }) as $instances | {instance_name: $instances.instance_name, instance_id: $instances.instance_id, vpc_id: $instances.vpc_id, availability_zone: $instances.az} | @tsv ' | column -t
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | ($resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, vpc_id: .outputs.vpcId}) as $subnets | [($resources[] | select(.type == "aws:ec2/instance:Instance") | { instance_name: .urn | split("::")[-1], instance_id: .outputs.id, subnet_id: .outputs.subnetId, az: .outputs.availabilityZone, vpc_id: ($subnets | select(.subnet_id == (.outputs.subnetId // empty)) | .vpc_id), uses_default_vpc: (.outputs.subnetId | startswith("subnet-default")) })] | sort_by(.instance_name) | .[] '
cd /workspace/pulumi && ./pulumi-export | jq -r ' [.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], subnet_id: .outputs.subnetId, az: .outputs.availabilityZone}] | sort_by(.name) | .[] | "Instance: \(.name) | Subnet: \(.subnet_id) | AZ: \(.az)" '
cd /workspace/pulumi && ./pulumi-export | jq -r ' .deployment.resources as $res | [ ($res[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, vpc_id: .outputs.vpcId}), {subnet_id: "subnet-default-c", vpc_id: "DEFAULT_VPC"} ] as $subnets | $res[] | select(.type == "aws:ec2/instance:Instance") | { instance: (.urn | split("::")[-1]), subnet: .outputs.subnetId, is_default: (.outputs.subnetId == "subnet-default-c") } | "\(.instance): \(.subnet) [default: \(.is_default)]" ' | sort
```

## AWS CDK — answered

16 commands, from `cdk-g3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC") | {logicalId: .key, type: .value.Type, vpcId: .value.Properties.VpcId, cidrBlock: .value.Properties.CidrBlock}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-ef113468614f9c1cf i-3c02eb69c1d65498e i-a59c133af01998f1e i-d4c0cb47c81eccb7b --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, instanceName: (.Tags[] | select(.Key == "Name") | .Value), vpcId: .VpcId, subnetId: .SubnetId}'
aws ec2 describe-instances --instance-ids i-1a632b2ae087b41f8 --region us-west-1 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, instanceName: (.Tags[] | select(.Key == "Name") | .Value), vpcId: .VpcId, subnetId: .SubnetId}'
aws ec2 describe-instances --instance-ids i-850e75c53cf9fc303 --region us-west-2 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, instanceName: (.Tags[] | select(.Key == "Name") | .Value), vpcId: .VpcId, subnetId: .SubnetId}'
aws ec2 describe-vpcs --vpc-ids vpc-default vpc-ddde268d vpc-45813635 vpc-7a3fc06b --region us-east-1 2>/dev/null | jq '.Vpcs[] | {vpcId: .VpcId, isDefault: .IsDefault}' && aws ec2 describe-vpcs --vpc-ids vpc-45813635 --region us-west-1 2>/dev/null | jq '.Vpcs[] | {vpcId: .VpcId, isDefault: .IsDefault}' && aws ec2 describe-vpcs --vpc-ids vpc-7a3fc06b --region us-west-2 2>/dev/null | jq '.Vpcs[] | {vpcId: .VpcId, isDefault: .IsDefault}'
# … 4 more
```

## Alchemy — answered

8 commands, from `alchemy-g3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId
find /workspace/alchemy/.alchemy -name "*.json" -type f | grep -E "us-east|us-west|eu-" | head -20
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId alchemy-ec2-multiregion/bench/exp-InstanceId alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId alchemy-ec2-multiregion/bench/exp-PrivateInstanceId alchemy-ec2-multiregion/bench/usw1-exp-InstanceId alchemy-ec2-multiregion/bench/usw2-exp-InstanceId 2>/dev/null | jq -r '.output.value // .output.InstanceId // empty' | sort
cd /workspace/alchemy && jq -r '.output.value' .alchemy/alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId.json .alchemy/alchemy-ec2-multiregion/bench/exp-InstanceId.json .alchemy/alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId.json .alchemy/alchemy-ec2-multiregion/bench/exp-PrivateInstanceId.json .alchemy/alchemy-ec2-multiregion/bench/usw1-exp-InstanceId.json .alchemy/alchemy-ec2-multiregion/bench/usw2-exp-InstanceId.json
cd /workspace/alchemy && cat > /tmp/check_vpcs.sh << 'EOF' #!/bin/bash # Instance IDs DEFAULT_VPC_INST="i-155260bca0b163118" # us-east-1 WEB_SERVER="i-a1944e0e5ef2c17dc" # us-east-1 LT_SERVER="i-7e126b9cbcdbaeb27" # us-east-1 PRIVATE_SERVER="i-a314499db74434f68" # us-east-1 USW1_SERVER="i-acd0046cf3fcd8f71" # us-west-1 USW2_SERVER="i-e25d97558a31631d1" # us-west-2 # Function to check VPC check_instance_vpc() { local instance_id=$1 local region=$2 echo "Checking $instance_id in $region..." aws ec2 describe-instances \ --instance-ids "$instance_id" \ --region "$region" \ --query 'Reservations[0].Instances[0].[InstanceId, VpcId, SubnetId]' \ --output text 2>/dev/null || echo "ERROR" } # Check us-east-1 instances echo "=== US-EAST-1 ===" check_instance_vpc "$DEFAULT_VPC_INST" "us-east-1" check_instance_vpc "$WEB_SERVER" "us-east-1" check_instance_vpc "$LT_SERVER" "us-east-1" check_instance_vpc "$PRIVATE_SERVER" "us-east-1" # Check us-west-1 echo "" echo "=== US-WEST-1 ===" check_instance_vpc "$USW1_SERVER" "us-west-1" # Check us-west-2 echo "" echo "=== US-WEST-2 ===" check_instance_vpc "$USW2_SERVER" "us-west-2" EOF chmod +x /tmp/check_vpcs.sh /tmp/check_vpcs.sh
cat > /logs/agent/agent-output.txt << 'EOF' EC2 Instances WITHOUT a Default VPC (All Regions) ================================================== Region: us-east-1 - i-a1944e0e5ef2c17dc (WebServerInstance) - VPC: vpc-b005d949 - i-7e126b9cbcdbaeb27 (LaunchTemplateInstance) - VPC: vpc-b005d949 - i-a314499db74434f68 (PrivateInstance) - VPC: vpc-b005d949 Region: us-west-1 - i-acd0046cf3fcd8f71 (WebServerInstance) - VPC: vpc-8c27b795 Region: us-west-2 - i-e25d97558a31631d1 (WebServerInstance) - VPC: vpc-58e467e1 Summary: 5 instances without a default VPC - 3 in us-east-1 - 1 in us-west-1 - 1 in us-west-2 Note: 1 instance (i-155260bca0b163118) in us-east-1 IS using the default VPC (vpc-default) EOF cat /logs/agent/agent-output.txt
```

## Alchemy v2 (Effect) — answered

15 commands, from `alchemy-effect-g2`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage default us-west-1.run.ts --local | grep -i instance; done
cd /workspace/alchemy && alchemy state resources --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage default us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack "alchemy-effect-ec2-multiregion-us-east-1" us-west-1.run.ts --local
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local | grep -iE "(Server|Instance)" | grep -v "^Exp"; done
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn LaunchTemplateServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn WebLaunchTemplate us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn PrivateServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn WebServer us-west-1.run.ts --local
# … 3 more
```
