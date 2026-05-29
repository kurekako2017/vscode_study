# AWS 单页笔记索引

这里收录按服务拆分的中日对照笔记，适合从总览继续往下学。

## 索引

- [S3 学习笔记](./S3.md)
- [EC2 学习笔记](./EC2.md)
- [IAM 学习笔记](./IAM.md)
- [VPC 学习笔记](./VPC.md)
- [Lambda 学习笔记](./Lambda.md)
- [SQS 学习笔记](./SQS.md)
- [SNS 学习笔记](./SNS.md)
- [CloudWatch 学习笔记](./CloudWatch.md)
- [ECR 学习笔记](./ECR.md)
- [ECS 学习笔记](./ECS.md)
- [Fargate 学习笔记](./Fargate.md)
- [EKS 学习笔记](./EKS.md)
- [KMS 学习笔记](./KMS.md)
- [Secrets Manager 学习笔记](./SecretsManager.md)
- [Route 53 学习笔记](./Route53.md)
- [CloudFormation 学习笔记](./CloudFormation.md)
- [CDK 学习笔记](./CDK.md)
- [Terraform 学习笔记](./Terraform.md)

## 高频架构组合

- [高频架构组合索引](./combos/README.md)
- [S3 + CloudFront](./combos/S3_CloudFront.md)
- [EC2 + ALB](./combos/EC2_ALB.md)
- [SQS + Lambda](./combos/SQS_Lambda.md)
- [Docker / ECR / ECS](./combos/Docker_ECR_ECS.md)
- [ECS + ECR + Fargate](./combos/ECS_ECR_Fargate.md)
- [RDS + CloudWatch](./combos/RDS_CloudWatch.md)
- [S3 + Lambda](./combos/S3_Lambda.md)
- [SQS + SNS](./combos/SQS_SNS.md)
- [S3 + SNS](./combos/S3_SNS.md)
- [SQS + Lambda + DLQ](./combos/SQS_Lambda_DLQ.md)
- [RDS + Lambda](./combos/RDS_Lambda.md)
- [S3 + Athena](./combos/S3_Athena.md)
- [Glue + S3](./combos/Glue_S3.md)
- [Kinesis + Lambda](./combos/Kinesis_Lambda.md)
- [Redshift + S3](./combos/Redshift_S3.md)
- [Athena + Glue](./combos/Athena_Glue.md)
- [Kinesis + Firehose](./combos/Kinesis_Firehose.md)
- [Lake Formation + Glue](./combos/LakeFormation_Glue.md)
- [Athena + QuickSight](./combos/Athena_QuickSight.md)
- [Redshift + QuickSight](./combos/Redshift_QuickSight.md)
- [Lake Formation + Athena](./combos/LakeFormation_Athena.md)
- [QuickSight + Lake Formation](./combos/QuickSight_LakeFormation.md)
- [Redshift + Lake Formation](./combos/Redshift_LakeFormation.md)
- [Web Project 部署流程](./combos/WebProject_Deployment.md)
- [Batch 部署流程](./combos/Batch_Deployment.md)

## 建议阅读顺序

1. 先看 [AWS知识点总览（中日对照）](../AWS_Knowledge_Map.md)
2. 再按 S3、IAM、VPC、EC2、Lambda、SQS、SNS、CloudWatch、ECR、ECS、EKS、Fargate、KMS、Secrets Manager、Route 53、CloudFormation、CDK、Terraform 的顺序阅读
3. 然后看高频架构组合，把单服务串成一条完整链路
4. 最后配合 LocalStack 的项目示例做实操
