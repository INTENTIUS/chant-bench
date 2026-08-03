# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-r5`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show InstanceId,region --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-g3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]' 2>/dev/null | sort
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]' 2>/dev/null | sort
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]' 2>/dev/null | sort
```

## Terraform — answered

3 commands, from `terraform-g3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.resources[] | select(.type=="aws_instance") | "\(.values.tags.Name // .address) (\(.values.id)) - Region: \(.values.availability_zone | .[:-1])"' 2>/dev/null | head -50
cd /workspace/terraform && ./terraform state list
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | select(.address | startswith("module.primary") or startswith("module.west")) | .resources[] | select(.type == "aws_instance") | { module: .address, id: .values.id, region: (.values.availability_zone | .[:-1]) }' | jq -s 'sort_by(.region)' | jq -r '.[] | "\(.region): \(.id) (\(.module))"'
```

## Pulumi — answered

1 commands, from `pulumi-g3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, instanceId: .outputs.id, region: .outputs.availabilityZone}'
```

## AWS CDK — answered

8 commands, from `cdk-g3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | keys[] as $key | select(.Resources[$key].Type=="AWS::EC2::Instance") | {logicalId: $key, resource: .Resources[$key]}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type=="AWS::EC2::Instance") | {logicalId: .key, resource: .value}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type=="AWS::EC2::Instance") | {logicalId: .key, resource: .value}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type=="AWS::EC2::Instance") | {logicalId: .key, resource: .value}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].{LogicalId:LogicalResourceId,PhysicalId:PhysicalResourceId}' --output json
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].{LogicalId:LogicalResourceId,PhysicalId:PhysicalResourceId}' --output json
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].{LogicalId:LogicalResourceId,PhysicalId:PhysicalResourceId}' --output json
```

## Alchemy — answered

17 commands, from `alchemy-g3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state tree
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-InstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-PrivateInstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-exp-InstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw2-exp-InstanceId
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-server
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw2-server
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/web
# … 5 more
```

## Alchemy v2 (Effect) — answered

23 commands, from `alchemy-effect-g2`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-2 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn WebServer us-west-1.run.ts --local | jq -r '.attr.id'
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn PrivateServer us-west-1.run.ts --local | jq -r '.attr.id'
# … 11 more
```
