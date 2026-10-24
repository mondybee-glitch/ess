# Adaptive Engineering Agent

حزمة وكيل هندسي تكيفي عبر API متوافق مع OpenAI. تحتوي على مهارة، حلقة أدوات مقيدة، ذاكرة SQLite للتغذية الراجعة، سياسة ترقية baseline/candidate، وDocker.

## التشغيل المحلي

```bash
cp .env.example .env
export EES_API_KEY='...'
export EES_MODEL='model-id'
export AGENT_WORKSPACE="$PWD/demo-workspace"
mkdir -p "$AGENT_WORKSPACE"
printf '{"task_id":"demo-1","request":"افحص الملفات واكتب تقريرًا","workspace":"%s","acceptance_criteria":["report exists"],"skill_ids":["adaptive-engineering-agent"],"risk_class":"low"}\n' "$AGENT_WORKSPACE" | python scripts/agent_runtime.py
```

## Docker

```bash
docker build -t adaptive-engineering-agent:0.1 .
docker run --rm --network=none \
  --read-only --cap-drop=ALL --security-opt=no-new-privileges \
  --pids-limit=128 --memory=2g --cpus=2 \
  -e EES_API_KEY -e EES_MODEL \
  -v "$PWD/demo-workspace:/workspace:rw" \
  adaptive-engineering-agent:0.1 < task.json
```

`--network=none` يمنع اتصال الوكيل بالمزود، لذلك استخدمه فقط مع Adapter محلي أو افصل موفر API في خدمة مضيفة. لا تمرر المفتاح إلى workspace ولا تسجل قيمته.

## التعلم

سجّل التغذية الراجعة:

```bash
python scripts/feedback_store.py feedback --task-id t1 --skill-id backend-development --category testing --outcome fail --details 'missing negative test'
python scripts/feedback_store.py candidate --skill-id backend-development --reason 'add negative test step' --expected-benefit 'fewer false passes' --regression-risk 'longer runs'
```

التعلم هنا يعني ذاكرة feedback واقتراحات مرشحة، وليس تعديلًا ذاتيًا أو ضمانًا للذكاء الخارق. لا تُرقّى مهارة إلا بعد مقارنة baseline/candidate واختبارات مستقلة.

## حدود مهمة

الحزمة لا تحتوي نموذجًا ذكاءً اصطناعيًا. تحتاج مزودًا خارجيًا ومتغيري `EES_API_KEY` و`EES_MODEL`. اكتمال العملية لا يعني صحة الناتج؛ يجب تشغيل الاختبارات ومراجعة الأدلة.
