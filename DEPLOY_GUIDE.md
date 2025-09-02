# 🚀 Vercel部署指南

## 📋 一键部署步骤

### 第1步：登录Vercel
1. 打开 https://vercel.com
2. 点击 "Sign Up" 或 "Login"
3. 选择 "Continue with GitHub"
4. 授权Vercel访问你的GitHub

### 第2步：导入项目
1. 在Vercel首页点击 "Add New..." → "Project"
2. 找到 `hazelian0619/wordcloud-tester` 仓库
3. 点击 "Import"

### 第3步：配置部署
**重要**：在部署设置页面，确保：
- ✅ Framework Preset: 选择 "Other" 
- ✅ Build Command: 留空
- ✅ Output Directory: 留空
- ✅ Install Command: `pip install -r requirements.txt`

### 第4步：环境变量（重要！）
在 "Environment Variables" 部分添加：

| 变量名 | 值 |
|--------|-----|
| `OPENAI_API_KEY` | `sk-cFt8t6WmtG5pPI03Qr4j9cVhTHwnzqM8Xmmq89wzgJYhN1bQ` |
| `OPENAI_BASE_URL` | `https://tbnx.plus7.plus/v1` |
| `OPENAI_MODEL` | `deepseek-chat` |

### 第5步：部署！
1. 点击 "Deploy"
2. 等待2-3分钟编译部署
3. 🎉 获得你的网站地址！

## 🌐 部署完成后

你将获得类似这样的网址：
- `https://wordcloud-tester.vercel.app`
- 或者 `https://wordcloud-tester-你的用户名.vercel.app`

## ✅ 功能测试清单

部署完成后，请测试：
- [ ] 页面能正常打开
- [ ] 输入"潮汕菜"能生成词云
- [ ] 点击节点能扩展新概念
- [ ] 聚光灯效果工作正常
- [ ] 导出功能正常

## 🔧 如果遇到问题

### 常见问题1：API调用失败
**现象**：页面显示但词云不生成
**解决**：检查环境变量是否正确设置

### 常见问题2：Python函数报错
**现象**：控制台显示500错误
**解决**：查看Vercel的Function Logs

### 常见问题3：页面无法访问
**现象**：网址打不开
**解决**：检查域名是否正确，等待DNS生效

## 🎯 成功标志

当你看到以下内容，说明部署成功：
1. ✅ 网页正常显示苹果风格界面
2. ✅ 输入词汇能生成词云图
3. ✅ 点击节点有扩展效果
4. ✅ 控制台没有错误信息

## 📱 分享给其他人

部署成功后，你可以：
- 发送网址给朋友：`https://你的域名.vercel.app`
- 发微信群、朋友圈
- 在博客、论坛分享
- 任何人点击都能直接使用！

---

🆘 **需要帮助？** 
如果遇到任何问题，请截图发送给我，我会帮你解决！