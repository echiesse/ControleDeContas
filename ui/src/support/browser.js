

export function getCookies() {
    const kvPairs = document.cookie.split(';')
        .map(s => s.trim())
        .map(item => {
            const [key, value] = item.split('=')
            return {[key]: value}
        })

    const cookies = {}
    for (let pair of kvPairs) {
        for (const k in pair) {
           cookies[k] = pair[k]
        }
    }
    return cookies
}


export function getCookie(name) {
    const cookies = getCookies()
    return cookies[name] || null
}


export async function aGetCookie(name) {
    const cookieObj = await cookieStore.get(name)
    return cookieObj.value
}