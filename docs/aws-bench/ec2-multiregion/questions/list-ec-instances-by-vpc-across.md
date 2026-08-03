# Which EC2 instances are in which VPCs across all regions?

`list-ec-instances-by-vpc-across` · the answer aws-bench grades against: **6 instances across 4 VPCs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-r5`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-g3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json
aws ec2 describe-instances --region us-west-1 --output json
aws ec2 describe-instances --region us-west-2 --output json
```

## Terraform — answered

5 commands, from `terraform-g3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_vpc|aws_subnet'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | .. | select(type=="object" and .type=="aws_instance") | "\(.address) | \(.values.availability_zone) | \(.values.subnet_id) | \(.values.vpc_security_group_ids)"' 2>/dev/null | head -20
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | recurse(.child_modules[]? // empty) | select(.resources) | .resources[] | select(.type=="aws_vpc" or .type=="aws_subnet") | {type, address, name: .values.tags.Name, vpc_id: .values.vpc_id, id: .values.id}' 2>/dev/null
cd /workspace/terraform && ./terraform state show module.primary.data.aws_vpc.default 2>/dev/null | head -20
cd /workspace/terraform && ./terraform state show module.primary.data.aws_subnets.default 2>/dev/null | grep -A 20 "ids"
```

## Pulumi — answered

7 commands, from `pulumi-g3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, instance_id: .outputs.id, private_ip: .outputs.privateIp, vpc_id: .outputs.vpcId, subnet_id: .outputs.subnetId, availability_zone: .outputs.availabilityZone}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn: .urn, subnet_id: .outputs.id, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone}' | sort
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {vpc_id: .outputs.id, cidr_block: .outputs.cidrBlock, urn: .urn}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[3]), instance_id: .outputs.id, subnet_id: .outputs.subnetId, availability_zone: .outputs.availabilityZone}' /tmp/pulumi-state.json
cat > /tmp/ec2_mapping.sh << 'EOF' #!/bin/bash # Parse Pulumi state to get EC2 instances in VPCs by region cd /workspace/pulumi # Build subnet-to-VPC mapping declare -A subnet_to_vpc declare -A subnet_to_az jq -r '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | "\(.outputs.id)|\(.outputs.vpcId)|\(.outputs.availabilityZone)"' /tmp/pulumi-state.json | while IFS='|' read subnet vpc az; do subnet_to_vpc[$subnet]=$vpc subnet_to_az[$subnet]=$az done # Build VPC name mapping from URNs declare -A vpc_names jq -r '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | "\(.outputs.id)|\(.urn | split("::")[3])"' /tmp/pulumi-state.json | while IFS='|' read vpc name; do vpc_names[$vpc]=$name done # Get instances and join with VPC info jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | "\(.urn | split("::")[3])|\(.outputs.id)|\(.outputs.subnetId)|\(.outputs.availabilityZone)"' /tmp/pulumi-state.json | while IFS='|' read instance_name instance_id subnet_id az; do # Extract region from AZ region=${az%?} # Get subnet info from the data we collected vpc_id=$(jq -r --arg subnet "$subnet_id" '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" and .outputs.id == $subnet) | .outputs.vpcId' /tmp/pulumi-state.json) vpc_name=$(jq -r --arg vpc "$vpc_id" '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc" and .outputs.id == $vpc) | .urn | split("::")[3]' /tmp/pulumi-state.json) # For default VPC, use the AZ to identify if [ -z "$vpc_id" ] || [ "$vpc_id" = "null" ]; then vpc_id="default-vpc" vpc_name="default-vpc" fi echo "$region|$instance_name|$instance_id|$subnet_id|$vpc_id|$vpc_name" done EOF chmod +x /tmp/ec2_mapping.sh /tmp/ec2_mapping.sh
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES BY VPC AND REGION ================================ Queried regions: us-east-1, us-west-1, us-west-2 Data source: Pulumi state export US-EAST-1 --------- VPC: vpc (vpc-12cacf39) - privateServer (i-57ff73956476908e9) | Subnet: subnet-ea868200 | AZ: us-east-1a - ltServer (i-c924ed6eff2d4feee) | Subnet: subnet-7f52035a | AZ: us-east-1a - webServer (i-cb9e8a0626c2576a8) | Subnet: subnet-7f52035a | AZ: us-east-1a VPC: default-vpc (default-vpc) - defaultVpcServer (i-30288bd1719667c62) | Subnet: subnet-default-c | AZ: us-east-1c US-WEST-1 --------- VPC: usw1-vpc (vpc-af640e85) - usw1-server (i-cc46ab7d4f7df270c) | Subnet: subnet-70720ae1 | AZ: us-west-1a US-WEST-2 --------- VPC: usw2-vpc (vpc-561c9c6f) - usw2-server (i-55039add58d6cec67) | Subnet: subnet-977f6a97 | AZ: us-west-2a SUMMARY ------- Total EC2 Instances: 6 By Region: us-east-1: 4 instances (3 in vpc-12cacf39, 1 in default-vpc) us-west-1: 1 instance (in vpc-af640e85) us-west-2: 1 instance (in vpc-561c9c6f) By VPC: vpc-12cacf39 (vpc): 3 instances vpc-af640e85 (usw1-vpc): 1 instance vpc-561c9c6f (usw2-vpc): 1 instance default-vpc: 1 instance EOF cat /logs/agent/agent-output.txt
```

## AWS CDK — answered

10 commands, from `cdk-g3`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, VpcId: .value.Properties.VpcId}' | head -50
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '{ Instances: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {Name: .value.Properties.Tags[0].Value, LogicalId: .key, SubnetId: .value.Properties.SubnetId}], Subnets: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, VpcId: .value.Properties.VpcId}], Vpcs: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC") | {LogicalId: .key, CidrBlock: .value.Properties.CidrBlock}] }'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '{ Instances: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {Name: .value.Properties.Tags[0].Value, LogicalId: .key, SubnetId: .value.Properties.SubnetId}], Subnets: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, VpcId: .value.Properties.VpcId}], Vpcs: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC") | {LogicalId: .key, CidrBlock: .value.Properties.CidrBlock}] }'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '{ Instances: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {Name: .value.Properties.Tags[0].Value, LogicalId: .key, SubnetId: .value.Properties.SubnetId}], Subnets: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, VpcId: .value.Properties.VpcId}], Vpcs: [.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC") | {LogicalId: .key, CidrBlock: .value.Properties.CidrBlock}] }'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws ec2 describe-subnets --subnet-ids subnet-default-a --region us-east-1 2>/dev/null | jq '.Subnets[] | {SubnetId: .SubnetId, VpcId: .VpcId, CidrBlock: .CidrBlock, AvailabilityZone: .AvailabilityZone}'
```

## Alchemy — answered

6 commands, from `alchemy-g3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -E "(Instance|instance)" | head -20
cd /workspace/alchemy && alchemy state list | grep -v "InstanceProfile\|InstanceId\|LaunchTemplate\|InstanceMetadata\|RestrictedAction\|PrivateIP" | grep -i instance
cd /workspace/alchemy && alchemy state tree
cd /workspace/alchemy && for resource in instance defaultVpcServer ltServer privateServer webServer usw1-server usw2-server; do echo "=== $resource ==="; alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>&1 | head -30; done
cd /workspace/alchemy && for resource in defaultVpcServer ltServer privateServer webServer usw1-server usw2-server; do echo "=== $resource ==="; alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>&1 | grep -E '"VpcId"|"InstanceId"|"region"|"Name"' | head -10; done
cd /workspace/alchemy && for resource in defaultVpcServer ltServer privateServer webServer usw1-server usw2-server; do alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>&1 | jq -r '"Instance: \(.id), Name: \(.output.desiredState.Tags[0].Value // "N/A"), Region: \(.output.region), Instance ID: \(.output.InstanceId), VPC ID: \(.output.VpcId)"'; done
```

## Alchemy v2 (Effect) — answered

18 commands, from `alchemy-effect-g2`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-2 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local
# … 6 more
```
