# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-h3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,PrivateIpAddress,region --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-h3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json
aws ec2 describe-instances --region us-west-1 --output json
aws ec2 describe-instances --region us-west-2 --output json
```

## Terraform — answered

14 commands, from `terraform-h3`.

```sh
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address, values: {instance_id: .values.id, ami: .values.ami, instance_type: .values.instance_type, region: .values.availability_zone | sub("[a-z]$"; ""), vpc_id: .values.vpc_security_group_ids, subnet_id: .values.subnet_id}}'
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.default_vpc_server' | grep -E "id|ami|instance_type|availability_zone|vpc_id|subnet_id"
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.launch_template_server' | grep -E "id|ami|instance_type|availability_zone|vpc_id|subnet_id"
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.private_server' | grep -E "id|ami|instance_type|availability_zone|vpc_id|subnet_id"
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.web_server' | grep -E "id|ami|instance_type|availability_zone|vpc_id|subnet_id"
cd /workspace/terraform && ./terraform state show 'module.west1.aws_instance.server' | grep -E "id|ami|instance_type|availability_zone|vpc_id|subnet_id"
cd /workspace/terraform && ./terraform state show 'module.west2.aws_instance.server' | grep -E "id|ami|instance_type|availability_zone|vpc_id|subnet_id"
cd /workspace/terraform && ./terraform state list | grep aws_subnet
cd /workspace/terraform && ./terraform state show 'module.primary.aws_subnet.private' | grep -E "id|vpc_id"
cd /workspace/terraform && ./terraform state show 'module.primary.aws_subnet.public' | grep -E "id|vpc_id"
cd /workspace/terraform && ./terraform state show 'module.west1.aws_subnet.public' | grep -E "id|vpc_id"
# … 2 more
```

## Pulumi — answered

6 commands, from `pulumi-h3`.

```sh
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | head -100
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | split("-") | .[0:-1] | join("-"), id: .outputs.id, vpcId: .outputs.vpcId, subnetId: .outputs.subnetId, tags: .outputs.tags}' | head -200
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' | jq -s 'map({ name: (.urn | split("::")[-1]), instanceId: .outputs.id, availabilityZone: .outputs.availabilityZone, vpcId: .outputs.vpcId, subnetId: .outputs.subnetId, primaryNetworkInterfaceId: .outputs.primaryNetworkInterfaceId, instanceType: .outputs.instanceType, tags: .outputs.tags })'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc" or .type == "aws:ec2/subnet:Subnet") | {type, urn: (.urn | split("::")[-1]), vpcId: .outputs.vpcId, availabilityZone: .outputs.availabilityZone, id: .outputs.id}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("Vpc") or contains("Subnet")) | select(.outputs.id == "subnet-default-c" or .urn | contains("default"))' | head -100
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" or .type == "aws:ec2/vpc:Vpc" or (.type == "aws:ec2:DefaultSubnet")) | {type, urn: (.urn | split("::")[-1]), id: .outputs.id, vpcId: .outputs.vpcId}'
```

## AWS CDK — answered

9 commands, from `cdk-h3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, Type: .value.Type, VpcId: .value.Properties.VpcId, CidrBlock: .value.Properties.CidrBlock}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, InstanceType: .value.Properties.InstanceType, SubnetId: .value.Properties.SubnetId, Tags: .value.Properties.Tags}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, InstanceType: .value.Properties.InstanceType, SubnetId: .value.Properties.SubnetId, Tags: .value.Properties.Tags}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId,Properties]' --output json 2>/dev/null
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output json 2>/dev/null
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output json 2>/dev/null
aws ec2 describe-instances --instance-ids i-6189a06b5c98b9e2e i-5be74f530ac36cb44 i-a31ba0f11f3f69b0a i-f15bcebfa2e18553c --region us-east-1 --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`].Value|[0],VpcId,SubnetId,InstanceType,State.Name]' --output json
```

## Alchemy — answered

17 commands, from `alchemy-h3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-InstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-PrivateInstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-exp-InstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw2-exp-InstanceId
cd /workspace/alchemy && alchemy state list | grep "aws::Instance"
cd /workspace/alchemy && alchemy state tree
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/private
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer
# … 5 more
```

## Alchemy v2 (Effect) — answered

13 commands, from `alchemy-effect-h3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 us-west-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 us-west-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-1 us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-2 us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local 2>&1
# … 1 more
```
