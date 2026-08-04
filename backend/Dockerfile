# ==============================================================================
# AymnGuard Enterprise Core - Ultimate Production Dockerfile (Degree of Honor)
# V2 - Enhanced Security, Tini Init, Lifecycle Management & Timezone Sync
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Builder Stage (مرحلة البناء وتجهيز الاعتماديات)
# ------------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

# إعداد متغيرات بيئية لبناء نظيف وسريع
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/usr/local/bin:$PATH"

WORKDIR /build

# تثبيت أدوات البناء الأساسية
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملفات المتطلبات أولاً لضمان كفاءة التخزين المؤقت (Layer Caching)
COPY requirements.txt .

# تثبيت الحزم باستخدام التخزين المؤقت المتقدم وتسريع الترجمة
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Runtime Stage (المرحلة النهائية التشغيلية فائقة الحماية)
# ------------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runtime

# إعداد متغيرات البيئة للتشغيل الآمن، الأداء، والتوقيت المحلي
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=10000 \
    APP_ENV="production" \
    TZ="Asia/Aden"

WORKDIR /app

# تثبيت Tini (لإدارة العمليات) و libpq (لقاعدة البيانات) و tzdata (للتوقيت)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    libpq5 \
    curl \
    tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# (Hardening) إزالة صلاحيات setuid/setgid لمنع تصعيد الامتيازات من قبل المخترقين
RUN find / -xdev -type f -perm /6000 -exec chmod a-s {} \; || true

# إنشاء مستخدم آمن غير جذري وإعداد الصلاحيات
RUN groupadd -g 10001 aymngroup && \
    useradd -u 10001 -g aymngroup -s /bin/false -m aymnuser

# نسخ المكتبات من مرحلة البناء
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# نسخ الكود المصدري وإعطاء الملكية الفورية للمستخدم الآمن (يضمن Alembic وجميع الأكواد)
COPY --chown=aymnuser:aymngroup . .

# إعداد مجلدات التشغيل وضبط الأذونات بدقة جراحية
RUN mkdir -p logs tmp && \
    chmod -R 750 /app && \
    chmod -R 770 logs tmp

# تفعيل المستخدم غير الجذري بشكل نهائي
USER aymnuser

# فحص ذاتي للصحة (Healthcheck) مع فترة سماح لبدء التشغيل
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# فتح المنفذ
EXPOSE ${PORT}

# استخدام Tini كمدير رئيسي (PID 1) لضمان إغلاق آمن ومعالجة صحيحة للعمليات
ENTRYPOINT ["/usr/bin/tini", "--"]

# أمر التشغيل النهائي المحسن لبيئة الإنتاج مع دعم الوكيل العكسي (Reverse Proxies)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "4", "--loop", "uvloop", "--proxy-headers", "--forwarded-allow-ips", "*"]
