# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-h3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region
```

## No tool (AWS CLI) — answered

3 commands, from `bare-h3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]' 2>/dev/null || echo "[]"
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]' 2>/dev/null || echo "[]"
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]' 2>/dev/null || echo "[]"
```

## Terraform — answered

5 commands, from `terraform-h3`.

```sh
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | {module_name: .address, instances: [.resources[] | select(.type == "aws_instance") | {name: .address, instance_id: .values.id, region: .values.tags.region // "unknown"}]}'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | {module: .address, instances: [.resources[] | select(.type == "aws_instance") | {instance_id: .values.id, region: .values.availability_zone}]}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | (.address | split(".")[1]) as $region | .resources[] | select(.type == "aws_instance") | "\($region): \(.values.id)"' | sort
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | select(.resources[]? | select(.type == "aws_instance")) | .resources[] | select(.type == "aws_instance") | {instance_id: .values.id, az: .values.availability_zone, region: (.values.availability_zone | gsub("[a-z]$"; ""))} | "\(.region): \(.instance_id)"' | sort -u
```

## Pulumi — answered

1 commands, from `pulumi-h3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, instance_id: .outputs.id, availability_zone: .outputs.availabilityZone, region: (.outputs.availabilityZone | sub("[a-z]$"; ""))}' -r
```

## AWS CDK — answered

5 commands, from `cdk-h3`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, PhysicalId: .value.Properties}' | head -50
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Region: "us-east-1"}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Region: "us-west-1"}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Region: "us-west-2"}'
```

## Alchemy — answered

4 commands, from `alchemy-h3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance | jq '.output'
cd /workspace/alchemy && alchemy state tree
cd /workspace/alchemy && for res in exp-DefaultVPCInstanceId exp-InstanceId exp-LaunchTemplateInstanceId exp-PrivateInstanceId usw1-exp-InstanceId usw2-exp-InstanceId; do echo "=== $res ==="; alchemy state get "alchemy-ec2-multiregion/bench/$res" 2>/dev/null | jq '.output' 2>/dev/null || echo "Not found"; done
```

## Alchemy v2 (Effect) — answered

9 commands, from `alchemy-effect-h3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-1 us-west-1.run.ts --local && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-2 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn ExpInstanceId us-west-1.run.ts --local | jq -r '.attr.physicalResourceId' 2>/dev/null || echo "Not found"
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn ExpInstanceId us-west-1.run.ts --local
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== Region: ${stack##*-} ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local | grep -i "^Exp.*InstanceId" | while read resource; do result=$(alchemy state get --stack "$stack" --stage bench --fqn "$resource" us-west-1.run.ts --local) instance_id=$(echo "$result" | jq -r '.props.value // empty' 2>/dev/null) if [[ ! -z "$instance_id" && "$instance_id" =~ ^i- ]]; then echo "$resource: $instance_id" fi done done
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | xargs grep -l "ExpInstanceId\|ExpDefaultVPCInstanceId\|ExpLaunchTemplateInstanceId\|ExpPrivateInstanceId" | while read file; do region=$(basename $(dirname $(dirname "$file"))) jq -r '.props.value // empty' "$file" 2>/dev/null | grep -E "^i-" && echo " (from: $region)" done
cd /workspace/alchemy && { echo "US-EAST-1:" find .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1 -name "*.json" -type f -exec jq -r 'select(.props.value and .props.value | startswith("i-")) | .props.value' {} \; echo "" echo "US-WEST-1:" find .alchemy/state/alchemy-effect-ec2-multiregion-us-west-1 -name "*.json" -type f -exec jq -r 'select(.props.value and .props.value | startswith("i-")) | .props.value' {} \; echo "" echo "US-WEST-2:" find .alchemy/state/alchemy-effect-ec2-multiregion-us-west-2 -name "*.json" -type f -exec jq -r 'select(.props.value and .props.value | startswith("i-")) | .props.value' {} \; }
cd /workspace/alchemy && { echo "US-EAST-1:" find .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1 -name "*.json" -type f -exec jq -r 'select(.props.value | type == "string" and startswith("i-")) | .props.value' {} \; echo "" echo "US-WEST-1:" find .alchemy/state/alchemy-effect-ec2-multiregion-us-west-1 -name "*.json" -type f -exec jq -r 'select(.props.value | type == "string" and startswith("i-")) | .props.value' {} \; echo "" echo "US-WEST-2:" find .alchemy/state/alchemy-effect-ec2-multiregion-us-west-2 -name "*.json" -type f -exec jq -r 'select(.props.value | type == "string" and startswith("i-")) | .props.value' {} \; }
```
