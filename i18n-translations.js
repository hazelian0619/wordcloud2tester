/**
 * 🌐 国际化翻译配置文件
 * 词云测试器 - 中英文翻译表
 *
 * 使用说明：
 * 1. 所有需要翻译的文本都在这里集中管理
 * 2. key采用语义化命名，便于维护
 * 3. 支持动态参数插值 {0}, {1} 等
 */

const translations = {
    // ========== 中文翻译 ==========
    zh: {
        // 页面标题和描述
        page_title: '词云测试器',
        page_subtitle: '基于语义路径的智能词汇扩展与可视化',

        // 控制面板 - 标签
        label_core_words: '核心词汇',
        label_dynamic_add: '动态添加',
        label_node_count: '节点数量',
        label_layout_mode: '布局模式',

        // 控制面板 - 占位符
        placeholder_core_word: '潮汕菜',
        placeholder_new_core_word: '输入新核心词',

        // 控制面板 - 下拉选项
        option_simple: '精简(10个)',
        option_moderate: '适中(15个)',
        option_rich: '丰富(25个)',

        option_radial: '径向分布',
        option_cluster: '聚类分布',
        option_force: '自由力导向',

        // 按钮
        btn_generate: '生成词云',
        btn_add_node: '添加节点',
        btn_clear_selection: '清空选择',
        btn_connection_mode: '连线模式',
        btn_connection_mode_active: '退出连线',
        btn_export_outline: '导出大纲',
        btn_export_image: '导出图谱',

        // 统计标签
        stat_total_nodes: '总节点数',
        stat_selected: '已选择',
        stat_core_words: '核心词',
        stat_fuzzy_words: '模糊词',

        // 已选择词汇区域
        title_selected_words: '已选择的词汇',

        // 交互提示
        title_interaction_tips: '交互提示：',
        tip_click_node: '<strong>单击节点</strong>：选择/取消选择词汇',
        tip_double_click: '<strong>双击节点</strong>或<strong>点击+号</strong>：扩展相关词汇',
        tip_connection_mode: '<strong>连线模式</strong>：先点击"连线模式"，然后依次点击两个节点建立关系连线',
        tip_click_link: '<strong>单击连线</strong>：选择/取消选择连线',
        tip_semantic_link: '<strong>语义连线</strong>：浅虚线表示AI建议关系，点击+号扩展后变为实线表示确认路径',
        tip_graph_operations: '<strong>图谱操作</strong>：鼠标拖拽平移、滚轮缩放、双击重置视图',

        // 调试面板
        title_core_nodes: '当前核心词节点',
        title_debug_info: '调试信息',
        msg_waiting_core_word: '等待添加核心词...',
        msg_waiting_generate: '等待生成词云...',

        // 动态消息 - 调试信息
        debug_ready: '🚀 模糊词云测试器已就绪，请输入核心词后点击生成',
        debug_start_generate: '🔄 开始生成词云数据...',
        debug_generation_complete: '✅ 初始词云生成完成！核心词: {0}个, 模糊词: {1}个',
        debug_view_reset: '🔄 视图已重置到初始位置和缩放级别',
        debug_layout_stable: '🎯 布局已稳定，节点已停止移动，可以开始点击交互',
        debug_force_stop: '⏰ 强制停止布局动画，节点现已完全固定',
        debug_start_drag: '🖱️ 开始拖拽节点: {0}',

        debug_expand_start: '🔄 开始扩展节点: {0} (类型: {1})...',
        debug_concepts_generated: '📊 Graphiti真实生成 {0} 个概念',
        debug_no_concepts: '❌ Graphiti API没有为此词汇生成概念: {0}',
        debug_expand_success: '✅ 成功扩展节点 {0}，添加 {1} 个新概念',
        debug_expand_failed: '❌ 扩展节点失败: {0}',

        debug_add_root_success: '✅ 成功添加新根节点: {0}',
        debug_clear_selection: '🗑️ 已清空所有选择（包括节点和连线）',

        debug_connection_mode_on: '🔗 已进入连线模式，点击两个节点建立连线',
        debug_connection_mode_off: '🔗 已退出连线模式',
        debug_select_start_node: '🔗 已选择起始节点: {0}，请点击目标节点建立连线',
        debug_connection_created: '🔗 已建立连线: {0} → {1}',
        debug_connection_exists: '⚠️ 该连线已存在',

        debug_export_outline: '✅ 大纲已导出为 Markdown 文件',
        debug_export_image: '✅ 高清图谱已导出为 PNG 文件',

        // 错误和警告消息
        error_no_wordcloud: '请先生成词云！',
        error_generation_failed: '❌ 词云生成失败: {0}',
        error_no_core_word: '请先输入核心词汇',
        error_expansion_path_warning: '⚠️ 路径验证失败: {0} 的根节点"{1}"不是核心词',

        // API相关消息
        api_calling: '🚀 调用API生成概念: {0}',
        api_success: '✅ 成功生成 {0} 个概念',
        api_failed: '❌ API调用失败: {0}',

        // 节点路径相关
        path_confirmed: 'ℹ️ 节点 {0} 没有需要确认的入链路径',

        // 导出相关
        export_outline_title: '导出Markdown大纲',
        export_image_title: '导出高清PNG图谱'
    },

    // ========== 英文翻译 ==========
    en: {
        // Page title and description
        page_title: 'Word Cloud Tester',
        page_subtitle: 'Intelligent Vocabulary Expansion and Visualization Based on Semantic Paths',

        // Control panel - Labels
        label_core_words: 'Core Words',
        label_dynamic_add: 'Dynamic Add',
        label_node_count: 'Node Count',
        label_layout_mode: 'Layout Mode',

        // Control panel - Placeholders
        placeholder_core_word: 'Teochew Cuisine',
        placeholder_new_core_word: 'Enter new core word',

        // Control panel - Select options
        option_simple: 'Simple (10)',
        option_moderate: 'Moderate (15)',
        option_rich: 'Rich (25)',

        option_radial: 'Radial Layout',
        option_cluster: 'Cluster Layout',
        option_force: 'Force-Directed',

        // Buttons
        btn_generate: 'Generate',
        btn_add_node: 'Add Node',
        btn_clear_selection: 'Clear',
        btn_connection_mode: 'Connect',
        btn_connection_mode_active: 'Exit Connect',
        btn_export_outline: 'Export Outline',
        btn_export_image: 'Export Graph',

        // Statistics labels
        stat_total_nodes: 'Total Nodes',
        stat_selected: 'Selected',
        stat_core_words: 'Core',
        stat_fuzzy_words: 'Extended',

        // Selected words section
        title_selected_words: 'Selected Words',

        // Interaction tips
        title_interaction_tips: 'Interaction Guide:',
        tip_click_node: '<strong>Click node</strong>: Select/deselect word',
        tip_double_click: '<strong>Double-click node</strong> or <strong>click + button</strong>: Expand related words',
        tip_connection_mode: '<strong>Connection mode</strong>: Click "Connect" button, then click two nodes to create a link',
        tip_click_link: '<strong>Click link</strong>: Select/deselect connection',
        tip_semantic_link: '<strong>Semantic links</strong>: Dashed lines show AI suggestions, solid lines show confirmed paths',
        tip_graph_operations: '<strong>Graph operations</strong>: Drag to pan, scroll to zoom, double-click to reset view',

        // Debug panel
        title_core_nodes: 'Current Core Nodes',
        title_debug_info: 'Debug Info',
        msg_waiting_core_word: 'Waiting for core words...',
        msg_waiting_generate: 'Waiting to generate word cloud...',

        // Dynamic messages - Debug info
        debug_ready: '🚀 Word cloud tester ready. Please enter core words and click generate',
        debug_start_generate: '🔄 Starting word cloud generation...',
        debug_generation_complete: '✅ Initial word cloud generated! Core words: {0}, Extended words: {1}',
        debug_view_reset: '🔄 View reset to initial position and zoom level',
        debug_layout_stable: '🎯 Layout stabilized, nodes stopped moving, ready for interaction',
        debug_force_stop: '⏰ Force stopped layout animation, nodes are now fixed',
        debug_start_drag: '🖱️ Started dragging node: {0}',

        debug_expand_start: '🔄 Expanding node: {0} (type: {1})...',
        debug_concepts_generated: '📊 Generated {0} real concepts via Graphiti',
        debug_no_concepts: '❌ Graphiti API generated no concepts for: {0}',
        debug_expand_success: '✅ Successfully expanded node {0}, added {1} new concepts',
        debug_expand_failed: '❌ Failed to expand node: {0}',

        debug_add_root_success: '✅ Successfully added new root node: {0}',
        debug_clear_selection: '🗑️ Cleared all selections (nodes and links)',

        debug_connection_mode_on: '🔗 Entered connection mode, click two nodes to create link',
        debug_connection_mode_off: '🔗 Exited connection mode',
        debug_select_start_node: '🔗 Selected start node: {0}, click target node to create link',
        debug_connection_created: '🔗 Created link: {0} → {1}',
        debug_connection_exists: '⚠️ This link already exists',

        debug_export_outline: '✅ Outline exported as Markdown file',
        debug_export_image: '✅ High-resolution graph exported as PNG file',

        // Error and warning messages
        error_no_wordcloud: 'Please generate word cloud first!',
        error_generation_failed: '❌ Word cloud generation failed: {0}',
        error_no_core_word: 'Please enter core words first',
        error_expansion_path_warning: '⚠️ Path validation failed: root node "{1}" of {0} is not a core word',

        // API related messages
        api_calling: '🚀 Calling API to generate concepts: {0}',
        api_success: '✅ Successfully generated {0} concepts',
        api_failed: '❌ API call failed: {0}',

        // Node path related
        path_confirmed: 'ℹ️ Node {0} has no incoming paths to confirm',

        // Export related
        export_outline_title: 'Export Markdown Outline',
        export_image_title: 'Export High-Resolution Graph'
    }
};

/**
 * 🌐 翻译函数
 * @param {string} key - 翻译键
 * @param {...any} args - 动态参数，用于替换 {0}, {1} 等占位符
 * @returns {string} 翻译后的文本
 */
function t(key, ...args) {
    const currentLang = window.currentLanguage || 'zh';
    let text = translations[currentLang][key] || translations['zh'][key] || key;

    // 替换动态参数 {0}, {1}, {2}...
    args.forEach((arg, index) => {
        text = text.replace(new RegExp(`\\{${index}\\}`, 'g'), arg);
    });

    return text;
}

/**
 * 🔄 切换语言
 * @param {string} lang - 语言代码 ('zh' 或 'en')
 */
function switchLanguage(lang) {
    if (!translations[lang]) {
        console.warn(`Language '${lang}' not supported, falling back to 'zh'`);
        lang = 'zh';
    }

    window.currentLanguage = lang;
    localStorage.setItem('preferred_language', lang);

    // 更新所有UI文本
    updateAllUIText();

    // 更新语言切换按钮状态
    updateLanguageSwitcherUI(lang);

    console.log(`🌐 Language switched to: ${lang === 'zh' ? '中文' : 'English'}`);
}

/**
 * 🎨 更新语言切换按钮UI状态
 */
function updateLanguageSwitcherUI(lang) {
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.lang-btn[data-lang="${lang}"]`)?.classList.add('active');
}

/**
 * 📝 更新所有UI文本
 * 这个函数会在语言切换时被调用，更新页面上所有需要翻译的元素
 */
function updateAllUIText() {
    // 使用 data-i18n 属性标记的元素
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = t(key);

        // 根据元素类型更新不同属性
        if (el.tagName === 'INPUT' && el.hasAttribute('placeholder')) {
            el.placeholder = translation;
        } else if (el.hasAttribute('title')) {
            el.title = translation;
        } else {
            el.innerHTML = translation;
        }
    });

    // 更新页面标题
    document.title = t('page_title');
}

/**
 * 🚀 初始化国际化系统
 * 在页面加载时调用，从localStorage恢复用户的语言偏好
 */
function initializeI18n() {
    const savedLang = localStorage.getItem('preferred_language') || 'zh';
    window.currentLanguage = savedLang;

    // 延迟更新UI，确保DOM已加载
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            updateAllUIText();
            updateLanguageSwitcherUI(savedLang);
        });
    } else {
        updateAllUIText();
        updateLanguageSwitcherUI(savedLang);
    }
}

// 自动初始化
initializeI18n();
