import api from "../client";

import type {
  Project,
  CreateProjectRequest,
} from "../../types/models/project";

export async function getProjects(): Promise<Project[]> {
  const response = await api.get(
    "/api/v1/projects"
  );

  return response.data;
}

export async function getProject(
  projectId: string,
): Promise<Project> {
  const response = await api.get(
    `/api/v1/projects/${projectId}`
  );

  return response.data;
}

export async function createProject(
  payload: CreateProjectRequest,
): Promise<Project> {
  const response = await api.post(
    "/api/v1/projects",
    payload,
  );

  return response.data;
}

export async function deleteProject(
  projectId: string,
): Promise<void> {
  await api.delete(
    `/api/v1/projects/${projectId}`
  );
}
