# Which EC2 instances are in which VPCs across all regions?

`list-ec-instances-by-vpc-across` · the answer aws-bench grades against: **6 instances across 4 VPCs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-h3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
```

## No tool (AWS CLI) — answered

6 commands, from `bare-h3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[*].Instances[*].[InstanceId,VpcId,SubnetId,InstanceType,State.Name]' | jq -r '.[] | .[] | @csv'
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[*].Instances[*].[InstanceId,VpcId,SubnetId,InstanceType,State.Name]' | jq -r '.[] | .[] | @csv'
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[*].Instances[*].[InstanceId,VpcId,SubnetId,InstanceType,State.Name]' | jq -r '.[] | .[] | @csv'
aws ec2 describe-vpcs --region us-east-1 --output json --query 'Vpcs[*].[VpcId,Tags[?Key==`Name`].Value|[0]]' | jq -r '.[] | @csv'
aws ec2 describe-vpcs --region us-west-1 --output json --query 'Vpcs[*].[VpcId,Tags[?Key==`Name`].Value|[0]]' | jq -r '.[] | @csv'
aws ec2 describe-vpcs --region us-west-2 --output json --query 'Vpcs[*].[VpcId,Tags[?Key==`Name`].Value|[0]]' | jq -r '.[] | @csv'
```

## Terraform — answered

10 commands, from `terraform-h3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E "aws_instance|aws_vpc"
cd /workspace/terraform && ./terraform show -json
cd /workspace/terraform && ./terraform show -json | jq -r ' .values.root_module as $root | ( [$root.resources[]? | select(.type == "aws_instance" or .type == "aws_vpc")] + [$root.child_modules[]?.resources[]? | select(.type == "aws_instance" or .type == "aws_vpc")] ) | group_by(.values.tags.region // .values.availability_zone[:-1] // "unknown") | map({ region: .[0].values.tags.region // .[0].values.availability_zone[:-1] // "unknown", resources: map({ address: .address, type: .type, name: .name, vpc_id: .values.vpc_id // .values.id, id: .values.id, tags: .values.tags }) }) '
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && jq '.values.root_module.resources[] | select(.type == "aws_instance" or .type == "aws_vpc") | {address, type, name, region: .values.availability_zone[:-1], vpc_id: .values.vpc_id, id: .values.id, tags: .values.tags}' /tmp/state.json
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | keys'
cd /workspace/terraform && ./terraform show -json | jq ' [ (.values.root_module.resources[] | select(.type == "aws_instance")), (.values.root_module.child_modules[]? | .resources[]? | select(.type == "aws_instance")) ] | map({ address: .address, name: .name, vpc_id: .values.vpc_id, availability_zone: .values.availability_zone, subnet_id: .values.subnet_id })'
cd /workspace/terraform && ./terraform show -json | jq ' [ (.values.root_module.resources[] | select(.type == "aws_vpc" or .type == "aws_subnet")), (.values.root_module.child_modules[]? | .resources[]? | select(.type == "aws_vpc" or .type == "aws_subnet")) ] | map({ type: .type, address: .address, id: .values.id, vpc_id: .values.vpc_id, availability_zone: .values.availability_zone, tags: .values.tags })'
cd /workspace/terraform && ./terraform show -json | jq ' [ (.values.root_module.resources[] | select(.type == "aws_launch_template")), (.values.root_module.child_modules[]? | .resources[]? | select(.type == "aws_launch_template")) ] | map({ address: .address, id: .values.id, vpc_id: .values.vpc_specification[0].vpc_id })'
cd /workspace/terraform && ./terraform show -json | jq ' [ (.values.root_module.resources[] | select(.type == "aws_instance")), (.values.root_module.child_modules[]? | .resources[]? | select(.type == "aws_instance")) ] | map({ address: .address, name: .name, availability_zone: .values.availability_zone, subnet_id: .values.subnet_id, vpc_id: .values.vpc_id, launch_template_id: .values.launch_template[0].id })'
find /workspace/terraform/modules -name "*.tf" -type f
```

## Pulumi — answered

10 commands, from `pulumi-h3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, region: .outputs.availabilityZone | sub(".$"; ""), vpc_id: .outputs.vpcId, instance_id: .outputs.id, subnet_id: .outputs.subnetId}' 2>/dev/null | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, outputs: .outputs}' 2>/dev/null | head -200
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone, arn: .arn}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | { subnets: ($resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, vpc_id: .outputs.vpcId, az: .outputs.availabilityZone}), instances: ($resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[3], instance_id: .outputs.id, subnet_id: .outputs.subnetId, region: (.outputs.availabilityZone | sub(".$"; "")), az: .outputs.availabilityZone}) } | .instances as $inst | .subnets as $subnets_map | $inst[] | . as $instance | { instance_name: .name, instance_id: .instance_id, region: .region, availability_zone: .az, subnet_id: .subnet_id, vpc_id: ($subnets_map[] | select(.subnet_id == $instance.subnet_id) | .vpc_id) } ' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && jq ' .deployment.resources | [ group_by(.type) as $by_type | ( $by_type[] | select(.[0].type == "aws:ec2/instance:Instance") as $instances | $by_type[] | select(.[0].type == "aws:ec2/subnet:Subnet") as $subnets | $instances[] | . as $inst | { instance_name: (.urn | split("::")[3]), instance_id: .outputs.id, region: (.outputs.availabilityZone | sub(".$"; "")), availability_zone: .outputs.availabilityZone, subnet_id: .outputs.subnetId, vpc_id: ( ($subnets[] | select(.outputs.id == $inst.outputs.subnetId) | .outputs.vpcId) ) } ) ] | .[] ' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | \ jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | { name: (.urn | split("::")[3]), instance_id: .outputs.id, region: (.outputs.availabilityZone | sub(".$"; "")), subnet_id: .outputs.subnetId }' > /tmp/instances.json && \ ./pulumi-export 2>/dev/null | \ jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | { subnet_id: .outputs.id, vpc_id: .outputs.vpcId }' > /tmp/subnets.json && \ jq -s 'reduce .[][0][] as $inst ({}; .[$inst.subnet_id] = $inst) as $inst_map | input | map(. as $subnet | { subnet_id: $subnet.subnet_id, vpc_id: $subnet.vpc_id, instances: [ ($inst_map | to_entries[] | select(.value.subnet_id == $subnet.subnet_id) | .value) ] } )' /tmp/instances.json /tmp/subnets.json 2>/dev/null | head -100
cd /workspace/pulumi && python3 << 'EOF' import json import subprocess # Get the pulumi state result = subprocess.run(['./pulumi-export'], capture_output=True, text=True) state = json.loads(result.stdout) # Extract instances and subnets instances = [] subnets = {} for resource in state['deployment']['resources']: if resource['type'] == 'aws:ec2/instance:Instance': instances.append({ 'name': resource['urn'].split('::')[3], 'instance_id': resource['outputs'].get('id'), 'region': resource['outputs'].get('availabilityZone', '')[:-1], # Remove last char (AZ letter) 'availability_zone': resource['outputs'].get('availabilityZone'), 'subnet_id': resource['outputs'].get('subnetId') }) elif resource['type'] == 'aws:ec2/subnet:Subnet': subnets[resource['outputs'].get('id')] = resource['outputs'].get('vpcId') # Correlate instances with VPCs results = [] for inst in instances: vpc_id = subnets.get(inst['subnet_id'], 'unknown') results.append({ 'instance_name': inst['name'], 'instance_id': inst['instance_id'], 'region': inst['region'], 'availability_zone': inst['availability_zone'], 'subnet_id': inst['subnet_id'], 'vpc_id': vpc_id }) # Sort by region then VPC results.sort(key=lambda x: (x['region'], x['vpc_id'])) # Print results print(json.dumps(results, indent=2)) EOF
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {vpc_id: .outputs.id, cidr_block: .outputs.cidrBlock, is_default: .outputs.isDefault}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.outputs.id == "i-438371dd30873e1f7") | {instance_name: (.urn | split("::")[3]), vpc_id: .outputs.vpcId, subnet_id: .outputs.subnetId, private_ip: .outputs.privateIp, inputs: .inputs}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/defaultVpc:DefaultVpc" or .type == "aws:ec2:DefaultVpc") | {vpc_id: .outputs.id, is_default: .outputs.isDefault}'
```

## AWS CDK — answered

14 commands, from `cdk-h3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type | startswith("AWS::EC2::")) | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type | startswith("AWS::EC2::")) | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type | startswith("AWS::EC2::")) | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type | startswith("AWS::EC2::")) | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::Subnet") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId, type: .ResourceType}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::Subnet") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId, type: .ResourceType}'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::Subnet") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId, type: .ResourceType}'
aws ec2 describe-instances --instance-ids i-6189a06b5c98b9e2e i-5be74f530ac36cb44 i-a31ba0f11f3f69b0a i-f15bcebfa2e18553c --region us-east-1 --query 'Reservations[*].Instances[*].[InstanceId, Tags[?Key==`Name`].Value|[0], VpcId, SubnetId, State.Name]' --output text
# … 2 more
```

## Alchemy — answered

12 commands, from `alchemy-h3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state list | head -50
cd /workspace/alchemy && alchemy state list | grep -E "(instance|server)" | sort
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-server
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw2-server
cd /workspace/alchemy && alchemy state list | grep -E "exp-(DefaultVPCInstanceId|InstanceId|LaunchTemplateInstanceId|PrivateInstanceId)" | sort
cd /workspace/alchemy && for file in instance defaultVpcServer ltServer privateServer webServer; do echo "=== $file ==="; alchemy state get alchemy-ec2-multiregion/bench/$file 2>/dev/null | grep -A 2 '"kind"'; done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/defaultVpcServer 2>/dev/null | jq '.output | {id, region, VpcId, InstanceId, SubnetId}'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/ltServer 2>/dev/null | jq '.output | {id, region, VpcId, InstanceId, SubnetId}'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/privateServer 2>/dev/null | jq '.output | {id, region, VpcId, InstanceId, SubnetId}'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer 2>/dev/null | jq '.output | {id, region, VpcId, InstanceId, SubnetId}'
```

## Alchemy v2 (Effect) — answered

16 commands, from `alchemy-effect-h3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state tree us-west-1.run.ts --local 2>&1 | head -100
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1 | jq .
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn LaunchTemplateServer us-west-1.run.ts --local 2>&1 | jq .
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn PrivateServer us-west-1.run.ts --local 2>&1 | jq .
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local 2>&1 | jq .
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1 | jq .
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1 | jq .
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn WebLaunchTemplate us-west-1.run.ts --local 2>&1 | jq .
# … 4 more
```
