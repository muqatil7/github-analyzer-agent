# GitHub Analyzer Agent 🤖

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.45%2B-green)
![LangChain](https://img.shields.io/badge/LangChain-0.3.7%2B-orange)
![LangSmith](https://img.shields.io/badge/LangSmith-0.1.147%2B-purple)
![MCP](https://img.shields.io/badge/MCP-1.1.0%2B-red)
![License](https://img.shields.io/badge/license-MIT-blue)

مشروع وكيل ذكي متقدم مبني باستخدام **LangGraph** + **LangChain** + **LangSmith** لتحليل مستودعات GitHub باستخدام تقنية **Model Context Protocol (MCP)**.

## ✨ المميزات الرئيسية

- 🔍 **تحليل ذكي شامل**: تحليل مستودعات GitHub لعدة أغراض (الأمان، الملخصات، المراجعات)
- 🔄 **إدارة السياق التلقائية**: تلخيص ذكي للسياق عند اقتراب حد الـ 200k token
- 📊 **مراقبة متقدمة**: تتبع شامل للعمليات باستخدام LangSmith
- 🛠️ **معمارية قابلة للتوسع**: تصميم مرن يدعم إضافة ميزات جديدة بسهولة
- ⚡ **أداء محسّن**: استخدام فعال لموارد النظام ومعالجة غير متزامنة
- 🔐 **أمان عالي**: إدارة آمنة للمفاتيح والرموز المميزة

## 🚀 التثبيت والإعداد

### المتطلبات المسبقة

- Python 3.9 أو أحدث
- حساب OpenAI مع API key
- حساب LangSmith للمراقبة
- GitHub Personal Access Token

### خطوات التثبيت

```bash
# 1. استنساخ المستودع
git clone https://github.com/muqatil7/github-analyzer-agent.git
cd github-analyzer-agent

# 2. إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# 3. تثبيت التبعيات
pip install -r requirements.txt

# 4. نسخ ملف المتغيرات البيئية وتحريره
cp .env.example .env
# قم بتحرير .env وأضف مفاتيح API الخاصة بك

# 5. تثبيت المشروع
pip install -e .
```

## 📖 الاستخدام

### الاستخدام الأساسي

```python
from src.main import GitHubAnalyzerAgent

# إنشاء الوكيل
agent = GitHubAnalyzerAgent()

# تحليل مستودع GitHub
result = await agent.analyze_repository(
    repo_url="https://github.com/user/repo",
    analysis_type="security",  # أو "summary" أو "custom"
    custom_prompt="ابحث عن نقاط الضعف الأمنية في هذا المشروع"
)

print(result)
```

## 📁 هيكل المشروع

```
github-analyzer-agent/
├── src/
│   ├── main.py                 # النقطة الرئيسية للتطبيق
│   ├── agent/
│   │   ├── github_agent.py     # LangGraph Agent الرئيسي
│   │   ├── state.py           # إدارة حالة الوكيل
│   │   └── tools.py           # أدوات مساعدة
│   ├── mcp/
│   │   ├── client.py          # عميل MCP للـ GitHub
│   │   └── config.py          # إعدادات MCP
│   ├── services/
│   │   ├── context_manager.py  # إدارة السياق والتلخيص
│   │   ├── langsmith_tracer.py # تتبع LangSmith
│   │   └── openai_service.py   # خدمة OpenAI
│   └── utils/
│       ├── logger.py          # نظام السجلات
│       └── validators.py      # التحقق من المدخلات
├── tests/                     # الاختبارات
├── examples/                  # أمثلة للاستخدام
└── docs/                      # الوثائق
```

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. Fork المستودع
2. إنشاء branch جديد للميزة (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى Branch (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

<div align="center">
  <strong>مصنوع بـ ❤️ باستخدام LangGraph + LangChain + LangSmith</strong>
</div>