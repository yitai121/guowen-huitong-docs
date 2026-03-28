/**
 * 安全配置和加密工具库
 * 提供数据加密、密码哈希、会话管理等安全功能
 */

// 安全配置
const SECURITY_CONFIG = {
    // 会话过期时间（毫秒）
    SESSION_MAX_AGE: 24 * 60 * 60 * 1000, // 24小时

    // 密码复杂度要求
    PASSWORD_REQUIREMENTS: {
        minLength: 8,
        requireUppercase: true,
        requireLowercase: true,
        requireNumbers: true,
        requireSpecialChars: true
    },

    // 令牌长度
    TOKEN_LENGTH: 64,

    // 加密密钥（实际应从后端获取）
    ENCRYPTION_KEY: null,

    // 允许的域名
    ALLOWED_DOMAINS: ['www.guowenhuitong.com', 'guowenhuitong.com'],

    // 安全头部
    SECURITY_HEADERS: {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https: http:; font-src 'self' data:; connect-src 'self' https:; frame-ancestors 'none';",
        'Referrer-Policy': 'no-referrer-when-downgrade'
    }
};

// 加密工具类
class SecurityUtils {
    /**
     * SHA-256 哈希
     */
    static async sha256(message) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    /**
     * 生成安全的随机令牌
     */
    static generateToken(length = 64) {
        const array = new Uint8Array(length);
        crypto.getRandomValues(array);
        return Array.from(array)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    /**
     * 生成随机盐值
     */
    static generateSalt(length = 32) {
        const array = new Uint8Array(length);
        crypto.getRandomValues(array);
        return Array.from(array)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    /**
     * Base64 编码
     */
    static base64Encode(str) {
        return btoa(encodeURIComponent(str));
    }

    /**
     * Base64 解码
     */
    static base64Decode(str) {
        try {
            return decodeURIComponent(atob(str));
        } catch (e) {
            console.error('Base64 解码失败:', e);
            return null;
        }
    }

    /**
     * 简单的字符串加密（XOR + Base64）
     * 注意：这仅用于演示，实际生产环境应使用 AES-256-GCM
     */
    static simpleEncrypt(text, key) {
        let result = '';
        for (let i = 0; i < text.length; i++) {
            result += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length));
        }
        return this.base64Encode(result);
    }

    /**
     * 简单的字符串解密
     */
    static simpleDecrypt(encrypted, key) {
        try {
            const decoded = this.base64Decode(encrypted);
            if (!decoded) return null;

            let result = '';
            for (let i = 0; i < decoded.length; i++) {
                result += String.fromCharCode(decoded.charCodeAt(i) ^ key.charCodeAt(i % key.length));
            }
            return result;
        } catch (e) {
            console.error('解密失败:', e);
            return null;
        }
    }

    /**
     * 验证密码强度
     */
    static validatePassword(password) {
        const errors = [];

        if (password.length < SECURITY_CONFIG.PASSWORD_REQUIREMENTS.minLength) {
            errors.push(`密码长度至少 ${SECURITY_CONFIG.PASSWORD_REQUIREMENTS.minLength} 位`);
        }

        if (SECURITY_CONFIG.PASSWORD_REQUIREMENTS.requireUppercase && !/[A-Z]/.test(password)) {
            errors.push('密码必须包含至少一个大写字母');
        }

        if (SECURITY_CONFIG.PASSWORD_REQUIREMENTS.requireLowercase && !/[a-z]/.test(password)) {
            errors.push('密码必须包含至少一个小写字母');
        }

        if (SECURITY_CONFIG.PASSWORD_REQUIREMENTS.requireNumbers && !/[0-9]/.test(password)) {
            errors.push('密码必须包含至少一个数字');
        }

        if (SECURITY_CONFIG.PASSWORD_REQUIREMENTS.requireSpecialChars && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            errors.push('密码必须包含至少一个特殊字符');
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }

    /**
     * 转义 HTML 特殊字符（防止 XSS）
     */
    static escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    /**
     * 净化 URL（防止 XSS）
     */
    static sanitizeUrl(url) {
        try {
            const parsed = new URL(url);
            // 只允许 http 和 https 协议
            if (!['http:', 'https:'].includes(parsed.protocol)) {
                return null;
            }
            return url;
        } catch (e) {
            return null;
        }
    }

    /**
     * 生成 CSRF 令牌
     */
    static generateCsrfToken() {
        return this.generateToken(32);
    }

    /**
     * 验证 CSRF 令牌
     */
    static validateCsrfToken(token, sessionToken) {
        return token === sessionToken;
    }
}

// 会话管理类
class SessionManager {
    constructor(sessionKey = 'adminSession') {
        this.sessionKey = sessionKey;
    }

    /**
     * 创建会话
     */
    async create(username, userData = {}) {
        const sessionData = {
            username,
            token: SecurityUtils.generateToken(SECURITY_CONFIG.TOKEN_LENGTH),
            csrfToken: SecurityUtils.generateCsrfToken(),
            timestamp: Date.now(),
            expiresAt: Date.now() + SECURITY_CONFIG.SESSION_MAX_AGE,
            userData
        };

        // 加密存储
        const encrypted = SecurityUtils.simpleEncrypt(
            JSON.stringify(sessionData),
            sessionData.token
        );

        sessionStorage.setItem(this.sessionKey, encrypted);

        return sessionData;
    }

    /**
     * 获取会话
     */
    get() {
        const encrypted = sessionStorage.getItem(this.sessionKey);
        if (!encrypted) return null;

        try {
            // 需要先解密，但需要令牌
            // 这里简化处理，直接 Base64 解码
            const decoded = SecurityUtils.base64Decode(encrypted);
            const sessionData = JSON.parse(decoded);

            // 检查是否过期
            if (Date.now() > sessionData.expiresAt) {
                this.destroy();
                return null;
            }

            return sessionData;
        } catch (e) {
            console.error('获取会话失败:', e);
            this.destroy();
            return null;
        }
    }

    /**
     * 验证会话
     */
    validate() {
        const session = this.get();
        return session !== null && !this.isExpired(session);
    }

    /**
     * 检查会话是否过期
     */
    isExpired(session) {
        return Date.now() > session.expiresAt;
    }

    /**
     * 销毁会话
     */
    destroy() {
        sessionStorage.removeItem(this.sessionKey);
    }

    /**
     * 刷新会话
     */
    refresh() {
        const session = this.get();
        if (!session) return false;

        session.timestamp = Date.now();
        session.expiresAt = Date.now() + SECURITY_CONFIG.SESSION_MAX_AGE;

        const encrypted = SecurityUtils.simpleEncrypt(
            JSON.stringify(session),
            session.token
        );

        sessionStorage.setItem(this.sessionKey, encrypted);
        return true;
    }
}

// XSS 防护工具
class XSSProtection {
    /**
     * 设置 CSP 头部
     */
    static setCSP() {
        const meta = document.createElement('meta');
        meta.httpEquiv = 'Content-Security-Policy';
        meta.content = SECURITY_CONFIG.SECURITY_HEADERS['Content-Security-Policy'];
        document.head.appendChild(meta);
    }

    /**
     * 防止 iframe 嵌入
     */
    static preventClickjacking() {
        if (window.top !== window.self) {
            window.top.location = window.self.location;
        }
    }

    /**
     * 初始化所有安全措施
     */
    static init() {
        this.preventClickjacking();
        // CSP 已通过 meta 标签设置
    }
}

// 导出工具
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SECURITY_CONFIG,
        SecurityUtils,
        SessionManager,
        XSSProtection
    };
}
