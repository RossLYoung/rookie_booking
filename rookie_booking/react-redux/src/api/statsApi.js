



export function fetchAllResults(url) {
    return fetch(url, {
        method     : 'GET',
        credentials: 'include' // include sessionid cookie
    }).then((response) => {
        if (!response.ok) {
            const error = new Error(response.statusText);
            error.response = response;
            throw error;
        }
        return response.json();
    });
}
