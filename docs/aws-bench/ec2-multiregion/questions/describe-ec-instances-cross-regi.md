# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,VpcId --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-m3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json
aws ec2 describe-instances --region us-west-1 --output json
aws ec2 describe-instances --region us-west-2 --output json
```

## Terraform — answered

5 commands, from `terraform-m1`.

```sh
cd /workspace/terraform && ./terraform state list
cd /workspace/terraform && ./terraform show -json | jq '.' > /tmp/terraform_state.json && wc -l /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address | startswith("module.primary") or startswith("module.west1") or startswith("module.west2")) | .resources[] | select(.type == "aws_instance")' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address | startswith("module.primary") or startswith("module.west1") or startswith("module.west2")) | .resources[] | select(.type == "aws_vpc" or .type == "aws_subnet") | {address: .address, type: .type, vpc_id: .values.id, cidr_block: .values.cidr_block}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address | startswith("module.primary") or startswith("module.west1") or startswith("module.west2")) | .resources[] | select(.type == "aws_subnet" or .type == "aws_vpc") | {address: .address, type: .type, id: .values.id, vpc_id: .values.vpc_id, availability_zone: .values.availability_zone}' /tmp/terraform_state.json
```

## Pulumi — answered

8 commands, from `pulumi-m1`.

```sh
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | head -200
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: (.inputs.availabilityZone | sub("[a-z]$"; "")), vpc: .inputs.vpcId, instance_id: .outputs.id, availability_zone: .inputs.availabilityZone}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, vpc: .inputs.vpcId, instance_id: .outputs.id, private_ip: .outputs.privateIp, availability_zone: .outputs.availabilityZone}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, instance_id: .outputs.id, subnet_id: .outputs.subnetId, primary_network_interface_id: .outputs.primaryNetworkInterfaceId}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" or (.type == "aws:ec2/default" and "VpcSubnet" | IN(.[].type))) | {type, id: .outputs.id, vpc_id: .outputs.vpcId}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("vpc") or contains("Vpc")) | {type, id: .outputs.id}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], availability_zone: .outputs.availabilityZone, inputs: {subnet_id: .inputs.subnetId, vpc_id: .inputs.vpcId}, outputs: {subnet_id: .outputs.subnetId}}'
```

## AWS CDK — answered

11 commands, from `cdk-m3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}' | head -200
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, vpcId: .value.Properties.VpcId, subnetId: (.value | select(.Type=="AWS::EC2::Subnet") | .Properties.CidrBlock)}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, subnet: .value.Properties.SubnetId}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, subnet: .value.Properties.SubnetId}' | head -100
for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" for stack in $(aws cloudformation list-stacks --region "$region" --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query 'StackSummaries[*].StackName' --output text | grep ec2-multiregion-EC2); do echo "Stack: $stack" aws cloudformation describe-stack-resources --stack-name "$stack" --region "$region" --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output text done done
for instance_id in i-6a62f03f1b63e02cb i-d49fa51ee7943b064 i-99a5057f76dd16760 i-3e459933b4e4a49c1; do echo "Instance: $instance_id" aws ec2 describe-instances --region us-east-1 --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].[Tags[?Key==`Name`].Value[0],VpcId,SubnetId,PrivateIpAddress]' --output text done
aws ec2 describe-instances --region us-east-1 --filters "Name=vpc-id,Values=vpc-50375e93" --query 'Reservations[0].Instances[*].[Tags[?Key==`Name`].Value[0],InstanceId,SubnetId]' --output text
aws ec2 describe-instances --region us-east-1 --instance-ids i-6a62f03f1b63e02cb i-99a5057f76dd16760 i-3e459933b4e4a49c1 --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Name`].Value[0],VpcId]' --output table
aws ec2 describe-instances --region us-east-1 --instance-ids i-6a62f03f1b63e02cb i-99a5057f76dd16760 i-3e459933b4e4a49c1 --query 'Reservations[*].Instances[*].[InstanceId,VpcId]' --output text
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances Across Regions ## Instance Count by Region **us-east-1:** 4 instances **us-west-1:** 1 instance **us-west-2:** 1 instance **Total:** 6 instances across all three regions --- ## Detailed Breakdown ### us-east-1 (4 instances) 1. **WebServerInstance** (i-6a62f03f1b63e02cb) - VPC: vpc-50375e93 - Subnet: subnet-d0c287b5 (10.0.0.0/24) - Instance Type: t3.micro 2. **MyEC2Instance** (i-d49fa51ee7943b064) - VPC: vpc-default (EC2-Classic) - Subnet: subnet-default-a - Instance Type: t3.micro 3. **PrivateInstance** (i-99a5057f76dd16760) - VPC: vpc-50375e93 - Subnet: subnet-788d6413 (10.0.1.0/24) - Instance Type: t3.micro 4. **LaunchTemplateInstance** (i-3e459933b4e4a49c1) - VPC: vpc-50375e93 - Subnet: subnet-d0c287b5 (10.0.0.0/24) - Instance Type: t3.micro ### us-west-1 (1 instance) 1. **WebServerInstance** (i-006e65b4905bccbb5) - Instance Type: t3.micro ### us-west-2 (1 instance) 1. **WebServerInstance** (i-1018901c5ceef586e) - Instance Type: t3.micro --- ## VPC Connectivity in us-east-1 **Instances sharing network connectivity (same VPC: vpc-50375e93):** 1. WebServerInstance (i-6a62f03f1b63e02cb) - Public subnet (10.0.0.0/24) 2. PrivateInstance (i-99a5057f76dd16760) - Private subnet (10.0.1.0/24) 3. LaunchTemplateInstance (i-3e459933b4e4a49c1) - Public subnet (10.0.0.0/24) **Isolated instance (different VPC):** - MyEC2Instance (i-d49fa51ee7943b064) - vpc-default (EC2-Classic VPC) **Summary:** In us-east-1, 3 instances share network connectivity through VPC vpc-50375e93, while 1 instance (MyEC2Instance) is in a separate VPC and is not directly connected to the others at the VPC level. EOF cat /logs/agent/agent-output.txt
```

## Alchemy — answered

3 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId
cd /workspace/alchemy && alchemy state list | grep "aws::Instance"
```

## Alchemy v2 (Effect) — answered

5 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local 2>&1 | head -50
find /workspace/alchemy/.alchemy/state/ -type f -name "*.json" | head -20
find /workspace/alchemy/.alchemy/state/ -type f -name "*.json" | sort
```
