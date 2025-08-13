import {aGetCookie} from '@/support/browser'

class HttpMethod {
    static CONNECT = 'CONNECT'
    static DELETE = 'DELETE'
    static GET = 'GET'
    static HEAD  = 'HEAD '
    static OPTIONS = 'OPTIONS'
    static PATCH = 'PATCH'
    static POST = 'POST'
    static PUT = 'PUT'
    static TRACE = 'TRACE'
}


const SAFE_HTTP_METHODS = [HttpMethod.GET, HttpMethod.HEAD, HttpMethod.OPTIONS, HttpMethod.TRACE]
const UNSAFE_HTTP_METHODS = [HttpMethod.CONNECT, HttpMethod.DELETE, HttpMethod.PATCH, HttpMethod.POST, HttpMethod.PUT]

const HTTP_METHODS = [...SAFE_HTTP_METHODS, ...UNSAFE_HTTP_METHODS]

const DEFAULT_HEADERS = {
    "Accept": "application/json",
}

const isHttpMethod = (method) => HTTP_METHODS.includes(method)
const isUnsafeHttpMethod = (method) => UNSAFE_HTTP_METHODS.includes(method)

async function jsonRequest(url, {method = HttpMethod.GET, data = {}, headers = {}}) {
    if (! isHttpMethod(method)) {
        throw new Error(`Unknown method ${method}`)
    }

    // Build the header:
    if ([HttpMethod.POST, HttpMethod.PUT, HttpMethod.PATCH].includes(method)) {
        headers['Content-Type'] = 'application/json'
    }

    headers = {...DEFAULT_HEADERS, ...headers}

    if (isUnsafeHttpMethod(method)) {
        const csrfToken = await aGetCookie('csrftoken')
        headers['X-CSRFTOKEN'] = csrfToken
    }

    // Build the options object:
    const options = {
        method: method,
        headers: headers,
    }

    if ([HttpMethod.POST, HttpMethod.PUT, HttpMethod.PATCH].includes(method)) {
        options.body = JSON.stringify(data)
    }

    // Send the request
    const response = await fetch(url, options)

    return await response.json()
}


export async function get(url) {
    return await jsonRequest(url)
}


export async function put(url, {data = {}, headers = {}}) {
    return await jsonRequest(url, {data: data, method: HttpMethod.PUT, headers: headers})
}


export async function post(url, {data = {}, headers = {}}) {
    return await jsonRequest(url, {data: data, method: HttpMethod.POST, headers: headers})
}
