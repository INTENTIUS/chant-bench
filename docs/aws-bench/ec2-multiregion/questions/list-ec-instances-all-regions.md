# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region
```

## No tool (AWS CLI) — answered

1 commands, from `bare-m3`.

```sh
# Query EC2 instances in all three regions for region in us-east-1 us-west-1 us-west-2; do echo "=== $region ===" >&2 aws ec2 describe-instances --region "$region" --output json | \ jq -r '.Reservations[].Instances[] | .InstanceId' 2>/dev/null done
```

## Terraform — answered

8 commands, from `terraform-m1`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E '^aws_instance\.' | head -20
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.resources[] | select(.type=="aws_instance") | "\(.address): \(.values.id) (region: \(.values.availability_zone | gsub("[a-z]$"; "")))"' 2>/dev/null
/workspace/terraform/terraform -chdir=/workspace/terraform state list | grep -E 'aws_instance\.'
/workspace/terraform/terraform -chdir=/workspace/terraform show -json | jq -r '.values.root_module.child_modules[] | select(.resources[] | select(.type=="aws_instance")) | .resources[] | select(.type=="aws_instance") | "\(.values.id) (module: \(.address | split(".")[0]), region: \(.values.availability_zone | gsub("[a-z]$"; "")))"'
/workspace/terraform/terraform -chdir=/workspace/terraform state show -json module.primary.aws_instance.default_vpc_server | jq '{instance_id: .values.id, availability_zone: .values.availability_zone}'
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && cat /tmp/state.json | jq '.values.root_module.resources[] | select(.type=="aws_instance") | {address, id: .values.id, availability_zone: .values.availability_zone}'
grep -A 5 '"type": "aws_instance"' /workspace/terraform/terraform.tfstate | grep -E '"id"|"availability_zone"|"module"|"name"' | head -50
grep -E '(\"id\":|\"region\":|\"availability_zone\":|"module":)' /workspace/terraform/terraform.tfstate | grep -E '(aws_instance|\"id\"|\"region\"|\"availability_zone\")' | paste - - - - | head -20
```

## Pulumi — answered

2 commands, from `pulumi-m1`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, instance_id: .outputs.id, region: .outputs.tags.aws_region, availability_zone: .outputs.availabilityZone}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[-1]), instance_id: .outputs.id, availability_zone: .outputs.availabilityZone} | (.availability_zone | match("([a-z]+-[a-z]+-\\d+)").captures[0].string) as $region | "\($region)\t\(.instance_id)\t\(.name)"' | sort
```

## AWS CDK — answered

3 commands, from `cdk-m3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key): \(.value.Properties.ImageId // "N/A")"'
cd /workspace/cdk_app # Get all stacks STACKS=( "ec2-multiregion-QARoles-us-east-1" "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2" ) # Extract region from stack name declare -A regions regions[ec2-multiregion-QARoles-us-east-1]="us-east-1" regions[ec2-multiregion-EC2-ks84v1fh12-us-east-1]="us-east-1" regions[ec2-multiregion-EC2-ls9fuhb522-us-west-1]="us-west-1" regions[ec2-multiregion-EC2-ls9fuhb522-us-west-2]="us-west-2" echo "EC2 Instance IDs by Region:" echo "============================" for stack in "${STACKS[@]}"; do region=${regions[$stack]} echo "" echo "Stack: $stack (Region: $region)" # Get stack resources and filter for EC2 instances aws cloudformation describe-stack-resources \ --stack-name "$stack" \ --region "$region" \ --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' \ --output text 2>/dev/null | while read -r logical physical; do if [ ! -z "$logical" ]; then echo " $logical: $physical" fi done || echo " (Stack not found or no EC2 instances)" done
```

## Alchemy — answered

3 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && for resource in "alchemy-ec2-multiregion/bench/exp-InstanceId" "alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId" "alchemy-ec2-multiregion/bench/exp-LaunchTemplateInstanceId" "alchemy-ec2-multiregion/bench/exp-PrivateInstanceId" "alchemy-ec2-multiregion/bench/usw1-exp-InstanceId" "alchemy-ec2-multiregion/bench/usw2-exp-InstanceId"; do echo "=== $resource ===" alchemy state get "$resource" 2>/dev/null | jq '.output // .props' 2>/dev/null || echo "Not found" done
```

## Alchemy v2 (Effect) — answered

8 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state stages --stack "$stack" us-west-1.run.ts --local 2>&1; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>&1 | grep -i "instance"; done
cd /workspace/alchemy && alchemy state resources --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && for inst in "DefaultVpcServer" "LaunchTemplateServer" "PrivateServer" "WebServer"; do echo "=== $inst ==="; alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "$inst" us-west-1.run.ts --local 2>&1 | jq '.attr.id // .attr.instanceId // .props.instanceId // empty' 2>&1; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>&1; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state get --stack "$stack" --stage bench --fqn "WebServer" us-west-1.run.ts --local 2>&1 | jq '.attr.id // .attr.instanceId // .props.instanceId // empty' 2>&1; done
```
