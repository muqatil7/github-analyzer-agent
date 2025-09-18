#!/usr/bin/env python3
"""
Agent State Management for GitHub Analysis
إدارة حالة الوكيل لتحليل GitHub
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Union
from typing_extensions import TypedDict, NotRequired
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field


class AnalysisType(str, Enum):
    """أنواع التحليل المدعومة."""
    SUMMARY = "summary"      # ملخص شامل للمستودع
    SECURITY = "security"    # تحليل أمني للكود
    CUSTOM = "custom"        # تحليل مخصص حسب الطلب


class AnalysisStatus(str, Enum):
    """حالات تنفيذ التحليل."""
    PENDING = "pending"          # في انتظار البدء
    FETCHING_REPO = "fetching"   # جلب بيانات المستودع
    ANALYZING = "analyzing"      # جاري التحليل
    COMPLETED = "completed"      # تم الإنجاز
    FAILED = "failed"            # فشل في التنفيذ


class RepositoryInfo(BaseModel):
    """معلومات مستودع GitHub."""
    url: str = Field(description="رابط المستودع")
    owner: str = Field(description="مالك المستودع")
    name: str = Field(description="اسم المستودع")
    description: Optional[str] = Field(None, description="وصف المستودع")
    language: Optional[str] = Field(None, description="اللغة الرئيسية")
    languages: Dict[str, int] = Field(default_factory=dict, description="اللغات المستخدمة")
    stars: int = Field(0, description="عدد النجوم")
    forks: int = Field(0, description="عدد التفرعات")
    size: int = Field(0, description="حجم المستودع")
    default_branch: str = Field("main", description="الفرع الافتراضي")
    files_analyzed: List[str] = Field(default_factory=list, description="قائمة الملفات المحللة")
    security_files: List[str] = Field(default_factory=list, description="ملفات الأمان")
    readme_content: Optional[str] = Field(None, description="محتوى README")


class ContextInfo(BaseModel):
    """معلومات سياق المحادثة."""
    current_tokens: int = Field(0, description="عدد الرموز الحالي")
    max_tokens: int = Field(200000, description="الحد الأقصى للرموز")
    summary_count: int = Field(0, description="عدد مرات التلخيص")
    last_summary: Optional[str] = Field(None, description="آخر تلخيص")
    preserved_messages: int = Field(5, description="عدد الرسائل المحفوظة")


class AnalysisResult(BaseModel):
    """نتائج التحليل."""
    analysis_type: AnalysisType = Field(description="نوع التحليل")
    status: AnalysisStatus = Field(description="حالة التحليل")
    summary: Optional[str] = Field(None, description="ملخص النتائج")
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="النتائج التفصيلية")
    recommendations: List[str] = Field(default_factory=list, description="التوصيات")
    confidence_score: float = Field(0.0, description="معدل الثقة في النتائج")
    processing_time: float = Field(0.0, description="وقت المعالجة")
    error_message: Optional[str] = Field(None, description="رسالة خطأ إن وجدت")


class AgentState(TypedDict):
    """
    حالة الوكيل الرئيسي للـ LangGraph.
    تحتوي على جميع البيانات اللازمة لتتبع عملية التحليل.
    """
    # الرسائل والمحادثة
    messages: List[BaseMessage]
    
    # معلومات المستودع
    repository: NotRequired[RepositoryInfo]
    
    # معاملات التحليل
    analysis_type: NotRequired[AnalysisType]
    custom_prompt: NotRequired[Optional[str]]
    
    # حالة التنفيذ
    status: NotRequired[AnalysisStatus]
    current_step: NotRequired[str]
    
    # إدارة السياق
    context: NotRequired[ContextInfo]
    
    # نتائج التحليل
    result: NotRequired[AnalysisResult]
    
    # بيانات إضافية وميتاداتا
    metadata: NotRequired[Dict[str, Any]]
    
    # معلومات التتبع
    trace_id: NotRequired[str]
    session_id: NotRequired[str]


class InputState(TypedDict):
    """مخطط الدخل للوكيل."""
    repo_url: str
    analysis_type: str  # "summary", "security", "custom"
    custom_prompt: NotRequired[Optional[str]]


class OutputState(TypedDict):
    """مخطط الخرج للوكيل."""
    analysis_result: AnalysisResult
    repository_info: RepositoryInfo
    context_summary: Dict[str, Any]


# ثوابت للنظام
CONSTANTS = {
    "MAX_CONTEXT_TOKENS": 200000,
    "PRESERVED_MESSAGES": 5,
    "DEFAULT_MODEL": "gpt-4o-mini",
    "CONTEXT_SUMMARY_TRIGGER": 0.85,  # 85% من الحد الأقصى
    "ANALYSIS_TIMEOUT": 300,  # 5 دقائق
    "MAX_FILE_SIZE": 100000,  # 100KB
    "MAX_FILES_TO_ANALYZE": 50,
}

# قوالب التحليل المعرفة مسبقاً
ANALYSIS_PROMPTS = {
    AnalysisType.SUMMARY: """
    تحليل شامل لمستودع GitHub:
    1. ملخص عام عن المشروع
    2. التقنيات واللغات المستخدمة
    3. هيكل المشروع والملفات الرئيسية
    4. الميزات والوظائف الرئيسية
    5. طريقة التثبيت والاستخدام
    6. جودة الكود والتوثيق
    """,
    
    AnalysisType.SECURITY: """
    تحليل أمني شامل لمستودع GitHub:
    1. فحص نقاط الضعف الأمنية المحتملة
    2. مراجعة إدارة التبعيات والمكتبات
    3. تقييم ممارسات الأمان في الكود
    4. فحص إعدادات الأمان والتشفير
    5. مراجعة أذونات الدخول والمصادقة
    6. تقييم مستوى المخاطر واقتراح الحلول
    """,
}

# أنماط الملفات المهمة للأمان
SECURITY_FILE_PATTERNS = [
    "requirements.txt",
    "package.json",
    "package-lock.json",
    "Pipfile",
    "Pipfile.lock",
    "composer.json",
    "pom.xml",
    "go.mod",
    "Cargo.toml",
    "yarn.lock",
    ".*secrets*",
    ".*config*",
    ".*env*",
    ".docker*",
    "*.key",
    "*.pem",
    "*.cert",
    "auth*",
    "login*",
]

# أنماط الملفات المهمة للتحليل
IMPORTANT_FILE_PATTERNS = [
    "README*",
    "CHANGELOG*",
    "LICENSE*",
    "CONTRIBUTING*",
    "SECURITY*",
    "setup.py",
    "main.*",
    "index.*",
    "app.*",
    "server.*",
    "client.*",
]


def create_initial_state(
    repo_url: str,
    analysis_type: AnalysisType,
    custom_prompt: Optional[str] = None,
    session_id: Optional[str] = None
) -> AgentState:
    """إنشاء حالة أولية للوكيل."""
    import uuid
    from datetime import datetime
    
    return AgentState(
        messages=[
            HumanMessage(content=f"مرحباً! أريد تحليل مستودع GitHub: {repo_url}")
        ],
        analysis_type=analysis_type,
        custom_prompt=custom_prompt,
        status=AnalysisStatus.PENDING,
        current_step="initialization",
        context=ContextInfo(),
        metadata={
            "created_at": datetime.now().isoformat(),
            "repo_url": repo_url,
            "version": "1.0.0"
        },
        trace_id=str(uuid.uuid4()),
        session_id=session_id or str(uuid.uuid4())
    )


def update_state_status(state: AgentState, new_status: AnalysisStatus, step: str = "") -> AgentState:
    """تحديث حالة الوكيل."""
    state["status"] = new_status
    if step:
        state["current_step"] = step
    return state