export const findParentById = (target: HTMLElement, idList: string[]) => {
  while (target.parentElement) {
    if (idList.includes(target.id)) {
      return target
    }

    target = target.parentElement
  }

  return null
}
