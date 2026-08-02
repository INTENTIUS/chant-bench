# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

5 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance ->kind:EC2::VPC !attr:providerDefault=true" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show providerDefault,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance ->kind:EC2::VPC attr:providerDefault=true" --at latest --env floci --show VpcId,region
cd /workspace/chant && chant search "kind:EC2::Instance ->kind:EC2::VPC" --at latest --env floci --show VpcId,region
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

8 commands, from `terraform-m1`.

```sh
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | .. | objects | select(.type == "aws_instance") | {address, values}' 2>/dev/null | head -100
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | recurse(.child_modules[]?) | .resources[]? | select(.type == "aws_instance") | {address: .address, vpc_id: .values.vpc_id, region: .values.region, instance_id: .values.id}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | recurse(.child_modules[]?) | .resources[]? | select(.type == "aws_instance") | {address: .address, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, region: .values.region, instance_id: .values.id}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | recurse(.child_modules[]?) | .resources[]? | select(.type == "aws_subnet") | {subnet_id: .values.id, vpc_id: .values.vpc_id, region: .values.region}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | recurse(.child_modules[]?) | .resources[]? | select(.type == "aws_vpc") | {vpc_id: .values.id, is_default: .values.is_default, region: .values.region}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | recurse(.child_modules[]?) | .resources[]? | select(.type == "aws_instance") | {address: .address, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, region: .values.region, instance_id: .values.id}' | jq -s 'group_by(.vpc_id) | .[]' 2>/dev/null
cd /workspace/terraform && find modules -type f -name "*.tf" | head -20
cat > /tmp/analysis.json << 'EOF' { "instances_without_default_vpc": [ { "terraform_address": "module.primary.aws_instance.web_server", "instance_id": "i-ef9c24a234de9b352", "region": "us-east-1", "subnet_id": "subnet-74f30a2b", "vpc_id": "vpc-a45be95e", "vpc_type": "custom" }, { "terraform_address": "module.primary.aws_instance.launch_template_server", "instance_id": "i-7ed39183343ec7319", "region": "us-east-1", "subnet_id": "subnet-74f30a2b", "vpc_id": "vpc-a45be95e", "vpc_type": "custom" }, { "terraform_address": "module.primary.aws_instance.private_server", "instance_id": "i-d65111136e4920bca", "region": "us-east-1", "subnet_id": "subnet-d6845f2f", "vpc_id": "vpc-a45be95e", "vpc_type": "custom" }, { "terraform_address": "module.west1.aws_instance.server", "instance_id": "i-1946ed4c443149f19", "region": "us-west-1", "subnet_id": "subnet-f82a16d3", "vpc_id": "vpc-8bf18bc2", "vpc_type": "custom" }, { "terraform_address": "module.west2.aws_instance.server", "instance_id": "i-9eed568209b248421", "region": "us-west-2", "subnet_id": "subnet-1fb6074c", "vpc_id": "vpc-fd8cc1c7", "vpc_type": "custom" } ], "instances_with_default_vpc": [ { "terraform_address": "module.primary.aws_instance.default_vpc_server", "instance_id": "i-702137d810a7d56fd", "region": "us-east-1", "subnet_id": "subnet-default-c", "vpc_type": "default" } ], "summary": { "total_instances": 6, "instances_without_default_vpc": 5, "instances_with_default_vpc": 1, "regions_analyzed": ["us-east-1", "us-west-1", "us-west-2"] } } EOF cat /tmp/analysis.json
```

## Pulumi — answered

9 commands, from `pulumi-m1`.

```sh
cd /workspace/pulumi && ./pulumi-export
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, id: .outputs.id, vpcId: .outputs.vpcId, subnetId: .outputs.subnetId, inputs_vpcSecurityGroupIds: .inputs.vpcSecurityGroupIds}' $(cd /workspace/pulumi && ./pulumi-export | tee /tmp/state.json > /dev/null && echo /tmp/state.json)
cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn, id: .outputs.id, vpcId: .outputs.vpcId}' | head -50
cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn, id: .outputs.id, isDefault: .outputs.isDefault, cidrBlock: .outputs.cidrBlock}'
cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet")'
cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], id: .outputs.id, subnetId: .outputs.subnetId, region: (.arn | split(":")[3] // "unknown"), inputs: {vpcSecurityGroupIds: .inputs.vpcSecurityGroupIds, subnetId: .inputs.subnetId}}'
cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[-1]), id: .outputs.id, subnetId: .outputs.subnetId, inputs_subnetId: .inputs.subnetId}'
cat /tmp/state.json | jq -r ' # Create a map of subnet to VPC ((.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {((.outputs.id // .id)): .outputs.vpcId}) | add) as $subnet_to_vpc | # Get all VPCs and determine which is default ((.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | select(.outputs.isDefault == true or .outputs.isDefault == "true") | .outputs.id) | values) as $default_vpc_id | # Get all instances .deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | { name: (.urn | split("::")[-1]), instance_id: .outputs.id, subnet_id: .outputs.subnetId, vpc_id: ($subnet_to_vpc[.outputs.subnetId]), is_in_managed_vpc: ($subnet_to_vpc[.outputs.subnetId] != null) } ' 2>/dev/null
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances WITHOUT Default VPC (All Regions) Based on analysis of the Pulumi state, the following EC2 instances do NOT have a default VPC: ## Instances in Custom VPCs (Non-Default): 1. **privateServer** (i-77ea5a355fd3b0c38) - Region: us-east-1 - Subnet: subnet-52a8630e - VPC: vpc-209676c6 (custom VPC) 2. **ltServer** (i-dd98868a196b5b609) - Region: us-east-1 - Subnet: subnet-48b173fc - VPC: vpc-209676c6 (custom VPC) 3. **webServer** (i-31f8aa5ea3b5e7375) - Region: us-east-1 - Subnet: subnet-48b173fc - VPC: vpc-209676c6 (custom VPC) 4. **usw1-server** (i-0e60377b9d285b3e3) - Region: us-west-1 - Subnet: subnet-64ea3205 - VPC: vpc-d7675f73 (custom VPC) 5. **usw2-server** (i-8a60e750df29eb589) - Region: us-west-2 - Subnet: subnet-d4b68c0e - VPC: vpc-f177c74b (custom VPC) ## Summary: - Total EC2 instances in Pulumi state: 6 - Instances WITHOUT default VPC: 5 - Instance WITH default VPC: 1 (defaultVpcServer using subnet-default-c) All instances without a default VPC are deployed in custom VPCs managed by Pulumi. EOF cat /logs/agent/agent-output.txt
```

## AWS CDK — answered

9 commands, from `cdk-m3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}' > /tmp/instances_us-east-1.json && cat /tmp/instances_us-east-1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}' > /tmp/instances_us-west-1.json && cat /tmp/instances_us-west-1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}' > /tmp/instances_us-west-2.json && cat /tmp/instances_us-west-2.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC") | {LogicalId: .key, Type: .value.Type, Properties: .value.Properties}'
find /workspace/cdk_app -type f -name "*.ts" | head -20
for stack in "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2"; do region=$(echo "$stack" | sed 's/.*-//g') echo "=== Stack: $stack (Region: $region) ===" aws cloudformation describe-stack-resources --stack-name "$stack" --region "$region" 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}' done
# Test the regions regions=() for stack in "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2"; do if [[ $stack =~ (us-east-1|us-west-1|us-west-2)$ ]]; then region="${BASH_REMATCH[1]}" echo "Stack: $stack -> Region: $region" aws cloudformation describe-stack-resources --stack-name "$stack" --region "$region" 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}' fi done
# Get the VPC IDs for each instance echo "=== US-EAST-1 ===" aws ec2 describe-instances --instance-ids i-6a62f03f1b63e02cb i-d49fa51ee7943b064 i-99a5057f76dd16760 i-3e459933b4e4a49c1 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, VpcId: .VpcId, SubnetId: .SubnetId}' echo "" echo "=== US-WEST-1 ===" aws ec2 describe-instances --instance-ids i-006e65b4905bccbb5 --region us-west-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, VpcId: .VpcId, SubnetId: .SubnetId}' echo "" echo "=== US-WEST-2 ===" aws ec2 describe-instances --instance-ids i-1018901c5ceef586e --region us-west-2 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, VpcId: .VpcId, SubnetId: .SubnetId}'
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

11 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state resources --stack us-east-1 --stage bench us-west-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && for fqn in WebServer LaunchTemplateServer PrivateServer; do echo "=== $fqn ===" alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn "$fqn" us-west-1.run.ts --local 2>&1 | jq '.attr | {instanceId, vpcId}' done
cd /workspace/alchemy && for stack in alchemy-effect-ec2-multiregion-us-east-1 alchemy-effect-ec2-multiregion-us-west-1 alchemy-effect-ec2-multiregion-us-west-2; do echo "=== Stack: $stack ===" for fqn in DefaultVpcServer WebServer LaunchTemplateServer PrivateServer; do echo -n "$fqn: " alchemy state get --stack "$stack" --stage bench --fqn "$fqn" us-west-1.run.ts --local 2>&1 | jq -r '.attr | "\(.instanceId) - VPC: \(.vpcId // "null")"' done echo "" done
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local 2>&1 | head -50
cd /workspace/alchemy && for stack in alchemy-effect-ec2-multiregion-us-east-1 alchemy-effect-ec2-multiregion-us-west-1 alchemy-effect-ec2-multiregion-us-west-2; do echo "=== Stack: $stack ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>&1 | grep -i "server\|instance" | grep -v "^Exp" done
cd /workspace/alchemy && { echo "US-EAST-1:" for fqn in DefaultVpcServer WebServer LaunchTemplateServer PrivateServer; do alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn "$fqn" us-west-1.run.ts --local 2>&1 | jq -r '.attr | " \(.instanceId) (\(.tags.Name // "no-name")): VPC=\(.vpcId // "null")"' done echo "" echo "US-WEST-1:" alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1 | jq -r '.attr | " \(.instanceId) (\(.tags.Name // "no-name")): VPC=\(.vpcId // "null")"' echo "" echo "US-WEST-2:" alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1 | jq -r '.attr | " \(.instanceId) (\(.tags.Name // "no-name")): VPC=\(.vpcId // "null")"' }
cd /workspace/alchemy && { echo "Instances WITHOUT default VPC (vpcId != vpc-default or vpc-default):" echo "" echo "US-EAST-1:" for fqn in DefaultVpcServer WebServer LaunchTemplateServer PrivateServer; do data=$(alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn "$fqn" us-west-1.run.ts --local 2>&1) instance_id=$(echo "$data" | jq -r '.attr.instanceId') vpc_id=$(echo "$data" | jq -r '.attr.vpcId') name=$(echo "$data" | jq -r '.attr.tags.Name // .fqn') if [ "$vpc_id" != "vpc-default" ]; then echo " Resource: $fqn" echo " Instance ID: $instance_id" echo " VPC ID: $vpc_id" echo " Name: $name" echo "" fi done echo "US-WEST-1:" data=$(alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1) instance_id=$(echo "$data" | jq -r '.attr.instanceId') vpc_id=$(echo "$data" | jq -r '.attr.vpcId') name=$(echo "$data" | jq -r '.attr.tags.Name // .fqn') if [ "$vpc_id" != "vpc-default" ]; then echo " Resource: WebServer" echo " Instance ID: $instance_id" echo " VPC ID: $vpc_id" echo " Name: $name" echo "" fi echo "US-WEST-2:" data=$(alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1) instance_id=$(echo "$data" | jq -r '.attr.instanceId') vpc_id=$(echo "$data" | jq -r '.attr.vpcId') name=$(echo "$data" | jq -r '.attr.tags.Name // .fqn') if [ "$vpc_id" != "vpc-default" ]; then echo " Resource: WebServer" echo " Instance ID: $instance_id" echo " VPC ID: $vpc_id" echo " Name: $name" echo "" fi }
```
