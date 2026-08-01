# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region --explain
```

## Terraform — answered

4 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_ec2_instance'
cd /workspace/terraform && ./terraform state show -json | jq -r '.values.root_module.child_modules[] | select(.resources != null) | .resources[] | select(.type == "aws_instance") | {address: .address, instance_id: .values.id, region: .values.tags.Region, availability_zone: .values.availability_zone}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | select(.resources != null) | .resources[] | select(.type == "aws_instance") | {address: .address, instance_id: .values.id, region: (.values.tags.Region // .values.availability_zone | split("-")[:-1] | join("-")), availability_zone: .values.availability_zone}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | select(.resources != null) | .resources[] | select(.type == "aws_instance") | "\(.values.availability_zone | split("-")[:-1] | join("-")): \(.values.id)"' | sort | uniq
```

## Pulumi — answered

2 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, instanceId: .outputs.id, region: .outputs.availabilityZone}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::") | .[3]), instanceId: .outputs.id, region: (.outputs.availabilityZone | sub("[a-z]$"; ""))}' | jq -s 'sort_by(.region, .name) | group_by(.region) | map({region: .[0].region, instances: map({name: .name, instanceId: .instanceId})})' 2>/dev/null
```

## AWS CDK — answered

8 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-east-1", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-west-1", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-west-2", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
```

## Alchemy — answered

3 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && for resource in "alchemy-ec2-multiregion/bench/exp-InstanceId" "alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId" "alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId" "alchemy-ec2-multiregion/bench/exp-PrivateInstanceId" "alchemy-ec2-multiregion/bench/usw1-exp-InstanceId" "alchemy-ec2-multiregion/bench/usw2-exp-InstanceId"; do echo "=== $resource ===" alchemy state get "$resource" 2>/dev/null | jq '.output // .props' 2>/dev/null || echo "Not found" done
```
