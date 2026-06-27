export const queryKeys = {
    projects: [
        "projects",
    ] as const,

    project: (
        id: string,
    ) =>
        [
            "project",
            id,
        ] as const,

    experiments: [
        "experiments",
    ] as const,

    experiment: (
        id: string,
    ) =>
        [
            "experiment",
            id,
        ] as const,

    molecules: [
        "molecules",
    ] as const,

    molecule: (
        id: string,
    ) =>
        [
            "molecule",
            id,
        ] as const,

    rankings: [
        "rankings",
    ] as const,

    reliability: [
        "reliability",
    ] as const,

    currentUser: [
        "current-user",
    ] as const,
};
