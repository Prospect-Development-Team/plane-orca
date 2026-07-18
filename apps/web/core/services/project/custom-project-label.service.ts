/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { API_BASE_URL } from "@plane/constants";
import { APIService } from "@/services/api.service";

export class CustomProjectLabelService extends APIService {
  constructor() {
    super(API_BASE_URL);
  }

  async getSettings(workspaceSlug: string): Promise<any> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/project-labels/settings/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async updateSettings(workspaceSlug: string, data: any): Promise<any> {
    return this.patch(`/api/orca/workspaces/${workspaceSlug}/project-labels/settings/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async getProjectProperty(workspaceSlug: string, projectId: string): Promise<any> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/projects/${projectId}/project-label/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async updateProjectProperty(workspaceSlug: string, projectId: string, data: any): Promise<any> {
    return this.patch(`/api/orca/workspaces/${workspaceSlug}/projects/${projectId}/project-label/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async getProjectLabels(workspaceSlug: string): Promise<any[]> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/project-labels/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async createProjectLabel(workspaceSlug: string, data: any): Promise<any> {
    return this.post(`/api/orca/workspaces/${workspaceSlug}/project-labels/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async updateProjectLabel(workspaceSlug: string, labelId: string, data: any): Promise<any> {
    return this.patch(`/api/orca/workspaces/${workspaceSlug}/project-labels/${labelId}/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async deleteProjectLabel(workspaceSlug: string, labelId: string): Promise<any> {
    return this.delete(`/api/orca/workspaces/${workspaceSlug}/project-labels/${labelId}/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }

  async getProjectLabelAssignments(workspaceSlug: string, projectId: string): Promise<any[]> {
    return this.get(`/api/orca/workspaces/${workspaceSlug}/projects/${projectId}/project-labels/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async updateProjectLabelAssignments(workspaceSlug: string, projectId: string, labelIds: string[]): Promise<any[]> {
    return this.post(`/api/orca/workspaces/${workspaceSlug}/projects/${projectId}/project-labels/`, {
      label_ids: labelIds,
    })
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response;
      });
  }
}
