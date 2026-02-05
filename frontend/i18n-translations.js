/**
 * 🌐 国际化翻译配置文件
 * 词云测试器 - 中英文翻译表
 */

const i18nTranslations = {
    zh: {
        title: '词云测试器',
        subtitle: '基于语义路径的智能词汇扩展与可视化',

        label: {
            coreWords: '核心词汇',
            newCoreWord: '动态添加',
            nodeCount: '节点数量',
            layoutMode: '布局模式'
        },

        placeholder: {
            coreWords: '潮汕菜',
            newCoreWord: '输入新核心词'
        },

        option: {
            nodeCount: {
                minimal: '精简(10个)',
                moderate: '适中(15个)',
                abundant: '丰富(25个)'
            },
            layoutMode: {
                radial: '径向分布',
                cluster: '聚类分布',
                force: '自由力导向'
            }
        },

        button: {
            generate: '生成词云',
            addNode: '添加节点',
            clearSelection: '清空选择',
            connectionMode: '连线模式',
            exportOutline: '导出大纲',
            exportImage: '导出图谱'
        },

        stats: {
            totalNodes: '总节点数',
            selectedNodes: '已选择',
            coreNodes: '核心词',
            fuzzyNodes: '模糊词'
        },

        tooltip: {
            exportOutline: '导出Markdown大纲',
            exportImage: '导出高清PNG图谱'
        }
    },

    en: {
        title: 'Word Cloud Tester',
        subtitle: 'Intelligent Vocabulary Expansion and Visualization Based on Semantic Paths',

        label: {
            coreWords: 'Core Words',
            newCoreWord: 'Dynamic Add',
            nodeCount: 'Node Count',
            layoutMode: 'Layout Mode'
        },

        placeholder: {
            coreWords: 'Teochew Cuisine',
            newCoreWord: 'Enter new core word'
        },

        option: {
            nodeCount: {
                minimal: 'Minimal (10)',
                moderate: 'Moderate (15)',
                abundant: 'Abundant (25)'
            },
            layoutMode: {
                radial: 'Radial Layout',
                cluster: 'Cluster Layout',
                force: 'Force-Directed'
            }
        },

        button: {
            generate: 'Generate Cloud',
            addNode: 'Add Node',
            clearSelection: 'Clear Selection',
            connectionMode: 'Connection Mode',
            exportOutline: 'Export Outline',
            exportImage: 'Export Graph'
        },

        stats: {
            totalNodes: 'Total Nodes',
            selectedNodes: 'Selected',
            coreNodes: 'Core Words',
            fuzzyNodes: 'Extended Words'
        },

        tooltip: {
            exportOutline: 'Export Markdown Outline',
            exportImage: 'Export High-Resolution PNG Graph'
        }
    }
};
