/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { observable, action, makeObservable, runInAction } from "mobx";
import { CustomProjectStateService } from "@/services/project/custom-project-state.service";
import type { CoreRootStore } from "../root.store";

export interface ICustomProjectStateStore {
  settings: any | null;
  states: any[] | null;
  projectProperties: Record<string, any>;
  fetchSettings: (workspaceSlug: string) => Promise<any>;
  updateSettings: (workspaceSlug: string, data: any) => Promise<any>;
  fetchStates: (workspaceSlug: string) => Promise<any[]>;
  createState: (workspaceSlug: string, data: any) => Promise<any>;
  updateState: (workspaceSlug: string, stateId: string, data: any) => Promise<any>;
  deleteState: (workspaceSlug: string, stateId: string) => Promise<any>;
  fetchProjectProperty: (workspaceSlug: string, projectId: string) => Promise<any>;
  updateProjectProperty: (workspaceSlug: string, projectId: string, data: any) => Promise<any>;
}

export class CustomProjectStateStore implements ICustomProjectStateStore {
  settings: any | null = null;
  states: any[] | null = null;
  projectProperties: Record<string, any> = {};

  rootStore: CoreRootStore;
  service: CustomProjectStateService;

  constructor(_rootStore: CoreRootStore) {
    makeObservable(this, {
      settings: observable,
      states: observable,
      projectProperties: observable,
      fetchSettings: action,
      updateSettings: action,
      fetchStates: action,
      createState: action,
      updateState: action,
      deleteState: action,
      fetchProjectProperty: action,
      updateProjectProperty: action,
    });

    this.rootStore = _rootStore;
    this.service = new CustomProjectStateService();
  }

  async fetchSettings(workspaceSlug: string) {
    const response = await this.service.getWorkspaceProjectStateSettings(workspaceSlug);
    runInAction(() => {
      this.settings = response;
    });
    return response;
  }

  async updateSettings(workspaceSlug: string, data: any) {
    const response = await this.service.updateWorkspaceProjectStateSettings(workspaceSlug, data);
    runInAction(() => {
      this.settings = response;
    });
    return response;
  }

  async fetchStates(workspaceSlug: string) {
    const response = await this.service.getProjectStates(workspaceSlug);
    runInAction(() => {
      this.states = response;
    });
    return response;
  }

  async createState(workspaceSlug: string, data: any) {
    const response = await this.service.createProjectState(workspaceSlug, data);
    await this.fetchStates(workspaceSlug);
    return response;
  }

  async updateState(workspaceSlug: string, stateId: string, data: any) {
    const response = await this.service.updateProjectState(workspaceSlug, stateId, data);
    await this.fetchStates(workspaceSlug);
    return response;
  }

  async deleteState(workspaceSlug: string, stateId: string) {
    const response = await this.service.deleteProjectState(workspaceSlug, stateId);
    await this.fetchStates(workspaceSlug);
    return response;
  }

  async fetchProjectProperty(workspaceSlug: string, projectId: string) {
    const response = await this.service.getProjectStateProperty(workspaceSlug, projectId);
    runInAction(() => {
      this.projectProperties = {
        ...this.projectProperties,
        [projectId]: response,
      };
    });
    return response;
  }

  async updateProjectProperty(workspaceSlug: string, projectId: string, data: any) {
    const response = await this.service.updateProjectStateProperty(workspaceSlug, projectId, data);
    runInAction(() => {
      this.projectProperties = {
        ...this.projectProperties,
        [projectId]: response,
      };
    });
    return response;
  }
}
