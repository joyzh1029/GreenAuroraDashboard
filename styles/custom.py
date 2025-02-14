def load_css():
    return """
    /* 定义颜色变量 */
    :root {
        --bermuda-50: #eefbf6;
        --bermuda-100: #d5f6e8;
        --bermuda-200: #aeecd5;
        --bermuda-300: #8de1c8;
        --bermuda-400: #43c4a2;
        --bermuda-500: #20a98a;
        --bermuda-600: #128970;
    }
    
    /* 页面背景色 */
    .stApp {
        background-color: var(--bermuda-50);
    }
    
    /* 隐藏Streamlit默认的padding和顶部菜单 */
    .block-container {
        padding: 1rem !important;
    }
    
    /* 隐藏部署菜单 */
    header {
        display: none !important;
    }
    
    /* 移除顶部空白 */
    #root > div:first-child {
        padding-top: 0 !important;
    }

    /* 地图相关样式 */
    .element-container:has(iframe) {
        height: 400px !important;
        width: 500px !important;
        margin: 0 auto !important;
        padding: 0 !important;
        display: block !important;
    }

    /* 控制地图容器的父元素 */
    .element-container:has(iframe) > div {
        height: 400px !important;
        width: 500px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    .stfolium {
        width: 500px !important;
        height: 400px !important;
        margin: 0 !important;
        padding: 0 !important;
        border-radius: 0.5rem;
        overflow: hidden;
        display: block !important;
    }

    .stfolium > iframe {
        width: 500px !important;
        height: 400px !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
    }

    /* 控制地图下方的空白 */
    .element-container:has(iframe) + div {
        display: none !important;
    }

    /* 确保地图容器不会被拉伸 */
    .css-1d391kg {
        width: auto !important;
    }

    /* 自定义metric样式 */
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    
    div[data-testid="metric-container"] > div {
        width: 100%;
    }

    div[data-testid="metric-container"] label {
        color: var(--bermuda-600);
        font-size: 1rem;
    }

    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: var(--bermuda-500);
        font-size: 1.5rem;
    }
    """
