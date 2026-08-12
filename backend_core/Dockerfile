# ==============================================================================
# AymnGuard Enterprise v5.0 - Ultimate Production Dockerfile (Degree of Honor)
# المنسق الهيكلي المدمج: أمان سيبراني مطلق، دعم كامل للبلوكتشين والتشفير،
# إدارة دورة حياة العمليات عبر Tini، تزامن التوقيت، وأداء Zero-Lag فائق.
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Builder Stage (مرحلة البناء وتجهيز الاعتماديات ومكتبات التشفير)
# ------------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

# إعداد متغيرات بيئية لبناء نظيف وسريع
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/usr/local/bin:$PATH"

WORKDIR /build

# تثبيت أدوات البناء الأساسية ومكتبات التشفير والبلوكتشين (gcc, libffi, libssl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملفات المتطلبات أولاً لضمان كفاءة التخزين المؤقت (Layer Caching)
COPY requirements.txt .

# تثبيت الحزم باستخدام التخزين المؤقت المتقدم وتسريع الترجمة
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Runtime Stage (المرحلة النهائية التشغيلية فائقة الحماية والاتزان)
# ------------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runtime

# إعداد متغيرات البيئة للتشغيل الآمن، الأداء العالي، وتحديد البورت السحابي المدفوع على 8000
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    APP_ENV="production" \
    TZ="Asia/Aden"

WORKDIR /app

# تثبيت Tini (لإدارة العمليات) و libpq (لقاعدة البيانات) و tzdata (التوقيت) ومكتبات الأمان
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    libpq5 \
    libffi8 \
    libssl3 \
    curl \
    tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# (Hardening) إزالة صلاحيات setuid/setgid لمنع تصعيد الامتيازات من قبل المخترقين
RUN find / -xdev -type f -perm /6000 -exec chmod a-s {} \; || true

# إنشاء مستخدم آمن غير جذري وإعداد الصلاحيات المؤسسية
RUN groupadd -g 10001 aymngroup && \
    useradd -u 10001 -g aymngroup -s /bin/false -m aymnuser

# نسخ المكتبات الجاهزة من مرحلة البناء
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# نسخ الكود المصدري وإعطاء الملكية الفورية للمستخدم الآمن
COPY --chown=aymnuser:aymngroup . .

# إعداد مجلدات التشغيل وضبط الأذونات بدقة جراحية
RUN mkdir -p logs tmp && \
    chmod -R 750 /app && \
    chmod -R 770 logs tmp

# تفعيل المستخدم غير الجذري بشكل نهائي
USER aymnuser

# فحص ذاتي للصحة (Healthcheck) مع فترة سماح لبدء التشغيل على السيرفر السحابي
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://135.181.86.199:${PORT}/ || exit 1

# فتح المنفذ التشغيلي السحابي الموحد
EXPOSE ${PORT}

# استخدام Tini كمدير رئيسي (PID 1) لضمان إغلاق آمن ومعالجة صحيحة للعمليات
ENTRYPOINT ["/usr/bin/tini", "--"]

# أمر التشغيل النهائي الموجه للسيرفر السحابي المدفوع مع دعم حلقة uvloop والوكيل العكسي على البورت 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--loop", "uvloop", "--proxy-headers", "--forwarded-allow-ips", "*"]
