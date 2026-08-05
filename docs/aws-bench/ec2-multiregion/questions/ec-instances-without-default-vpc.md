# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

6 commands, from `chant-h3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance ->kind:EC2::VPC !attr:providerDefault=true" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show region,providerDefault --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:logicalName=defaultVpcServer" --at latest --env floci --show VpcId,region
cd /workspace/chant && chant search "kind:EC2::Instance attr:instanceId=i-8db4c1b669671bea4" --at latest --env floci --show VpcId,region
cd /workspace/chant && chant lifecycle show floci | grep -A 1 "AWS::EC2::Instance"
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region
```

## No tool (AWS CLI) — answered

1 commands, from `bare-h3`.

```sh
# Get instances from all regions and identify non-default VPCs regions=("us-east-1" "us-west-1" "us-west-2") for region in "${regions[@]}"; do echo "=== Region: $region ===" # Get default VPC for this region default_vpc=$(aws ec2 describe-vpcs \ --region "$region" \ --filters "Name=isDefault,Values=true" \ --query 'Vpcs[0].VpcId' \ --output text) echo "Default VPC: $default_vpc" # Get all instances and their VPC IDs aws ec2 describe-instances \ --region "$region" \ --query 'Reservations[*].Instances[*].[InstanceId,VpcId,State.Name,InstanceType]' \ --output json | jq -r ".[][] | @csv" | while IFS=',' read -r instance_id vpc_id state instance_type; do # Remove quotes from CSV output instance_id=$(echo $instance_id | tr -d '"') vpc_id=$(echo $vpc_id | tr -d '"') state=$(echo $state | tr -d '"') instance_type=$(echo $instance_type | tr -d '"') # Check if VPC is not default if [ "$vpc_id" != "$default_vpc" ] && [ "$vpc_id" != "null" ]; then echo " Non-default: $instance_id (VPC: $vpc_id, State: $state, Type: $instance_type)" fi done echo "" done
```

## Terraform — answered

11 commands, from `terraform-h3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address: .address, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, availability_zone: .values.availability_zone}' 2>/dev/null
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.default_vpc_server | grep -E "vpc_id|subnet_id|availability_zone|tags"
cd /workspace/terraform && for instance in "module.primary.aws_instance.default_vpc_server" "module.primary.aws_instance.launch_template_server" "module.primary.aws_instance.private_server" "module.primary.aws_instance.web_server" "module.west1.aws_instance.server" "module.west2.aws_instance.server"; do echo "=== $instance ==="; ./terraform state show "$instance" | grep -E "vpc_id|subnet_id"; done
cd /workspace/terraform && ./terraform state list | grep -E "aws_vpc|aws_subnet" | head -20
cd /workspace/terraform && ./terraform state show module.primary.data.aws_vpc.default | grep -E "id|is_default"
cd /workspace/terraform && ./terraform state show module.primary.data.aws_subnets.default | grep -A 50 "ids" | head -20
cd /workspace/terraform && ./terraform state show module.primary.aws_subnet.private | grep "id ="
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | (.child_modules[] | select(.address | contains("primary")) | .resources[] | select(.type == "aws_subnet") | {address: .address, subnet_id: .values.id, vpc_id: .values.vpc_id})' 2>/dev/null
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | (.child_modules[] | select(.address | contains("west")) | .resources[] | select(.type == "aws_subnet") | {address: .address, subnet_id: .values.id, vpc_id: .values.vpc_id})' 2>/dev/null
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | (.child_modules[] | select(.address | startswith("module.")) | select(.address | contains("primary") or contains("west")) | .resources[] | select(.type == "aws_instance") | {instance: .address, subnet_id: .values.subnet_id, availability_zone: .values.availability_zone, region: (.values.availability_zone | split("") | .[:-1] | join(""))})' 2>/dev/null
```

## Pulumi — answered

5 commands, from `pulumi-h3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type | startswith("aws:ec2/instance")) | {urn, outputs: {id: .outputs.id, vpc_id: .outputs.vpc_id, subnet_id: .outputs.subnet_id}, inputs: {vpc_id: .inputs.vpc_id, subnet_id: .inputs.subnet_id}}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type | startswith("aws:ec2/instance")) | {urn, provider: .provider, outputs: .outputs | {id, vpc_id, subnet_id, primary_network_interface_id}, inputs}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn, outputs: {id, isDefault}, inputs: {isDefault}}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn, outputs: {id, vpcId}, inputs: {vpcId}}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet")'
```

## AWS CDK — answered

16 commands, from `cdk-h3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | keys[] as $key | select(.Resources[$key].Type == "AWS::EC2::Instance") | {logical_id: $key, properties: .Resources[$key].Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/us-east-1.json && jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logical_id: .key, properties: .value.Properties}' /tmp/us-east-1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/us-west-1.json && jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logical_id: .key, properties: .value.Properties}' /tmp/us-west-1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/us-west-2.json && jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logical_id: .key, properties: .value.Properties}' /tmp/us-west-2.json
cd /workspace/cdk_app && jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC") | {logical_id: .key, properties: .value.Properties}' /tmp/us-east-1.json
cd /workspace/cdk_app && jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {logical_id: .key, properties: .value.Properties}' /tmp/us-east-1.json
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws ec2 describe-instances --instance-ids i-6189a06b5c98b9e2e i-5be74f530ac36cb44 i-a31ba0f11f3f69b0a i-f15bcebfa2e18553c --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, VpcId: .VpcId, SubnetId: .SubnetId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-38eeb7a7f4e7bcbdd --region us-west-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, VpcId: .VpcId, SubnetId: .SubnetId}'
aws ec2 describe-vpcs --filters Name=is-default,Values=true --region us-west-1 2>/dev/null | jq '.Vpcs[] | {VpcId: .VpcId, IsDefault: .IsDefault}'
# … 4 more
```

## Alchemy — answered

12 commands, from `alchemy-h3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance | jq '.'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-InstanceId | jq '.output'
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *Server.json instance.json; do echo "=== $f ==="; jq '.kind, .id, (.output // .props | select(. != null) | keys)' "$f" 2>/dev/null || true; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *Server.json usw1-server.json usw2-server.json; do echo "=== $f ==="; jq '{id: .id, region: .props.region // .output.region, InstanceId: .output.InstanceId, VpcId: .output.VpcId, SubnetId: .output.SubnetId}' "$f" 2>/dev/null || true; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *Server.json usw1-server.json usw2-server.json; do if [ -f "$f" ]; then echo "File: $f"; jq '{id: .id, region: .output.region, InstanceId: .output.InstanceId, VpcId: .output.VpcId}' "$f" 2>/dev/null; echo; fi; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *vpc.json; do echo "File: $f"; jq '{id: .id, region: .output.region, VpcId: .output.VpcId, IsDefault: .output.IsDefault}' "$f" 2>/dev/null; echo; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *vpc.json; do echo "File: $f"; jq '{id: .id, region: .output.region, vpcId: .output.vpcId, isDefault: .output.isDefault}' "$f" 2>/dev/null; echo; done
cd /workspace/alchemy && alchemy state list | grep -i vpc
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVpcId | jq '.'
cd /workspace/alchemy && find . -name "*.ts" -type f | head -5
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES WITHOUT DEFAULT VPC (ALL REGIONS) ================================================ The following EC2 instances do NOT have a default VPC: 1. us-east-1 Region: - Instance Name: webServer Instance ID: i-1a2520075910557b9 VPC ID: vpc-f48dc6dc VPC Type: Custom VPC (isDefault: false) Subnet: subnet-10.0.0.0/24 (public) - Instance Name: ltServer Instance ID: i-8fc4ddd60bc65ec81 VPC ID: vpc-f48dc6dc VPC Type: Custom VPC (isDefault: false) Subnet: subnet-10.0.0.0/24 (public) Note: Launched via Launch Template - Instance Name: privateServer Instance ID: i-a2033e67b5aa99996 VPC ID: vpc-f48dc6dc VPC Type: Custom VPC (isDefault: false) Subnet: subnet-10.0.1.0/24 (private) 2. us-west-1 Region: - Instance Name: usw1-server Instance ID: i-bfe6923537a487308 VPC ID: vpc-e1ee3364 VPC Type: Custom VPC (isDefault: false) Subnet: subnet-10.0.0.0/24 (public) 3. us-west-2 Region: - Instance Name: usw2-server Instance ID: i-5ba9c6e00e19b0616 VPC ID: vpc-93d7bff5 VPC Type: Custom VPC (isDefault: false) Subnet: subnet-10.0.0.0/24 (public) SUMMARY ======= Total instances without default VPC: 5 Instances WITH default VPC: 1 - Instance Name: defaultVpcServer Instance ID: i-fc4a3dcb05851f4f2 Region: us-east-1 VPC ID: vpc-default (Account's Default VPC) Note: All non-default instances use custom VPCs deployed as part of the Alchemy estate. EOF cat /logs/agent/agent-output.txt
```

## Alchemy v2 (Effect) — answered

11 commands, from `alchemy-effect-h3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && \ alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i instance
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | head -20
find /workspace/alchemy/.alchemy/state -name "*[Ii]nstance*.json" -type f
find /workspace/alchemy/.alchemy/state -type f -name "*.json" -exec grep -l '"resourceType": "aws:ec2/instance:Instance"' {} \;
grep -h "resourceType" /workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/*.json | sort -u
find /workspace/alchemy/.alchemy/state -type f -name "*.json" -exec grep -l '"resourceType": "AWS.EC2.Instance"' {} \;
find /workspace/alchemy/.alchemy/state -type f -name "*.json" -exec grep -l '"resourceType": "AWS.EC2.LaunchTemplateInstance"' {} \;
find /workspace/alchemy/.alchemy/state -type f -name "*.json" -exec grep -l '"resourceType": "AWS.EC2.VPC"' {} \;
```
