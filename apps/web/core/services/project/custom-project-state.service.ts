/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { API_BASE_URL } from "@plane/constants";
import { APIService } from "@/services/api.service";

export class CustomProjectStateService extends APIService {
  constructor() {
    super(API_BASE_URL);
  }

  async getWorkspaceProjectStateSettings(workspaceSlug: string): Promise<any> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/project-states/settings/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async updateWorkspaceProjectStateSettings(workspaceSlug: string, data: any): Promise<any> {
    return this.patch(`/api/orca/workspaces/${workspaceSlug}/project-states/settings/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async getProjectStates(workspaceSlug: string): Promise<any[]> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/project-states/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async createProjectState(workspaceSlug: string, data: any): Promise<any> {
    return this.post(`/api/orca/workspaces/${workspaceSlug}/project-states/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async updateProjectState(workspaceSlug: string, stateId: string, data: any): Promise<any> {
    return this.patch(`/api/orca/workspaces/${workspaceSlug}/project-states/${stateId}/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async deleteProjectState(workspaceSlug: string, stateId: string): Promise<any> {
    return this.delete(`/api/orca/workspaces/${workspaceSlug}/project-states/${stateId}/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async getProjectStateProperty(workspaceSlug: string, projectId: string): Promise<any> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/projects/${projectId}/project-state/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async updateProjectStateProperty(workspaceSlug: string, projectId: string, data: any): Promise<any> {
    return this.patch(`/api/orca/workspaces/${workspaceSlug}/projects/${projectId}/project-state/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }
}
