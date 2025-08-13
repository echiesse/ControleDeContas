

export function formatUTCDateToSend(d) {
    const year = `${d.getUTCFullYear()}`
    const month = `${d.getUTCMonth() + 1}`.padStart(2, '0')
    const day = `${d.getUTCDate()}`.padStart(2, '0')
    return `${year}-${month}-${day}`
}

export function formatDateToSend(d) {
    const year = `${d.getFullYear()}`
    const month = `${d.getMonth() + 1}`.padStart(2, '0')
    const day = `${d.getDate()}`.padStart(2, '0')
    return `${year}-${month}-${day}`
}
