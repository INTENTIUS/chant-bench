# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

4 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show providerDefault
cd /workspace/chant && chant search "kind:EC2::Instance !->kind:EC2::VPC ->attr:providerDefault=true" --at latest --env floci --show VpcId,region
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain | grep -v "vpc-default"
```

## Terraform — answered

7 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform show -json | head -100
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | .resources[] | select(.type == "aws_instance") | {address: .address, instance_id: .values.id, subnet_id: .values.subnet_id, region: .values.region, vpc_in_name: .values.tags_all.Name}' 2>/dev/null | head -100
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_subnet") | {address: .address, subnet_id: .values.id, vpc_id: .values.vpc_id, region: .values.region}' 2>/dev/null | head -50
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_vpc") | {address: .address, vpc_id: .values.id, is_default: .values.default, region: .values.region, cidr: .values.cidr_block}' 2>/dev/null
cd /workspace/terraform && ./terraform show -json | jq ' [ (.values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | (.resources[] | select(.type == "aws_instance") as $inst | .values as $values | $inst | { instance_id: $values.id, address: .address, subnet_id: $values.subnet_id, region: $values.region, name: $values.tags_all.Name } ) ) ] | unique_by(.instance_id) | map(.) ' 2>/dev/null
cd /workspace/terraform && ./terraform show -json | jq ' { vpc_info: [ .values.root_module.child_modules[] | .resources[] | select(.type == "aws_vpc") | {vpc_id: .values.id, is_default: .values.default, region: .values.region, cidr: .values.cidr_block} ], subnet_info: [ .values.root_module.child_modules[] | .resources[] | select(.type == "aws_subnet") | {subnet_id: .values.id, vpc_id: .values.vpc_id, region: .values.region} ], instance_info: [ .values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | .resources[] | select(.type == "aws_instance") | {instance_id: .values.id, subnet_id: .values.subnet_id, region: .values.region, name: .values.tags_all.Name} ] } ' 2>/dev/null > /tmp/terraform_state.json && cat /tmp/terraform_state.json
cat > /tmp/analyze.jq << 'EOF' # Create mapping of subnet -> VPC (.subnet_info | map({(.subnet_id): .vpc_id}) | add) as $subnet_to_vpc | # Identify default VPCs (.vpc_info | map(select(.is_default == true) | .vpc_id) | .[]) as $default_vpc_id | # Enrich instances with VPC info (.instance_info | map( . + { vpc_id: ( if .subnet_id == "subnet-default-c" or .subnet_id == "subnet-default-a" or .subnet_id == "subnet-default-b" then "vpc-default" else $subnet_to_vpc[.subnet_id] end ) } ) | unique_by(.instance_id)) as $instances | # Separate into default and non-default VPC instances { instances_in_default_vpc: ($instances | map(select(.vpc_id == $default_vpc_id or .vpc_id == "vpc-default"))), instances_not_in_default_vpc: ($instances | map(select(.vpc_id != $default_vpc_id and .vpc_id != "vpc-default"))) } EOF jq -f /tmp/analyze.jq /tmp/terraform_state.json
```

## Pulumi — answered

4 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc" or .type == "aws:ec2/subnet:Subnet") | {type, urn, outputs: {id, vpcId, isDefault: .outputs.isDefault}}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn, id: .outputs.id, vpcId: .outputs.vpcId}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {urn, id: .outputs.id, isDefault: .outputs.isDefault}'
```

## AWS CDK — answered

10 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {LogicalId: .key, VpcId: .value.Properties.VpcId, SubnetId: .value.Properties.Tags[0]}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.ResourcesVpc' 2>/dev/null | head -20
```
