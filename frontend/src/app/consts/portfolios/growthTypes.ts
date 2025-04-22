export type GrowthType = "up" | "down" | "middle"

export const growthTypes = new Map<number, GrowthType>()
growthTypes.set(-1, "down")
growthTypes.set(0, "middle")
growthTypes.set(1, "up")
