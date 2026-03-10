# Outputs for AWS ECS Fargate module

output "cluster_id" {
  description = "ECS cluster ID"
  value       = aws_ecs_cluster.connector.id
}

output "service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.connector.name
}

output "task_definition_arn" {
  description = "ARN of the task definition"
  value       = aws_ecs_task_definition.connector.arn
}

output "task_role_arn" {
  description = "ARN of the task IAM role"
  value       = aws_iam_role.ecs_task.arn
}
