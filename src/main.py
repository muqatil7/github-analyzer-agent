#!/usr/bin/env python3
"""
GitHub Analyzer Agent - Main Entry Point
مشروع وكيل ذكي لتحليل مستودعات GitHub باستخدام LangGraph + LangChain + LangSmith
"""

import asyncio
import logging
import os
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from langsmith import traceable

from .agent import GitHubAgent, AnalysisType
from .services import ContextManager, LangSmithTracer
from .utils import setup_logger, validate_github_url

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد نظام السجلات
logger = setup_logger(__name__)


class GitHubAnalyzerAgent:
    """
    الوكيل الرئيسي لتحليل مستودعات GitHub.
    يدمج LangGraph + LangChain + LangSmith + MCP لتحليل شامل.
    """
    
    def __init__(self):
        """تهيئة الوكيل مع كل الخدمات المطلوبة."""
        self.agent: Optional[GitHubAgent] = None
        self.context_manager: Optional[ContextManager] = None
        self.tracer: Optional[LangSmithTracer] = None
        self._initialized = False
        
        logger.info("تم إنشاء GitHubAnalyzerAgent")
    
    async def initialize(self) -> None:
        """تهيئة كل المكونات المطلوبة للوكيل."""
        if self._initialized:
            return
            
        try:
            logger.info("بدء تهيئة مكونات الوكيل...")
            
            # التحقق من المتغيرات البيئية المطلوبة
            self._validate_environment()
            
            # تهيئة مدير السياق
            self.context_manager = ContextManager(
                max_tokens=200000,  # 200k tokens limit
                model_name="gpt-4o-mini"
            )
            
            # تهيئة تتبع LangSmith
            self.tracer = LangSmithTracer()
            await self.tracer.initialize()
            
            # تهيئة الوكيل الرئيسي
            self.agent = GitHubAgent(
                context_manager=self.context_manager,
                tracer=self.tracer
            )
            await self.agent.initialize()
            
            self._initialized = True
            logger.info("تم تهيئة جميع مكونات الوكيل بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تهيئة الوكيل: {e}")
            raise
    
    def _validate_environment(self) -> None:
        """التحقق من وجود المتغيرات البيئية المطلوبة."""
        required_vars = [
            "OPENAI_API_KEY",
            "LANGSMITH_API_KEY", 
            "GITHUB_PERSONAL_ACCESS_TOKEN"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"المتغيرات البيئية المطلوبة مفقودة: {', '.join(missing_vars)}"
            )
    
    @traceable(name="analyze_repository")
    async def analyze_repository(
        self,
        repo_url: str,
        analysis_type: str = "summary",
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        تحليل مستودع GitHub.
        
        Args:
            repo_url: رابط مستودع GitHub
            analysis_type: نوع التحليل (summary, security, custom)
            custom_prompt: تعليمات مخصصة للتحليل (للنوع custom)
            
        Returns:
            نتائج التحليل
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # التحقق من صحة رابط GitHub
            if not validate_github_url(repo_url):
                raise ValueError(f"رابط GitHub غير صحيح: {repo_url}")
            
            logger.info(f"بدء تحليل المستودع: {repo_url}")
            logger.info(f"نوع التحليل: {analysis_type}")
            
            # تحويل نوع التحليل
            analysis_enum = self._get_analysis_type(analysis_type)
            
            # تشغيل التحليل
            result = await self.agent.analyze(
                repo_url=repo_url,
                analysis_type=analysis_enum,
                custom_prompt=custom_prompt
            )
            
            logger.info("تم إكمال التحليل بنجاح")
            return result
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المستودع: {e}")
            raise
    
    def _get_analysis_type(self, analysis_type: str) -> AnalysisType:
        """تحويل نوع التحليل من نص إلى Enum."""
        type_mapping = {
            "summary": AnalysisType.SUMMARY,
            "security": AnalysisType.SECURITY,
            "custom": AnalysisType.CUSTOM
        }
        
        if analysis_type not in type_mapping:
            raise ValueError(
                f"نوع تحليل غير مدعوم: {analysis_type}. "
                f"الأنواع المدعومة: {list(type_mapping.keys())}"
            )
        
        return type_mapping[analysis_type]
    
    async def get_context_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات استخدام السياق."""
        if not self.context_manager:
            return {"error": "Context manager not initialized"}
        
        return self.context_manager.get_stats()
    
    async def cleanup(self) -> None:
        """تنظيف الموارد."""
        logger.info("بدء تنظيف موارد الوكيل...")
        
        if self.agent:
            await self.agent.cleanup()
        
        if self.tracer:
            await self.tracer.cleanup()
        
        logger.info("تم تنظيف جميع الموارد")


async def main():
    """مثال على الاستخدام الأساسي."""
    analyzer = GitHubAnalyzerAgent()
    
    try:
        # تهيئة الوكيل
        await analyzer.initialize()
        
        # مثال على تحليل أمني
        result = await analyzer.analyze_repository(
            repo_url="https://github.com/microsoft/TypeScript",
            analysis_type="security"
        )
        
        print("نتائج التحليل:")
        print(result)
        
        # عرض إحصائيات السياق
        stats = await analyzer.get_context_stats()
        print("\nإحصائيات السياق:")
        print(stats)
        
    except Exception as e:
        logger.error(f"خطأ في التطبيق: {e}")
    
    finally:
        await analyzer.cleanup()


if __name__ == "__main__":
    asyncio.run(main())