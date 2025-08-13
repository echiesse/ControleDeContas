

export function newDateFromLocalDateStr(dateStr) {
    const date = new Date(dateStr)
    // With the following ajdustment we can assume `dateStr` is at localtime instead of UTC
    const tzOffsetHours = date.getTimezoneOffset() / 60
    date.setHours(date.getHours() + tzOffsetHours)
    return date
}

export function newUTCDateFromStr(dateStr) {
    // dateStr is at UTC
    // The date is created as if we were at UTC but the returned date is represented in localtime
    return new Date(dateStr)
}

export function now() {
    return new Date()
}
