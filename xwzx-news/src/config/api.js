/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // DeepSeek API地址（OpenAI兼容格式）
  apiEndpoint: 'https://api.deepseek.com/chat/completions',

  // API Key 从环境变量读取：在项目根目录新建 .env（参考 .env.example）
  // 切勿把真实密钥写进代码或提交到仓库
  apiKey: import.meta.env.VITE_DEEPSEEK_API_KEY || '',

  // 使用的模型
  model: 'deepseek-chat'
}
