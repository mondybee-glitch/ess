# ابدأ من هنا — v0.7.6

1. اقرأ `SKILL.md` و`references/safety-policy.md`.
2. استخدم `capability-registry.json` بوصفه الجرد الرسمي للمهارات الـ72.
3. لإنشاء/تحسين مهارة: `skills/skill-creation-and-evaluation/SKILL.md`.
4. لتنفيذ خادم MCP: `skills/mcp-server-engineering/SKILL.md`.
5. لاختبار الويب: `skills/browser-e2e-and-test-diagnostics/SKILL.md` والمرجع المرتبط به.
6. لتصميم الواجهات: `skills/ui-ux-design/SKILL.md` والمرجع المرتبط به.
7. نفّذ المدقق والاختبارات الواردة في `README.md`، وسجّل كل ما لم يتم تشغيله على أنه غير متحقق منه.

لا تعتبر نجاح فحص البنية دليلًا على جودة الذكاء الاصطناعي أو الجاهزية للإنتاج.


لتشغيل تقييم فعلي لوكيل متوافق مع المحوّل: راجع `docs/agent-evaluation/ADAPTER-PROTOCOL-v1.md` ثم استخدم `python scripts/run_agent_evals.py --command "python /absolute/path/to/adapter.py" --skill backend-development --limit 3`. لا يُعتبر التنفيذ نجاحًا للجودة قبل التقييم المستقل.


لإنشاء حزمة معرفة Markdown فقط لواجهات الدردشة التي تقبل ملفات Markdown: `python scripts/export_chat_safe_skills.py --output dist/EES_Gemini_Chat_Safe_Markdown.zip`. هذه ليست حزمة تشغيل.


## التوافق متعدد الوكلاء — v0.10.3
هذه الحزمة تضيف نقاط دخول وتعليمات مستقلة لـ Gemini وGoogle Antigravity وClaude، وعقدًا عامًا للوكلاء وملحوظات لـ ChatGPT/البيئات السحابية. ابدأ بقراءة `AGENTS.md` و`docs/multi-agent/UNIVERSAL-AGENT-ARCHITECTURE.md`. وجود ملفات التعليمات لا يثبت أن المنتج حمّلها؛ يجب إجراء اختبار توافق فعلي داخل كل بيئة.
