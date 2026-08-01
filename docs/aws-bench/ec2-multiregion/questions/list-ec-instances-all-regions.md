# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region --explain
```

## No tool (AWS CLI) — answered

1 commands, from `bare-m3`.

```sh
# Query EC2 instances in all three regions for region in us-east-1 us-west-1 us-west-2; do echo "=== $region ===" >&2 aws ec2 describe-instances --region "$region" --output json | \ jq -r '.Reservations[].Instances[] | .InstanceId' 2>/dev/null done
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

7 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Stack: "us-east-1"}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Stack: "us-west-1"}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Stack: "us-west-2"}'
```

## Alchemy — answered

3 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && for resource in "alchemy-ec2-multiregion/bench/exp-InstanceId" "alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId" "alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId" "alchemy-ec2-multiregion/bench/exp-PrivateInstanceId" "alchemy-ec2-multiregion/bench/usw1-exp-InstanceId" "alchemy-ec2-multiregion/bench/usw2-exp-InstanceId"; do echo "=== $resource ===" alchemy state get "$resource" 2>/dev/null | jq '.output // .props' 2>/dev/null || echo "Not found" done
```

## Alchemy v2 (Effect) — answered

17 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state tree us-east-1.run.ts --local 2>&1 | head -50
cd /workspace/alchemy && alchemy state tree us-west-1.run.ts --local 2>&1 | head -50
cd /workspace/alchemy && alchemy state tree us-west-2.run.ts --local 2>&1 | head -50
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-east-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-2.run.ts --local 2>&1 | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-east-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-2.run.ts --local 2>&1
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | head -20
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | xargs grep -l '"resourceType".*Instance' | sort
cat /workspace/alchemy/.alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/DefaultVpcServer.json | jq '{resource: .resourceType, name: .props.instanceName, instanceId: .attr.instanceId}'
# … 5 more
```
