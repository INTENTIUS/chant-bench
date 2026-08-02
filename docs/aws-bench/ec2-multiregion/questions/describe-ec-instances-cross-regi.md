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

14 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance"))' > /tmp/east1-instances.json && cat /tmp/east1-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance"))' > /tmp/west1-instances.json && cat /tmp/west1-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance"))' > /tmp/west2-instances.json && cat /tmp/west2-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC")) | map({key: .key, type: .value.Type, properties: .value.Properties})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | keys' | head -30
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | {vpc: .ResourcesVpc46097686, publicSubnet: .ResourcesVpcPublicSubnet1Subnet7103FD34, privateSubnet: .ResourcesVpcPrivateSubnet1Subnet98586872}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | {vpc: .ResourcesVpc46097686, publicSubnet: .ResourcesVpcPublicSubnet1Subnet7103FD34}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | {vpc: .ResourcesVpc46097686, publicSubnet: .ResourcesVpcPublicSubnet1Subnet7103FD34}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
# … 2 more
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
