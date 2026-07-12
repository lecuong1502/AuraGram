export function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function validateUsername(username) {
    return /^[a-z0-9._]{3,30}$/.test(username);
}

export function validatePassword(password) {
    return password.length >= 8;
}