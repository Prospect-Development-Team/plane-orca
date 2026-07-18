/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { observable, action, computed, makeObservable, runInAction } from "mobx";
import { CustomProjectLabelService } from "@/services/project/custom-project-label.service";
import type { CoreRootStore } from "../root.store";
import { buildTree } from "@plane/utils";

export interface ICustomProjectLabelStore {
  settings: any | null;
  projectProperties: Record<string, any>;
  labels: any[] | null;
  labelsTree: any[];
  projectLabelAssignments: Record<string, any[]>;
  fetchSettings: (workspaceSlug: string) => Promise<any>;
  updateSettings: (workspaceSlug: string, data: any) => Promise<any>;
  fetchProjectProperty: (workspaceSlug: string, projectId: string) => Promise<any>;
  updateProjectLabelProperty: (workspaceSlug: string, projectId: string, data: any) => Promise<any>;
  fetchLabels: (workspaceSlug: string) => Promise<any[]>;
  createLabel: (workspaceSlug: string, data: any) => Promise<any>;
  updateLabel: (workspaceSlug: string, labelId: string, data: any) => Promise<any>;
  deleteLabel: (workspaceSlug: string, labelId: string) => Promise<any>;
  updateLabelPosition: (
    workspaceSlug: string,
    draggingLabelId: string,
    droppedParentId: string | null,
    droppedLabelId: string | undefined,
    dropAtEndOfList: boolean
  ) => Promise<void>;
  fetchProjectLabelAssignments: (workspaceSlug: string, projectId: string) => Promise<any[]>;
  updateProjectLabelAssignments: (workspaceSlug: string, projectId: string, labelIds: string[]) => Promise<any[]>;
}

export class CustomProjectLabelStore implements ICustomProjectLabelStore {
  settings: any | null = null;
  projectProperties: Record<string, any> = {};
  labels: any[] | null = null;
  projectLabelAssignments: Record<string, any[]> = {};

  rootStore: CoreRootStore;
  service: CustomProjectLabelService;

  constructor(_rootStore: CoreRootStore) {
    makeObservable(this, {
      settings: observable,
      projectProperties: observable,
      labels: observable,
      labelsTree: computed,
      projectLabelAssignments: observable,
      fetchSettings: action,
      updateSettings: action,
      fetchProjectProperty: action,
      updateProjectLabelProperty: action,
      fetchLabels: action,
      createLabel: action,
      updateLabel: action,
      deleteLabel: action,
      updateLabelPosition: action,
      fetchProjectLabelAssignments: action,
      updateProjectLabelAssignments: action,
    });

    this.rootStore = _rootStore;
    this.service = new CustomProjectLabelService();
  }

  get labelsTree() {
    if (!this.labels) return [];
    return buildTree(this.labels);
  }

  async fetchSettings(workspaceSlug: string) {
    const response = await this.service.getSettings(workspaceSlug);
    runInAction(() => {
      this.settings = response;
    });
    return response;
  }

  async updateSettings(workspaceSlug: string, data: any) {
    const response = await this.service.updateSettings(workspaceSlug, data);
    runInAction(() => {
      this.settings = response;
    });
    return response;
  }

  async fetchProjectProperty(workspaceSlug: string, projectId: string) {
    const response = await this.service.getProjectProperty(workspaceSlug, projectId);
    runInAction(() => {
      this.projectProperties = {
        ...this.projectProperties,
        [projectId]: response,
      };
    });
    return response;
  }

  async updateProjectLabelProperty(workspaceSlug: string, projectId: string, data: any) {
    const response = await this.service.updateProjectProperty(workspaceSlug, projectId, data);
    runInAction(() => {
      this.projectProperties = {
        ...this.projectProperties,
        [projectId]: response,
      };
    });
    return response;
  }

  async fetchLabels(workspaceSlug: string) {
    const response = await this.service.getProjectLabels(workspaceSlug);
    runInAction(() => {
      this.labels = response.toSorted((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
    });
    return response;
  }

  async createLabel(workspaceSlug: string, data: any) {
    const response = await this.service.createProjectLabel(workspaceSlug, data);
    await this.fetchLabels(workspaceSlug);
    return response;
  }

  async updateLabel(workspaceSlug: string, labelId: string, data: any) {
    const response = await this.service.updateProjectLabel(workspaceSlug, labelId, data);
    await this.fetchLabels(workspaceSlug);
    return response;
  }

  async deleteLabel(workspaceSlug: string, labelId: string) {
    const response = await this.service.deleteProjectLabel(workspaceSlug, labelId);
    await this.fetchLabels(workspaceSlug);
    return response;
  }

  async updateLabelPosition(
    workspaceSlug: string,
    draggingLabelId: string,
    droppedParentId: string | null,
    droppedLabelId: string | undefined,
    dropAtEndOfList: boolean
  ) {
    if (!this.labels) return;
    const currLabel = this.labels.find((l) => l.id === draggingLabelId);
    if (!currLabel) return;

    if (currLabel.parent === droppedParentId && !droppedLabelId) return;

    const data: Partial<any> = { parent: droppedParentId };
    const labelTree = this.labelsTree;

    let currentArray: any[];
    if (!droppedParentId) {
      currentArray = labelTree;
    } else {
      currentArray = labelTree.find((label) => label.id === droppedParentId)?.children || [];
    }

    let droppedLabelIndex = currentArray.findIndex((label) => label.id === droppedLabelId);
    if (dropAtEndOfList || droppedLabelIndex === -1) {
      droppedLabelIndex = currentArray.length;
    }

    if (currentArray.length > 0) {
      let prevSortOrder: number | undefined;
      let nextSortOrder: number | undefined;

      if (typeof currentArray[droppedLabelIndex - 1] !== "undefined") {
        prevSortOrder = currentArray[droppedLabelIndex - 1].sort_order;
      }
      if (typeof currentArray[droppedLabelIndex] !== "undefined") {
        nextSortOrder = currentArray[droppedLabelIndex].sort_order;
      }

      let sortOrder = 65535;
      if (prevSortOrder !== undefined && nextSortOrder !== undefined) {
        sortOrder = (prevSortOrder + nextSortOrder) / 2;
      } else if (nextSortOrder !== undefined) {
        sortOrder = nextSortOrder / 2;
      } else if (prevSortOrder !== undefined) {
        sortOrder = prevSortOrder + 10000;
      }
      data.sort_order = sortOrder;
    }

    await this.updateLabel(workspaceSlug, draggingLabelId, data);
  }

  async fetchProjectLabelAssignments(workspaceSlug: string, projectId: string) {
    const response = await this.service.getProjectLabelAssignments(workspaceSlug, projectId);
    runInAction(() => {
      this.projectLabelAssignments = {
        ...this.projectLabelAssignments,
        [projectId]: response,
      };
    });
    return response;
  }

  async updateProjectLabelAssignments(workspaceSlug: string, projectId: string, labelIds: string[]) {
    const response = await this.service.updateProjectLabelAssignments(workspaceSlug, projectId, labelIds);
    runInAction(() => {
      this.projectLabelAssignments = {
        ...this.projectLabelAssignments,
        [projectId]: response,
      };
    });
    return response;
  }
}
