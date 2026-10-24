# دمج Adaptive Engineering Agent مع EES — v0.7.8

## ما الذي تم دمجه؟
تم تضمين مصدر `adaptive-engineering-agent v0.1.0` داخل `integrations/adaptive-engineering-agent/` مع الحفاظ على أسماء الملفات ومحتواها الأصلي، وإضافة دليل تشغيل واختبارات تكامل سطحية. لم تُستبدل منظومة EES الأساسية ولم تُعدّل المهارات الـ74.

## مكونات الدمج
- `scripts/agent_runtime.py`: وكيل قائم على API متوافق مع OpenAI، وأدوات قراءة/كتابة ملفات وتشغيل أوامر مسموحة.
- `scripts/feedback_store.py`: تخزين feedback ومقترحات تحسين المهارات في SQLite.
- `SKILL.md` و`references/protocol.md` و`references/promotion.md`: تعليمات التشغيل والبروتوكول وضوابط الترقية.
- `tests/test_package.py`: اختبارات المشروع الأصلي.

## العلاقة مع EES
هذا **دمج للمصدر والتوثيق داخل إصدار EES** وليس ادعاءً بأن الوكيل أصبح جزءًا من runtime الأساسي أو أن دورة feedback مرتبطة تلقائيًا بـ `capability-registry.json` أو نظام التقييم المركزي. الربط التشغيلي بين نتائج الوكيل وتقييم مهارات EES يظل خطوة لاحقة تحتاج تصميمًا ومراجعة مستقلة.

## تشغيل اختبارات الوكيل المدمج
من جذر هذا المجلد:

```bash
python integrations/adaptive-engineering-agent/tests/test_package.py
python -m compileall -q integrations/adaptive-engineering-agent/scripts integrations/adaptive-engineering-agent/tests
```

اختبار EES الأساسي يُشغّل بصورة منفصلة وفق `README.md` و`QUALITY-GATE.md`.

## إعداد التشغيل الفعلي
1. انسخ `.env.example` إلى ملف إعداد محلي خارج نظام التحكم بالإصدارات، وأدخل `EES_API_KEY` و`EES_MODEL` بنفسك.
2. راجع `scripts/agent_runtime.py` وقيود الأوامر قبل تشغيله على أي مساحة عمل غير تجريبية.
3. ابدأ ببيئة اختبار غير حساسة. لا تضع مفاتيح API أو أسرارًا داخل ملفات المهارات أو سجل Git.
4. شغّل الاختبارات، وافحص المخرجات يدويًا قبل اعتماد أي مقترح تحسين.

## حدود الأمان
- قائمة السماح للأوامر والكتابة داخل مساحة العمل هي ضوابط داخل التطبيق، وليست بديلًا عن عزل نظام التشغيل أو الحاوية.
- `feedback_store.py` يسجل feedback ومقترحات؛ لا يغيّر ملفات المهارات تلقائيًا ولا يثبت صحة التحسينات.
- وجود Dockerfile لا يثبت أن Docker متاح أو أن صورة الحاوية بُنيت أو شُغّلت.
- لم يُجرَ اتصال حي بمزوّد نموذج في عملية الدمج هذه. نجاح اختبارات الوحدة لا يثبت جودة الوكيل أو جاهزيته للإنتاج.
